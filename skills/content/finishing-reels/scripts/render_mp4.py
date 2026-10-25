"""Renders the finished reel straight to mp4 from the same plan.json as assemble_draft.py, without CapCut.

Usage:
    python3 render_mp4.py plan.json out.mp4 [--preview SECONDS]

What it reproduces from the reference project (read from the CapCut drafts and the local CapCut cache):
- the entrance of the first clip, when it is "Balançar para cima e para a direita" (the CapCut shader, frame by frame);
- the opening sounds, from the cache files the reference project uses;
- the punch-ins of the plan, as hard cuts to the reference project's scale around the frame centre, each with the
  reference project's punch-in sound;
- the caption template: font, size, max line width, white text with the spoken word in the template colour,
  black stroke and hard shadow, pages of up to three words.
Everything else comes from the plan: the recording with its split-screen keyframes, the overlays, the reel's audio.

Requires ffmpeg with libass, numpy (the entrance) and fontTools (accented capitals for a font that lacks them):
    python3 -m venv .venv && .venv/bin/pip install numpy fonttools
"""
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from assemble_draft import (US, WORD_CAP_PX, WORD_FILL, WORD_LIFT_PX, WORD_SHADOW, Draft, cutouts, die,  # noqa: E402
                            load_json, local_path, probe, punch_ins, screen_words, sound_times)
import own_assets  # noqa: E402

W, H, FPS = 1080, 1920, 30
HALF = H / 2  # CapCut's y unit is half the frame height; negative is down
ENTRANCE = "Balançar para cima e para a direita"
# CapCut caption size 12 matches libass size 74 with this template's font: measured on the
# author's posted reel, where "DA TUA CONVERSA" spans 775 px.
ASS_PER_CAPCUT_SIZE = 74 / 12
PAGE_WORDS = 3  # the word-by-word templates show up to three words at a time
# CapCut breaks a caption line a little before line_max_width: on the author's reel "CONVERSA COM ELA" (835 px)
# stays on one line and "UMA CONVERSA QUE" (839 px) breaks, with line_max_width 0.82 (886 px).
LINE_LIMIT = 837 / 886


def ff(args, **kw):
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", *args], **kw)
    if r.returncode:
        die(f"ffmpeg failed: {' '.join(map(str, args))[:300]}")
    return r


# ---------- entrance: CapCut's "Balançar para cima e para a direita", from its Transform.lua and shader ----------

def ease(u):
    # Transform.lua funcEaseAction: damped spring from the start pose to rest
    return 0.0 if u in (0.0, 1.0) else math.exp(-7 * u) * math.sin((u - 0.075) * 2 * math.pi / 0.3) + 1.0


def blur_step(u, dur):
    # funcEaseBlurAction: blur follows the speed of the spring; 7.0 / duration is the tween's start value
    w = 2 * math.pi / 0.3
    d = (-7 * math.exp(-7 * u) * math.sin((u - 0.075) * w) + math.exp(-7 * u) * math.cos((u - 0.075) * w) * w) * 0.1
    return abs(7.0 / dur * d)


def render_entrance(rec, out, dur=0.5):
    try:
        import numpy as np
    except ImportError:
        die("the entrance needs numpy: python3 -m venv .venv && .venv/bin/pip install numpy fonttools")
    n = round(dur * FPS)
    raw = ff(["-i", str(rec), "-frames:v", str(n), "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
             capture_output=True).stdout
    frames = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).astype(np.float32)
    ratio = W / H
    cols, rows = np.meshgrid((np.arange(W) + 0.5) / W, 1 - (np.arange(H) + 0.5) / H)
    px, py = (cols * 2 - 1) * ratio, rows * 2 - 1  # output pixel in the effect's space (y up, height 2)
    start, rot0, sc0 = (-1.2 * ratio, 1.2), -20.0, 1.1
    d = np.array([-1.0, 1.0]) / math.sqrt(2)  # blurDirection (-1, 1), normalised as in the shader
    enc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "ffv1", str(out)], stdin=subprocess.PIPE)
    for i in range(min(n, len(frames))):
        u = i / FPS / dur
        e = ease(u)
        # y and the angle flip sign against the shader's convention: checked frame by frame against CapCut's export
        tx, ty = start[0] * (1 - e), -start[1] * (1 - e)
        a = math.radians(-rot0 * (1 - e))
        s = sc0 + (1.0 - sc0) * e
        # inverse model: undo translate, rotate, scale (SetTRS order)
        qx, qy = px - tx, py - ty
        ux = (math.cos(a) * qx + math.sin(a) * qy) / s
        uy = (-math.sin(a) * qx + math.cos(a) * qy) / s
        ux, uy = (ux / ratio + 1) / 2, (uy + 1) / 2
        inside = (ux >= -1) & (ux <= 2) & (uy >= -1) & (uy <= 2)
        step = blur_step(u, dur)
        acc = np.zeros((H, W, 3), np.float32)
        for k in range(-7, 8):  # 15 taps, mirrored outside the frame: 1 - abs(abs(c) - 1)
            cx = 1 - np.abs(np.abs(ux + d[0] * step / W * k) - 1)
            cy = 1 - np.abs(np.abs(uy + d[1] * step / H * k) - 1)
            fx = np.clip(cx * W - 0.5, 0, W - 1)
            fy = np.clip((1 - cy) * H - 0.5, 0, H - 1)
            x0, y0 = fx.astype(np.int32), fy.astype(np.int32)
            x1, y1 = np.minimum(x0 + 1, W - 1), np.minimum(y0 + 1, H - 1)
            wx, wy = (fx - x0)[..., None], (fy - y0)[..., None]
            f = frames[i]
            acc += (f[y0, x0] * (1 - wx) * (1 - wy) + f[y0, x1] * wx * (1 - wy)
                    + f[y1, x0] * (1 - wx) * wy + f[y1, x1] * wx * wy)
        img = (acc / 15) * inside[..., None]
        enc.stdin.write(np.clip(img, 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close()
    enc.wait()


# ---------- CapCut's files or ours ----------

def pick_font(path, own, what):
    """(font file, family, size factor, horizontal scale): the reference project's font, or ours when the cache
    lacks it or the plan asks for ours."""
    if not own and path.exists():
        return path, path.stem, 1.0, 1.0
    if not own:
        print(f"render_mp4: {what} font {path.name} not in the CapCut cache; using our free stand-in", file=sys.stderr)
    f, family, k, sx = own_assets.font(path.stem)
    return f, family, k, sx


def pick_sound(path, name, own, what):
    """(file, its start in s): the reference project's library sound, or our synthesized one (cut already, start 0)."""
    if not own and path.exists():
        return path, None
    f = own_assets.sound(name)
    if f is None:
        print(f"render_mp4: warning: {what} '{name}' not in the CapCut cache and no stand-in; skipped", file=sys.stderr)
    elif not own:
        print(f"render_mp4: {what} '{name}' not in the CapCut cache; using our synthesized stand-in", file=sys.stderr)
    return f, 0.0


# ---------- captions ----------

def accent_font(src, dst, family):
    """Adds the accented capitals pt-BR needs, composed from the font's own glyphs, when the font lacks them."""
    try:
        from fontTools.pens.boundsPen import BoundsPen
        from fontTools.ttLib import TTFont
        from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphComponent
    except ImportError:
        print("render_mp4: warning: fontTools missing, accented letters fall back to another font", file=sys.stderr)
        shutil.copy(src, dst)
        return family
    f = TTFont(src)
    cmap = f.getBestCmap()
    if all(ord(c) in cmap for c in "ÁÃÇÉÊÍÓÕÚ"):
        shutil.copy(src, dst)
        return family
    gs, glyf, hmtx = f.getGlyphSet(), f["glyf"], f["hmtx"]

    def bounds(name):
        p = BoundsPen(gs)
        gs[name].draw(p)
        return p.bounds

    def comp(name, x, y, sx=1.0, sy=1.0):
        c = GlyphComponent()
        c.glyphName, c.x, c.y, c.flags = name, round(x), round(y), 0x4
        if (sx, sy) != (1.0, 1.0):
            c.transform = [[sx, 0.0], [0.0, sy]]
        return c

    def put(ch, comps, base):
        g = Glyph()
        g.numberOfContours, g.components = -1, comps
        name = f"uni{ord(ch):04X}"
        glyf[name], hmtx[name] = g, hmtx[base]
        for t in f["cmap"].tables:
            if t.isUnicode():
                t.cmap[ord(ch)] = name

    gap = 30  # font units between the letter and its accent
    marks = {"grave": "`", "acute": "`", "circ": "^", "tilde": "~"}  # the acute is the grave mirrored
    for ch, (base, acc) in {"À": ("A", "grave"), "Á": ("A", "acute"), "Â": ("A", "circ"), "Ã": ("A", "tilde"),
                            "É": ("E", "acute"), "Ê": ("E", "circ"), "Í": ("I", "acute"), "Ó": ("O", "acute"),
                            "Ô": ("O", "circ"), "Õ": ("O", "tilde"), "Ú": ("U", "acute")}.items():
        if ord(ch) in cmap or ord(marks[acc]) not in cmap:
            continue
        b, m = cmap[ord(base)], cmap[ord(marks[acc])]
        bx0, _, bx1, by1 = bounds(b)
        ax0, ay0, ax1, _ = bounds(m)
        sx = -1.0 if acc == "acute" else 1.0
        dx = (bx0 + bx1) / 2 - sx * (ax0 + ax1) / 2
        put(ch, [comp(b, 0, 0), comp(m, dx, by1 + gap - ay0, sx)], b)
    if ord("Ç") not in cmap and ord(",") in cmap:
        c, cm = cmap[ord("C")], cmap[ord(",")]
        bx0, by0, bx1, _ = bounds(c)
        ax0, _, ax1, ay1 = bounds(cm)
        put("Ç", [comp(c, 0, 0), comp(cm, (bx0 + bx1) / 2 - 0.75 * (ax0 + ax1) / 2, by0 + 20 - 0.75 * ay1, 0.75, 0.75)], c)
    f.setGlyphOrder(glyf.glyphOrder)
    f["maxp"].numGlyphs = len(glyf.glyphOrder)
    f["maxp"].maxComponentElements = max(getattr(f["maxp"], "maxComponentElements", 0), 2)
    f["maxp"].maxComponentDepth = max(getattr(f["maxp"], "maxComponentDepth", 0), 1)
    new = family + " PT"
    for rec in f["name"].names:
        if rec.nameID in (1, 4, 16):
            rec.string = new
    f.save(dst)
    return new


def ass_time(t):
    cs = int(round(max(0.0, t) * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


def ass_colour(rgb):
    r, g, b = (round(c * 255) for c in rgb[:3])
    return f"&H00{b:02X}{g:02X}{r:02X}&"


def vmetrics(f):
    """(ascent, descent) as libass reads them: the OS/2 win metrics when the font sets them, else hhea. A font whose
    win and hhea metrics differ (Lexend) came out 22% small when sized by hhea."""
    o = f["OS/2"]
    if o.usWinAscent + o.usWinDescent:
        return o.usWinAscent, -o.usWinDescent
    return f["hhea"].ascent, f["hhea"].descent


def text_width(font, size):
    """Width in px of a string at an ASS font size, from the font's advances; None without fontTools."""
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        return None
    f = TTFont(font)
    cmap, hmtx = f.getBestCmap(), f["hmtx"]
    asc, desc = vmetrics(f)
    em = asc - desc  # libass sizes a font by ascent + descent, not by units per em
    space = hmtx[cmap[32]][0] if 32 in cmap else em / 4
    return lambda t: sum(hmtx[cmap[ord(c)]][0] if ord(c) in cmap else space for c in t) * size / em


def wrap(words, width, limit):
    """CapCut fills a line before breaking: greedy, first line widest."""
    if width is None:
        return " ".join(words)
    lines, cur = [], []
    for w in words:
        if cur and width(" ".join(cur + [w])) > limit:
            lines.append(cur)
            cur = []
        cur.append(w)
    lines.append(cur)
    return "\\N".join(" ".join(l) for l in lines)


def write_ass(path, cues, style, split_ranges):
    """cues: [(start, end, [(word, s, e), ...])]; one event per stretch in which the highlighted word is the same."""
    fs = style["size"]
    head = (f"[Script Info]\nScriptType: v4.00+\nPlayResX: {W}\nPlayResY: {H}\nWrapStyle: 2\nScaledBorderAndShadow: yes\n\n"
            "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
            "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
            "Alignment, MarginL, MarginR, MarginV, Encoding\n"
            f"Style: Cap,{style['family']},{fs:.0f},&H00FFFFFF&,&H00FFFFFF&,&H00000000&,&H00000000&,0,0,0,0,"
            f"{style.get('scale_x', 1.0) * 100:.1f},100,0,0,1,"
            f"{style['outline']:.1f},0,5,{style['margin']},{style['margin']},0,1\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    hi, white = style["highlight"], "&H00FFFFFF&"
    xs, ys = style["shadow_xy"]
    out = []
    for a, b, words in cues:
        pages = [words[i:i + PAGE_WORDS] for i in range(0, len(words), PAGE_WORDS)]
        for k, pg in enumerate(pages):
            p0 = a if k == 0 else pg[0][1]
            p1 = pages[k + 1][0][1] if k + 1 < len(pages) else b
            mid = (p0 + p1) / 2
            # a reel with a split screen keeps one caption height, under the panel, as the author's approved reels do
            y = HALF - (style["y_split"] if split_ranges else style["y_full"]) * HALF
            # a stretch where the panel fills the frame takes its own height, so the caption leaves the drawing
            for r0, r1, ry in style["y_ranges"]:
                if r0 <= mid < r1:
                    y = HALF - ry * HALF
            cuts = sorted({p0, p1, *[min(max(s, p0), p1) for _, s, _ in pg]})
            for s0, s1 in zip(cuts, cuts[1:]):
                if s1 - s0 < 0.01:
                    continue
                cur = max((i for i, (_, s, _) in enumerate(pg) if s <= s0 + 1e-6), default=None)
                plain = [w.upper() for w, _, _ in pg]
                lines = wrap(plain, style["width"], (W - 2 * style["margin"]) * LINE_LIMIT).split("\\N")
                txt, k = [], 0
                for line in lines:
                    parts = []
                    for w in line.split(" "):
                        parts.append("{\\c" + (hi if k == cur else white) + "}" + w)
                        k += 1
                    txt.append(" ".join(parts))
                txt = "\\N".join(txt)
                out.append(f"Dialogue: 0,{ass_time(s0)},{ass_time(s1)},Cap,,0,0,0,,"
                           f"{{\\an5\\pos(540,{y:.0f})\\xshad{xs:.1f}\\yshad{ys:.1f}\\4c&H00000000&}}{txt}")
    Path(path).write_text(head + "\n".join(out) + "\n", encoding="utf-8")
    return len(out)


def srt_cues(p, words, fixes):
    sec = lambda x: (lambda h, m_, r: int(h) * 3600 + int(m_) * 60 + float(r.replace(",", ".")))(*x.strip().split(":"))
    out = []
    for n, blk in enumerate(re.split(r"\n\s*\n", Path(p).read_text(encoding="utf-8-sig").strip()), 1):
        L = blk.strip().splitlines()
        if len(L) < 3 or "-->" not in L[1]:
            continue
        a, b = (sec(x) for x in L[1].split("-->"))
        text = " ".join(L[2:]).strip()
        for wrong, right in fixes.items():
            text = text.replace(wrong, right)
        ws = [w for w in words if w.get("cue") == n] if words and "cue" in words[0] else \
             [w for w in words if a - 0.05 <= (w["s"] + w["e"]) / 2 <= b + 0.05]
        toks = text.split()
        timed = []
        for i, tok in enumerate(toks):
            w = ws[i] if i < len(ws) else None
            s = w["s"] if w else (timed[-1][2] if timed else a)
            timed.append((tok, max(a, s), w["e"] if w else b))
        out.append((a, b, timed))
    return out


def write_words_ass(path, ws, font, family, size, squeeze):
    """One event per word, centred on x, its capitals placed where CapCut draws the word template."""
    from fontTools.ttLib import TTFont
    f = TTFont(font)
    asc, desc = vmetrics(f)
    em = asc - desc
    cap = getattr(f["OS/2"], "sCapHeight", 0) or f["head"].unitsPerEm * 0.7
    out = []
    for w in ws:
        cap_px = WORD_CAP_PX * w["scale"] * size / 15
        fs = cap_px * em / cap
        centre = HALF - w["y"] * HALF - WORD_LIFT_PX * w["scale"] * size / 15
        base = centre + cap_px / 2
        box = base - (asc + desc) * fs / em / 2  # libass centres the ascent-descent box
        sh = WORD_SHADOW * cap_px
        out.append(f"Dialogue: 0,{ass_time(w['t'])},{ass_time(w['end'])},Word,,0,0,0,,"
                   f"{{\\an5\\pos(540,{box:.0f})\\fs{fs:.1f}\\fscx{squeeze * 100:.1f}\\xshad{sh:.1f}\\yshad{sh:.1f}}}{w['text']}")
    r, g, b = WORD_FILL
    head = (f"[Script Info]\nScriptType: v4.00+\nPlayResX: {W}\nPlayResY: {H}\nWrapStyle: 2\nScaledBorderAndShadow: yes\n\n"
            "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
            "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
            "Alignment, MarginL, MarginR, MarginV, Encoding\n"
            f"Style: Word,{family},100,&H00{b:02X}{g:02X}{r:02X}&,&H00FFFFFF&,&H00000000&,&H00000000&,0,0,0,0,100,100,0,0,1,"
            "0,0,5,0,0,0,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    Path(path).write_text(head + "\n".join(out) + "\n", encoding="utf-8")


# ---------- composition ----------

def y_expr(bps, dur):
    """Pixel offset of the recording over time, from the plan's main breakpoints (ramps are linear)."""
    pts, prev = [], 0.0
    for b in sorted(bps, key=lambda b: b["t"]):
        y = -b.get("y", 0.0) * HALF
        r = b.get("ramp", 0.0) if y != prev else 0.0
        pts.append((b["t"], prev, y, r))
        prev = y
    expr = "0"
    for t, y0, y1, r in pts:
        seg = f"{y1:.2f}" if not r else f"({y0:.2f}+({y1 - y0:.2f})*clip((t-{t:.4f})/{r:.4f},0,1))"
        expr = f"if(lt(t,{t:.4f}),{expr},{seg})"
    return expr


def main():
    argv = sys.argv[1:]
    preview = None
    if "--preview" in argv:
        i = argv.index("--preview")
        preview = float(argv[i + 1])
        del argv[i:i + 2]
    if len(argv) != 2:
        die("usage: render_mp4.py plan.json out.mp4 [--preview SECONDS]")
    plan, out = load_json(argv[0]), Path(argv[1])
    ref = Draft(plan["reference"])
    rec = Path(plan["recording"])
    dur = probe(rec) if preview is None else min(preview, probe(rec))
    work = Path(tempfile.mkdtemp(prefix="render_mp4_"))
    own = plan.get("own_assets", False)  # our free font and synthesized sounds instead of the CapCut cache

    # split-screen ranges, as assemble_draft computes them
    bps = sorted(plan["main"], key=lambda b: b["t"])
    split = [(b["t"], bps[i + 1]["t"] if i + 1 < len(bps) else 1e9) for i, b in enumerate(bps) if b.get("y", 0)]
    punches = [p for p in punch_ins(plan, ref, probe(rec)) if p["t"] < dur]
    ws = [w for w in screen_words(plan, ref, probe(rec)) if w["t"] < dur]

    filt = [f"color=black:s={W}x{H}:r={FPS}:d={dur:.3f}[bg]",
            f"[0:v]scale={W}:{H},setsar=1" + (f",split={len(punches) + 1}[r0]" + "".join(f"[pz{i}]" for i in range(len(punches)))
                                               if punches else "[r0]")]
    # punch-ins: a zoomed copy of the recording, cut to each punch-in's frames, laid over the full-frame recording
    for i, p in enumerate(punches):
        zw, zh = round(W * p["scale"] / 2) * 2, round(H * p["scale"] / 2) * 2
        filt += [f"[pz{i}]trim=start={p['t'] - 0.5 / FPS:.4f}:end={p['end'] - 0.5 / FPS:.4f},scale={zw}:{zh},crop={W}:{H}[z{i}]",
                 f"[r{i}][z{i}]overlay=0:0:eof_action=pass[r{i + 1}]"]
    filt.append(f"[bg][r{len(punches)}]overlay=x=0:y='{y_expr(bps, dur)}':eval=frame[v0]")
    inputs, n, last = ["-i", str(rec)], 1, "v0"
    # entrance of the reference project's first clip
    a = ref.entrance()
    if plan.get("entrance", True) and a:
        if a.get("name") != ENTRANCE:
            print(f"render_mp4: warning: entrance '{a.get('name')}' is not reproduced yet; the reel starts without it",
                  file=sys.stderr)
        else:
            ent = work / "entrance.mkv"
            render_entrance(rec, ent, a.get("duration", 500000) / 1e6)
            inputs += ["-i", str(ent)]
            filt.append(f"[{last}][{n}:v]overlay=0:0:eof_action=pass[v{n}]")
            last, n = f"v{n}", n + 1
    # words on screen, then the cut-out of the person over the ones behind the head
    if ws:
        wseg, wtmpl = ref.word_template()
        wst = json.loads(ref.idx[wtmpl["text_info_resources"][0]["text_material_id"]][1]["content"])["styles"][0]
        wfont, wfam, _, wsx = pick_font(local_path(wst["font"]["path"]), own, "word")
        (work / "fonts").mkdir(exist_ok=True)
        wfam = accent_font(wfont, work / "fonts" / "word.ttf", wfam)
        sc = wtmpl["text_info_resources"][0]["attach_info"]["clip"]["scale"]
        write_words_ass(work / "words.ass", ws, work / "fonts" / "word.ttf", wfam, wst.get("size", 15), sc["x"] / sc["y"] * wsx)
        filt.append(f"[{last}]ass={work / 'words.ass'}:fontsdir={work / 'fonts'}[vw]")
        last = "vw"
        for w, f in cutouts(plan, ws, punches):
            inputs += ["-itsoffset", f"{w['t']:.4f}", "-i", str(f)]
            filt.append(f"[{last}][{n}:v]overlay=0:0:eof_action=pass:enable='between(t,{w['t']:.4f},{w['end']:.4f})'[v{n}]")
            last, n = f"v{n}", n + 1
    # overlays, in plan order (later ones on top), each from its start
    for o in plan.get("overlays", []):
        inputs += ["-itsoffset", f"{o['start']:.4f}", "-i", o["file"]]
        end = o.get("end", 1e9)
        filt.append(f"[{last}][{n}:v]overlay=0:0:eof_action=pass:enable='between(t,{o['start']:.4f},{end:.4f})'[v{n}]")
        last, n = f"v{n}", n + 1
    # captions
    cap = plan.get("captions")
    if cap:
        counts = {}
        for _, s in ref.segments("text"):
            k, m = ref.mat(s)
            if k == "text_templates":
                counts.setdefault(m.get("name"), []).append((s, m))
        name = cap.get("template") or max(counts, key=lambda x: len(counts[x]))
        seg, tmpl = counts[name][0]
        tm = ref.idx[tmpl["text_info_resources"][0]["text_material_id"]][1]
        st = json.loads(tm["content"])["styles"][0]
        src_font, family, k, sx = pick_font(local_path(st["font"]["path"]), own, "caption")
        fonts = work / "fonts"
        fonts.mkdir(exist_ok=True)
        family = accent_font(src_font, fonts / "caption.ttf", family)
        size = st.get("size", 12) * ASS_PER_CAPCUT_SIZE * k
        sh = (st.get("shadows") or [{}])[0]
        dist, ang = sh.get("distance", 0), math.radians(sh.get("angle", 0))
        y_full = cap.get("y_full")
        if y_full is None:
            y_full = (seg.get("clip") or {}).get("transform", {}).get("y", -0.56)
        style = {"family": family, "size": size,
                 "outline": (st.get("strokes") or [{"width": 0}])[0]["width"] * size,
                 "highlight": ass_colour(st["fill"]["content"]["solid"]["color"]),
                 "shadow_xy": (dist * math.cos(ang), -dist * math.sin(ang)),
                 "margin": round(W * (1 - tm.get("line_max_width", 0.82)) / 2),
                 "width": (lambda w: w and (lambda t: w(t) * sx))(text_width(fonts / "caption.ttf", size)),
                 "scale_x": sx,
                 "y_full": y_full, "y_split": cap.get("y_split", -0.71),
                 "y_ranges": cap.get("y_ranges", [])}
        words = load_json(cap["words"]) if cap.get("words") else []
        nev = write_ass(work / "captions.ass", srt_cues(cap["srt"], words, cap.get("fixes", {})), style, split)
        filt.append(f"[{last}]ass={work / 'captions.ass'}:fontsdir={fonts}[vc]")
        last = "vc"
        print(f"render_mp4: {nev} caption events in '{name}' ({family}, size {size:.0f})")
    filt.append(f"[{last}]format=yuv420p[v]")
    # audio: the recording's speech, the reel's audio files, the reference project's opening sounds
    mix = ["[0:a]aresample=48000[a0]"]
    labels = ["[a0]"]
    for au in plan.get("audio", []):
        inputs += ["-i", au["file"]]
        d = round(au.get("start", 0.0) * 1000)
        mix.append(f"[{n}:a]aresample=48000,volume={au.get('volume', 1.0)},adelay={d}:all=1[a{n}]")
        labels.append(f"[a{n}]")
        n += 1
    if plan.get("opening_sounds", True):
        for _, s in ref.segments("audio"):
            k, m = ref.mat(s)
            if k == "audios" and m.get("type") in ("sound", "music") and s["target_timerange"]["start"] < 1_000_000:
                f, start = pick_sound(local_path(m["path"]), m.get("name", ""), own, "opening sound")
                if f is None:
                    continue
                ss, sd = s["source_timerange"]["start"] / 1e6 if start is None else start, s["target_timerange"]["duration"] / 1e6
                inputs += ["-i", str(f)]
                mix.append(f"[{n}:a]aresample=48000,atrim={ss:.3f}:{ss + sd:.3f},asetpts=PTS-STARTPTS,"
                           f"volume={s.get('volume', 1.0):.4f},adelay={round(s['target_timerange']['start'] / 1000)}:all=1[a{n}]")
                labels.append(f"[a{n}]")
                n += 1
    _, ps, pm = ref.punch()
    times = sound_times(punches, ws)
    if ps is not None and times:
        f, start = pick_sound(local_path(pm["path"]), pm.get("name", ""), own, "punch-in sound")
        if f is not None:
            ss, sd = ps["source_timerange"]["start"] / US if start is None else start, ps["target_timerange"]["duration"] / US
            for t in times:
                inputs += ["-i", str(f)]
                mix.append(f"[{n}:a]aresample=48000,atrim={ss:.3f}:{ss + sd:.3f},asetpts=PTS-STARTPTS,"
                           f"volume={ps.get('volume', 1.0):.4f},adelay={round(t * 1000)}:all=1[a{n}]")
                labels.append(f"[a{n}]")
                n += 1
    mix.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=first,alimiter=limit=0.89:level=false[a]")
    graph = ";".join(filt + mix)
    ff([*inputs, "-filter_complex", graph, "-map", "[v]", "-map", "[a]", "-t", f"{dur:.3f}", "-r", str(FPS),
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(out)])
    shutil.rmtree(work, ignore_errors=True)
    print(f"render_mp4: wrote {out} ({dur:.2f} s), punch-ins {[(round(p['t'], 2), round(p['end'], 2), round(p['scale'], 2)) for p in punches]}")


if __name__ == "__main__":
    main()
