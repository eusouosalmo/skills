---
name: finishing-reels
description: Finishes a talking-head Reel or Short from its cut, scenes, sfx and captions, either as a CapCut desktop project ready to open or as the final mp4 rendered without CapCut, in the editing style of one of the author's own CapCut projects (entrance, opening sounds, caption template, split-screen keyframes and divider). Use when the user wants a recorded reel put together or finished (montar no capcut, finalizar o reel, vídeo final sem capcut, mp4 pronto pra postar).
compatibility: The CapCut output is confirmed on CapCut desktop 9.6 for Windows, written from WSL. Needs Python 3.8+, ffmpeg (with libass) and ffprobe; the mp4 also needs numpy and fontTools (python3 -m venv .venv && .venv/bin/pip install numpy fonttools). Multiple-choice questions use the agent's question tool when it has one (AskUserQuestion in Claude Code).
metadata:
  status: draft
  internal: true
---

# Finishing reels

The author records a reel, cuts it (the `cutting-raw-takes` skill), captions it, and gets scenes from the `animating-reel-scenes` skill: a reel folder with the cut, `legenda.srt`, `words.json`, `timeline.md` and `exports/` (overlays `.mov` with alpha, `00-sfx.wav`). This skill turns that folder into the finished reel, with the editing style the author already uses in their own CapCut projects. Write every message to the author in pt-BR.

Each rule comes with its reason. When a case falls outside the examples, decide by the reason.

## 1. The output

The reel comes out in one of two forms, and both carry the same edit:

- **CapCut project:** the author opens it in CapCut, adjusts what they want and exports. Needs an empty project made in the app and CapCut closed while it is written.
- **Final mp4:** ready to post, rendered here without CapCut. The entrance, the opening sounds and the caption template are reproduced from the reference project.

When the request names one ("no capcut", "sem capcut", "mp4"), take it. Otherwise ask before any render or write, with how each one is used, recommending the CapCut project when the author wants to keep adjusting and the mp4 when they want to post right away. The author asked for both forms to stay available, and the choice changes everything after step 3.

Done when the output form is known.

## 2. The reference project

The style comes from one of the author's own CapCut projects, the **reference project**, never recreated by hand: the author already chose that entrance, those sounds and that caption template. Find it in this order: the author's style notes (the style file `timeline.md` points to), the "Referência" line of `timeline.md`, then ask, listing the projects in the drafts folder (`<user>/AppData/Local/CapCut/User Data/Projects/com.lveditor.draft/`); once answered, offer to record it in the style notes. From it the scripts take, at the same times and volumes:

- the entrance animation of its first clip (a zoom with a sway, for example);
- the opening sounds: library sounds starting in its first second (camera click at 0.0 s, reversed whoosh at 0.3 s);
- its most used caption template, with font, colour and word-by-word highlight.

From the reference project copy style only, never the properties of its media: its video once carried `has_sound_separated` (the author had extracted the audio there), and the speech went silent in the new project. `scripts/assemble_draft.py` resets those fields; a hand-written project has to do the same.

Done when you know the reference project and it has an entrance, opening sounds and a caption template (say which one is missing, if any).

## 3. The plan

Read `timeline.md` whole and write `plan.json` next to the reel (fields in the docstring of `scripts/assemble_draft.py`; both outputs read the same plan). Times come from `timeline.md` in `HH:MM:SS:FF` at 30 fps; convert each with frames / 30.

- **recording:** the clean cut. Check one frame: when it already has captions burned in, they show twice and slide off the frame in the split screen; ask for the version without captions.
- **main:** one breakpoint per change of framing. Split-screen entry: `y` that moves the face to the lower half, with a `ramp` of 0.4 s at the timecode the timeline gives; exit: `y` 0 with a ramp ending when the panel leaves; a cut to a close inside the split keeps the split `y`. CapCut's `y` unit is half the frame height (960 px), downwards negative: 380 px down is -0.396. Take the value from `timeline.md` ("desce ~380 px") or from the author's split-screen project.
- **overlays:** each export at its own timecode from the exports table, never all at 00:00 unless the table says so.
- **divider:** every split-screen range gets the divider the author chose, a black line with a hard shadow drawn from the centre in 0.4 s with the entry keyframe, so the panel and the footage do not meet in a raw seam. Render it with `scripts/render_divider.sh <reel>/exports/NN-divisao.mov <seconds of the split range>` and add it as an overlay starting at the entry, `own_track: true`.
- **audio:** `00-sfx.wav` at 0.
- **captions:** the SRT, the word timing from `words.json`, and every caption error `timeline.md` points out in `fixes`. In a reel with a split screen every caption sits at `y_split` (-0.71, on the chest under the panel), the hook and the close included, as in the author's approved reels; a reel without one keeps the reference project's height. The scripts apply this.

Files you generate go in the reel's `exports/`, on the Windows drive, where CapCut can read them.

Done when every row of the exports table, every split range and every caption fix in `timeline.md` is in the plan.

## 4a. CapCut project: write and check

Write only into an empty project the author created in the CapCut app. The app writes the ids, the `Timelines/<id>/` copy and the metadata a project needs; writing into such a project is what is confirmed to open on 9.6, and a folder made by hand is not. When the request names no empty project, or the named one does not exist in the drafts folder, ask the author to create one in the app with the reel's name and close CapCut, then stop until they confirm. A project of the same reel that already exists is the author's edit: leave it as it is.

CapCut must stay closed while you write: it saves its own state on close and erases the write. The script checks with `tasklist.exe` and refuses while CapCut runs; when it refuses, ask the author to close it.

Run `python3 scripts/assemble_draft.py plan.json --dry-run`, compare the tracks with the plan, then run it without `--dry-run`. The script backs the project up into `backup_dir` (outside the drafts folder, where CapCut would list the copy as a project), writes the root `draft_content.json` and every `Timelines/*/draft_content.json` (CapCut 9.x reads the copy), updates `draft_meta_info.json`, and validates references, ids and overlaps. It refuses a project that already has clips; pass `--force` only after the author agrees to replace it.

Done when the script prints `written:` with the tracks you planned.

## 4b. Final mp4: render and check

Run `scripts/render_mp4.py plan.json <reel>/exports/<reel name> - final.mp4 --preview 8` under the memory cap, with a Python that has numpy and fontTools. Look at frames 0 to 15 (the entrance: the frame moves in with a directional blur and mirrored edges, never black corners) and at a caption that breaks into two lines, then render the whole reel without `--preview`. The script reproduces CapCut's own pieces from the reference project and the local CapCut cache:

- the entrance "Balançar para cima e para a direita", frame by frame from its shader (another entrance is reported and left out);
- the caption template: its font with the pt-BR accented capitals added when the font lacks them, the size, colour, stroke and shadow, pages of up to three words, lines broken where CapCut breaks them;
- the opening sounds, from the cache files the reference project uses.

Done when the mp4 has the reel's length at 1080x1920 and 30 fps, and the frames you looked at match the plan.

## 5. Hand over

Tell the author where the output is, what is in it (each track, or each layer of the mp4), what to check (the entrance and opening sounds, the speech audible, the split-screen keyframe, captions in the template), and what stayed for them (the impact sound the timeline leaves to them, an optional punch-in). For a CapCut project, say where the backup is and ask them to keep CapCut closed if a fix is needed.
