"""Writes a reel into an empty CapCut desktop project, copying style from one of the author's projects.

Usage (CapCut closed):
    python3 assemble_draft.py plan.json            # backs up, writes, validates
    python3 assemble_draft.py plan.json --dry-run  # prints the tracks it would write

The plan (JSON, paths in the local filesystem; see SKILL.md for each field):
{
  "project": "<CapCut drafts folder>/<empty project made in the app>",
  "reference": "<CapCut drafts folder>/<author project whose style is copied>",
  "media_references": ["<other author projects, searched for a local .mov and .wav>"],
  "backup_dir": "<folder outside the CapCut drafts folder>",
  "recording": "<reel>/corte.mp4",
  "main": [{"t": 0, "y": 0}, {"t": 5.9, "y": -0.396, "ramp": 0.4}, {"t": 92.94, "y": -0.396}],
  "entrance": true,
  "opening_sounds": true,
  "punch_ins": [{"t": 2.54, "end": 3.3, "word": "microfone"}, {"t": 1.03, "end": 1.8, "scale": 1.1}],
  "overlays": [{"file": "<reel>/exports/01-x.mov", "start": 0, "end": 100.6, "volume": 0}],
  "audio": [{"file": "<reel>/exports/00-sfx.wav", "start": 0}],
  "captions": {"srt": "<reel>/legenda.srt", "words": "<reel>/words.json",
               "fixes": {"wrong text": "right text"}, "y_split": -0.71, "y_full": null}
}

Requires Python 3.8+ and ffprobe. Exits non-zero with a message when a precondition fails.
"""
import copy
import datetime
import json
import re
import shutil
import statistics
import subprocess
import sys
import uuid
from pathlib import Path

US = 1_000_000  # CapCut times are integer microseconds
FRAME = 1 / 30  # the reels are 30 fps; punch-ins snap to this grid
OPENING_WINDOW = 1.0  # library sounds starting this early in the reference project belong to its opening (observed: camera click at 0.0 s, whoosh at 0.3 s)
# Properties that describe one specific media file. Copied from a reference project they break the new project:
# has_sound_separated muted the speech once (the reference project's audio had been extracted to another track).
MEDIA_FIELDS_RESET = {"has_sound_separated": False, "extra_type_option": 0, "local_id": "", "unique_id": "",
                      "local_material_id": "", "origin_material_id": "", "md5": ""}
# Per-material settings of the reference project clip that the new clip must not inherit (loudness, denoise, fades).
SKIP_REFS = {"loudnesses", "realtime_denoises", "vocal_beautifys", "audio_fades"}


def die(msg):
    sys.exit(f"assemble_draft: {msg}")


def load_json(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        die(f"cannot read {p}: {e}")


def win_path(p):
    """/mnt/d/Vídeos/x -> D:/Vídeos/x (CapCut on Windows reads Windows paths)."""
    s = str(Path(p).resolve())
    m = re.match(r"^/mnt/([a-z])/(.*)$", s)
    if not m:
        print(f"assemble_draft: warning: {s} is not on a Windows drive; CapCut on Windows cannot open it", file=sys.stderr)
    return f"{m.group(1).upper()}:/{m.group(2)}" if m else s


def probe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    if r.returncode or not r.stdout.strip():
        die(f"ffprobe failed on {p}: {r.stderr.strip()}")
    return float(r.stdout)


def capcut_running():
    try:
        r = subprocess.run(["tasklist.exe"], capture_output=True, text=True, errors="replace", timeout=20)
    except (OSError, subprocess.TimeoutExpired):
        return None  # not on WSL/Windows: the caller has to confirm by hand
    return "capcut" in r.stdout.lower()


nid = lambda: str(uuid.uuid4()).upper()


class Draft:
    def __init__(self, path):
        self.path = Path(path)
        self.d = load_json(self.path / "draft_content.json")
        self.idx = {x["id"]: (k, x) for k, v in self.d["materials"].items() if isinstance(v, list)
                    for x in v if isinstance(x, dict) and "id" in x}

    def segments(self, kind):
        for t in self.d["tracks"]:
            if t["type"] == kind:
                for s in t["segments"]:
                    yield t, s

    def mat(self, seg):
        return self.idx.get(seg["material_id"], (None, None))

    def main_track(self):
        return next(t for t in self.d["tracks"] if t["type"] == "video")["segments"]

    def entrance(self):
        """The 'in' animation of the first clip, or None."""
        first = self.main_track()[0]
        return next((a for r in first.get("extra_material_refs", []) if self.idx.get(r, ("",))[0] == "material_animations"
                     for a in self.idx[r][1].get("animations", []) if a.get("type") == "in"), None)

    def punch(self):
        """The reference project's punch-in: its scale (median of the short zoomed clips of the main track) and the
        library sound that starts on the frame of its first punch-in, as (scale, sound segment, sound material)."""
        zoomed = [s for s in self.main_track() if (s.get("clip") or {}).get("scale", {}).get("x", 1.0) > 1.2
                  and s["target_timerange"]["duration"] < 2 * US]
        if not zoomed:
            return None, None, None
        t0 = zoomed[0]["target_timerange"]["start"]
        snd = next(((s, m) for _, s in self.segments("audio") for k, m in [self.mat(s)]
                    if k == "audios" and m.get("type") in ("sound", "music")
                    and abs(s["target_timerange"]["start"] - t0) <= FRAME * US), (None, None))
        return statistics.median(s["clip"]["scale"]["x"] for s in zoomed), *snd


def moving_ranges(main, rec_dur):
    """Where the recording is off its full-frame place: split-screen ranges and the ramps into and out of them."""
    bps = sorted(main, key=lambda b: b["t"])
    out, prev = [], 0.0
    for i, b in enumerate(bps):
        y = b.get("y", 0.0)
        e = bps[i + 1]["t"] if i + 1 < len(bps) else rec_dur
        if y != 0:
            out.append((b["t"], e))
        elif prev != 0 and b.get("ramp"):
            out.append((b["t"], b["t"] + b["ramp"]))
        prev = y
    return out


def punch_ins(plan, ref, rec_dur):
    """The plan's punch-ins, checked against the frame: each one a hard cut to the reference project's scale, held on a
    spoken word, only where the face fills the frame (after the entrance, outside split screens and their ramps)."""
    scale, _, _ = ref.punch()
    ent = ref.entrance() if plan.get("entrance", True) else None
    ent_end = (ent or {}).get("duration", 0) / US
    blocked = moving_ranges(plan["main"], rec_dur)
    out, last = [], -1.0
    for p in sorted(plan.get("punch_ins", []), key=lambda p: p["t"]):
        # on the frame grid: a keyframe between two frames gives one frame of half zoom in CapCut
        t, e = round(p["t"] / FRAME) * FRAME, round(p["end"] / FRAME) * FRAME
        s = p.get("scale", scale)
        if s is None:
            die(f"punch-in at {t}: the reference project has no punch-in to take the scale from; give 'scale'")
        if not 0 < e - t <= 2.0:
            die(f"punch-in at {t}: it must last more than 0 and at most 2 s (the reference's last 0.7 to 1.0 s)")
        if t < ent_end:
            die(f"punch-in at {t} overlaps the entrance animation (0 to {ent_end:.2f} s)")
        if e > rec_dur:
            die(f"punch-in at {t} ends after the recording ({rec_dur:.2f} s)")
        hit = next(((a, b) for a, b in blocked if t < b and e > a), None)
        if hit:
            die(f"punch-in at {t}-{e} falls in a split screen or its keyframe ({hit[0]:.2f}-{hit[1]:.2f} s): "
                "zoom only where the face fills the frame")
        if t < last:
            die(f"punch-in at {t} overlaps the previous one")
        out.append({**p, "t": t, "end": e, "scale": s})
        last = e
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    if len(args) != 1:
        die("usage: assemble_draft.py plan.json [--dry-run]")
    plan = load_json(args[0])
    proj = Path(plan["project"])
    if not (proj / "draft_content.json").exists():
        die(f"{proj} is not a CapCut project (no draft_content.json). Ask the user to create an empty project in the CapCut app.")
    out = Draft(proj)
    if any(t["segments"] for t in out.d.get("tracks", [])) and "--force" not in sys.argv:
        die(f"{proj} already has clips on its timeline. Writing would replace the user's edit; ask first, then pass --force.")
    ref = Draft(plan["reference"])
    others = [Draft(p) for p in plan.get("media_references", [])]
    D = out.d
    D.setdefault("materials", {})

    def add(kind, m):
        D["materials"].setdefault(kind, []).append(m)
        return m["id"]

    def clone_refs(src, seg, keep_anim):
        refs = []
        for r in seg.get("extra_material_refs", []):
            kind, m = src.idx.get(r, (None, None))
            if kind is None or kind in SKIP_REFS or (kind == "material_animations" and not keep_anim):
                continue
            c = copy.deepcopy(m)
            c["id"] = nid()
            refs.append(add(kind, c))
        return refs

    def seg_from(src, tmpl, material_id, start, dur, src_start=0.0, keep_anim=False):
        s = copy.deepcopy(tmpl)
        s.update(id=nid(), material_id=material_id, common_keyframes=[], keyframe_refs=[],
                 source_timerange={"start": round(src_start * US), "duration": round(dur * US)},
                 target_timerange={"start": round(start * US), "duration": round(dur * US)})
        s["extra_material_refs"] = clone_refs(src, tmpl, keep_anim)
        if s.get("clip"):
            s["clip"] = {"scale": {"x": 1.0, "y": 1.0}, "rotation": 0.0, "transform": {"x": 0.0, "y": 0.0},
                         "flip": {"vertical": False, "horizontal": False}, "alpha": 1.0}
        return s

    def media(kind, tmpl, path, dur, **extra):
        m = copy.deepcopy(tmpl)
        m.update(MEDIA_FIELDS_RESET)
        m.update(id=nid(), path=win_path(path), duration=round(dur * US), **extra)
        if "material_name" in m:
            m["material_name"] = Path(path).name
        if kind == "audios":
            m["name"] = Path(path).name
        return add(kind, m)

    def kf(prop, pts):
        return {"id": nid(), "material_id": "", "property_type": prop, "keyframe_list": [
            {"id": nid(), "curveType": "Line", "time_offset": round(t * US), "left_control": {"x": 0.0, "y": 0.0},
             "right_control": {"x": 0.0, "y": 0.0}, "values": [v], "string_value": "", "graphID": ""} for t, v in pts]}

    def track(kind, segs):
        return {"attribute": 0, "flag": 0, "id": nid(), "is_default_name": True, "name": "", "segments": segs, "type": kind}

    def find_local(kind, ext):
        """A material of the author's own media (a local .mov or .wav) and its segment, used as the shape to copy."""
        for src in [ref] + others:
            for t, s in src.segments("video" if kind == "videos" else "audio"):
                k, m = src.mat(s)
                p = (m or {}).get("path", "").lower()
                if k == kind and p.endswith(ext) and "/cache/" not in p and "ios_album" not in p:
                    return src, m, s
        die(f"no {ext} clip in the reference project or media_references to copy the material shape from; add a project that has one")

    tracks = []
    rec = Path(plan["recording"])
    rec_dur = probe(rec)

    # 1. recording: one clip per breakpoint of "main"; a ramp keyframes y from the previous value
    main_tracks = [t for t in ref.d["tracks"] if t["type"] == "video"]
    first = main_tracks[0]["segments"][0]
    plain = main_tracks[0]["segments"][1] if len(main_tracks[0]["segments"]) > 1 else first
    rec_tmpl = ref.mat(first)[1]
    rec_id = media("videos", rec_tmpl, rec, rec_dur, has_audio=True, width=1080, height=1920)
    bps = sorted(plan["main"], key=lambda b: b["t"])
    if not bps or bps[0]["t"] != 0:
        bps.insert(0, {"t": 0, "y": 0})
    punches = punch_ins(plan, ref, rec_dur)
    segs, prev_y, split_ranges = [], 0.0, []
    for i, b in enumerate(bps):
        a = b["t"]
        e = bps[i + 1]["t"] if i + 1 < len(bps) else rec_dur
        keep = i == 0 and plan.get("entrance", True)
        s = seg_from(ref, first if keep else plain, rec_id, a, e - a, a, keep_anim=keep)
        y = b.get("y", 0.0)
        s["clip"]["transform"]["y"] = y
        # keyframe times are in the source's time, which here equals the timeline's
        r = b.get("ramp") if b.get("ramp") and y != prev_y else 0.0
        ys = [(a, prev_y), (a + r, y)] if r else []
        # a punch-in is a hard cut: the scale jumps between two keyframes one frame apart, in and out
        sc = []
        for p in (p for p in punches if a <= p["t"] < e):
            sc += [(p["t"] - FRAME, 1.0)] if p["t"] - FRAME >= a else []
            sc += [(p["t"], p["scale"]), (p["end"] - FRAME, p["scale"]), (p["end"], 1.0)]
        if ys or sc:
            pts = sorted({t for t, _ in ys + sc})
            yv = lambda t: y if not r else prev_y + (y - prev_y) * min(max((t - a) / r, 0.0), 1.0)
            sv = lambda t: next((v for tt, v in sc if abs(tt - t) < 1e-9), 1.0)
            s["common_keyframes"] = [kf("KFTypePositionX", [(t, 0.0) for t in pts]),
                                     kf("KFTypePositionY", [(t, yv(t)) for t in pts]),
                                     kf("KFTypeScaleX", [(t, sv(t)) for t in pts]),
                                     kf("KFTypeRotation", [(t, 0.0) for t in pts])]
        if y != 0:
            split_ranges.append((a, e))
        prev_y = y
        segs.append(s)
    tracks.append(track("video", segs))

    # 2. overlays (.mov with alpha): packed onto as few tracks as possible without overlap
    if plan.get("overlays"):
        src, mt, st = find_local("videos", ".mov")
        lanes = []
        for o in sorted(plan["overlays"], key=lambda o: o["start"]):
            f = Path(o["file"])
            fd = probe(f)
            dur = min(o.get("end", o["start"] + fd), rec_dur) - o["start"]
            m = media("videos", mt, f, fd, has_audio=False, width=1080, height=1920)
            s = seg_from(src, st, m, o["start"], min(dur, fd), o.get("src_start", 0.0))
            s["volume"] = o.get("volume", 0.0)
            lane = next((l for l in lanes if l[-1][1] <= o["start"] + 1e-3), None)
            if lane is None or o.get("own_track"):
                lane = []
                lanes.append(lane)
            lane.append((o["start"], o["start"] + dur, s))
        tracks += [track("video", [x[2] for x in l]) for l in lanes]

    # 3. audio files of the reel (00-sfx.wav), each on its own track
    for au in plan.get("audio", []):
        src, mt, st = find_local("audios", ".wav")
        f = Path(au["file"])
        fd = probe(f)
        m = media("audios", mt, f, fd)
        s = seg_from(src, st, m, au.get("start", 0.0), min(fd, rec_dur - au.get("start", 0.0)))
        s["volume"] = au.get("volume", 1.0)
        tracks.append(track("audio", [s]))

    # 4. opening sounds of the reference project: library sounds in its first OPENING_WINDOW seconds, same times and volumes
    if plan.get("opening_sounds", True):
        segs = []
        for t, s in ref.segments("audio"):
            k, m = ref.mat(s)
            if k == "audios" and m.get("type") in ("sound", "music") and s["target_timerange"]["start"] < OPENING_WINDOW * US:
                c = copy.deepcopy(m)
                c["id"] = nid()
                ns = seg_from(ref, s, add("audios", c), s["target_timerange"]["start"] / US,
                              s["target_timerange"]["duration"] / US, s["source_timerange"]["start"] / US)
                ns["volume"] = s.get("volume", 1.0)
                segs.append(ns)
        if segs:
            tracks.append(track("audio", segs))

    # 5. each punch-in gets the reference project's punch-in sound on its first frame, same cut and volume
    _, ps, pm = ref.punch()
    sounded = [p for p in punches if p.get("sound", True)]
    if sounded and ps is None:
        print("assemble_draft: warning: the reference project has no sound on its punch-in; punch-ins go silent", file=sys.stderr)
    elif sounded:
        segs = []
        for p in sounded:
            c = copy.deepcopy(pm)
            c["id"] = nid()
            ns = seg_from(ref, ps, add("audios", c), p["t"], ps["target_timerange"]["duration"] / US,
                          ps["source_timerange"]["start"] / US)
            ns["volume"] = ps.get("volume", 1.0)
            segs.append(ns)
        tracks.append(track("audio", segs))

    # 6. captions: SRT cues in the reference project's caption template, word timing from words.json
    cap = plan.get("captions")
    if cap:
        counts = {}
        for _, s in ref.segments("text"):
            k, m = ref.mat(s)
            if k == "text_templates":
                counts.setdefault(m.get("name"), []).append(s)
        if not counts:
            die("the reference project has no caption template (text_templates) to copy")
        name = cap.get("template") or max(counts, key=lambda n: len(counts[n]))
        cap_seg = counts[name][0]
        cap_tmpl = ref.mat(cap_seg)[1]
        cap_text = ref.idx[cap_tmpl["text_info_resources"][0]["text_material_id"]][1]
        y_full = cap.get("y_full")
        if y_full is None:
            y_full = (cap_seg.get("clip") or {}).get("transform", {}).get("y", -0.56)  # the reference project's own caption height
        y_split = cap.get("y_split", -0.71)  # on the chest, under a 960 px panel, in the author's split-screen reels
        words = load_json(cap["words"]) if cap.get("words") else []

        def srt(p):
            sec = lambda x: (lambda h, m_, r: int(h) * 3600 + int(m_) * 60 + float(r.replace(",", ".")))(*x.strip().split(":"))
            for n, blk in enumerate(re.split(r"\n\s*\n", Path(p).read_text(encoding="utf-8-sig").strip()), 1):
                L = blk.strip().splitlines()
                if len(L) >= 3 and "-->" in L[1]:
                    a, b = L[1].split("-->")
                    yield n, sec(a), sec(b), " ".join(L[2:]).strip()

        segs = []
        for n, a, b, text in srt(cap["srt"]):
            for wrong, right in cap.get("fixes", {}).items():
                text = text.replace(wrong, right)
            ws = [w for w in words if w.get("cue") == n] if words and "cue" in words[0] else \
                 [w for w in words if a - 0.05 <= (w["s"] + w["e"]) / 2 <= b + 0.05]
            tokens, starts, ends = [], [], []
            for i, tok in enumerate(text.split()):
                w = ws[i] if i < len(ws) else None
                s0 = max(0, round(((w["s"] if w else a) - a) * 1000))
                e0 = max(s0, round(((w["e"] if w else b) - a) * 1000))
                if tokens:
                    tokens.append(" "); starts.append(ends[-1]); ends.append(ends[-1])
                tokens.append(tok); starts.append(s0); ends.append(e0)
            tm = copy.deepcopy(cap_text)
            content = json.loads(tm["content"])
            content["text"] = text
            for st in content.get("styles", []):
                st["range"] = [0, len(text)]
            tm.update(id=nid(), content=json.dumps(content, ensure_ascii=False), recognize_text=text,
                      words={"start_time": starts, "end_time": ends, "text": tokens})
            add("texts", tm)
            tt = copy.deepcopy(cap_tmpl)
            tt["id"] = nid()
            res = tt["text_info_resources"][0]
            res["id"], res["text_material_id"] = nid(), tm["id"]
            res["attach_info"]["duration"] = round((b - a) * US)
            res["extra_material_refs"] = clone_refs(ref, {"extra_material_refs": res.get("extra_material_refs", [])}, True)
            add("text_templates", tt)
            s = seg_from(ref, cap_seg, tt["id"], a, b - a, 0.0, keep_anim=True)
            # a reel with a split screen keeps one caption height, under the panel, as the author's approved reels do
            s["clip"]["transform"]["y"] = y_split if split_ranges else y_full
            for r in s["extra_material_refs"]:  # the caption animation spans the whole cue
                k, m = next(((k, x) for k, v in D["materials"].items() if isinstance(v, list)
                             for x in v if isinstance(x, dict) and x.get("id") == r), (None, None))
                if k == "material_animations":
                    for an in m.get("animations", []):
                        if an.get("type") == "caption":
                            an["duration"] = round((b - a) * US)
            segs.append(s)
        tracks.append(track("text", segs))

    D["tracks"] = tracks
    D["duration"] = round(rec_dur * US)
    D["canvas_config"] = {**ref.d.get("canvas_config", {}), "width": 1080, "height": 1920}

    summary = [(t["type"], len(t["segments"])) for t in tracks]
    pin = [(round(p["t"], 2), round(p["end"], 2), round(p["scale"], 2)) for p in punches]
    if dry:
        print(f"dry run: {rec_dur:.2f} s, tracks {summary}, split ranges {split_ranges}, punch-ins {pin}")
        return

    running = capcut_running()
    if running:
        die("CapCut is open. Ask the user to close it: CapCut rewrites the project on close and would erase this write.")
    if running is None and "--capcut-closed" not in sys.argv:
        die("cannot check whether CapCut is open (no tasklist.exe). Confirm with the user, then pass --capcut-closed.")

    bdir = Path(plan["backup_dir"]) / f"{proj.name}-{datetime.datetime.now():%Y%m%d-%H%M%S}"
    if str(bdir.resolve()).startswith(str(proj.parent.resolve())):
        die("backup_dir is inside the CapCut drafts folder, where CapCut would list the backup as a project")
    shutil.copytree(proj, bdir)

    text = json.dumps(D, ensure_ascii=False, separators=(",", ":"))
    targets = [proj / "draft_content.json"] + sorted((proj / "Timelines").glob("*/draft_content.json"))
    for p in targets:  # CapCut 9.x reads the copy under Timelines/<id>/; both must match
        p.write_text(text, encoding="utf-8")

    meta_p = proj / "draft_meta_info.json"
    meta = load_json(meta_p)
    meta["tm_duration"] = D["duration"]
    files = [(rec, rec_dur, "video")] + [(Path(o["file"]), probe(o["file"]), "video") for o in plan.get("overlays", [])] \
        + [(Path(a["file"]), probe(a["file"]), "music") for a in plan.get("audio", [])]
    value = [{"ai_group_type": "", "create_time": 0, "duration": round(d * US), "enter_from": 0, "extra_info": "",
              "file_Path": win_path(p), "height": 1920 if k == "video" else 0, "id": nid(), "import_time": 0,
              "import_time_ms": -1, "item_source": 1, "material_color_tag": "", "md5": "", "metetype": k,
              "roughcut_time_range": {"duration": -1, "start": -1}, "sub_time_range": {"duration": -1, "start": -1},
              "type": 0, "width": 1080 if k == "video" else 0} for p, d, k in files]
    dm = meta.setdefault("draft_materials", [])
    slot = next((x for x in dm if x.get("type") == 0), None)
    if slot is None:
        dm.append({"type": 0, "value": value})
    else:
        slot["value"] = value
    meta_p.write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")

    # validate: every reference resolves, no duplicate ids, no overlap inside a track
    idx = {}
    for k, v in D["materials"].items():
        for x in v if isinstance(v, list) else []:
            if isinstance(x, dict) and "id" in x:
                if x["id"] in idx:
                    die(f"duplicate material id {x['id']}")
                idx[x["id"]] = k
    for t in tracks:
        end = -1
        for s in sorted(t["segments"], key=lambda s: s["target_timerange"]["start"]):
            if s["material_id"] not in idx or any(r not in idx for r in s.get("extra_material_refs", [])):
                die(f"dangling reference in a {t['type']} track")
            if s["target_timerange"]["start"] < end:
                die(f"overlapping clips in a {t['type']} track")
            end = s["target_timerange"]["start"] + s["target_timerange"]["duration"]
    print(f"written: {rec_dur:.2f} s, tracks {summary}, split ranges {split_ranges}, punch-ins {pin}")
    print(f"files: {[str(p.relative_to(proj)) for p in targets] + ['draft_meta_info.json']}; backup: {bdir}")


if __name__ == "__main__":
    main()
