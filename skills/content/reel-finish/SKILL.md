---
name: reel-finish
description: Finishes a talking-head Reel or Short from its cut, scenes, sfx and captions, either as a CapCut desktop project ready to open or as the final mp4 rendered without CapCut, in the editing style of one of the author's own CapCut projects (entrance, opening sounds, punch-ins and words on screen with their sound, caption template, split-screen keyframes and divider). Use when the user wants a recorded reel put together or finished (montar no capcut, finalizar o reel, vídeo final sem capcut, mp4 pronto pra postar).
compatibility: The CapCut output is confirmed on CapCut desktop 9.6 for Windows, written from WSL. Needs Python 3.8+, ffmpeg (with libass) and ffprobe; the mp4 also needs numpy and fontTools, and words behind the head need numpy, Pillow and mediapipe in both outputs (python3 -m venv .venv && .venv/bin/pip install numpy fonttools pillow mediapipe; the segmentation model downloads once into ~/.cache/reel-finish). Without the CapCut cache, the mp4 downloads its stand-in fonts once from Google Fonts into the same folder. Multiple-choice questions use the agent's question tool when it has one (AskUserQuestion in Claude Code).
metadata:
  status: draft
  internal: true
---

# Finishing reels

The author records a reel, cuts it (the `reel-cut` skill), captions it, and gets scenes from the `reel-motion` skill: a reel folder with the cut, `legenda.srt`, `words.json`, `timeline.md` and `exports/` (overlays `.mov` with alpha, `00-sfx.wav`). This skill turns that folder into the finished reel, with the editing style the author already uses in their own CapCut projects. Write every message to the author in pt-BR.

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
- its most used caption template, with font, colour and word-by-word highlight;
- its punch-ins: short clips of the main track zoomed in with a hard cut, and the library sound on their first frame;
- its words on screen: a text template carrying a text effect, other than the caption template, behind the head.

From the reference project copy style only, never the properties of its media: its video once carried `has_sound_separated` (the author had extracted the audio there), and the speech went silent in the new project. `scripts/assemble_draft.py` resets those fields; a hand-written project has to do the same.

Done when you know the reference project and it has an entrance, opening sounds and a caption template (say which one is missing, if any).

## 3. The plan

Read `timeline.md` whole and write `plan.json` next to the reel (fields in the docstring of `scripts/assemble_draft.py`; both outputs read the same plan). Times come from `timeline.md` in `HH:MM:SS:FF` at 30 fps; convert each with frames / 30.

- **recording:** the clean cut. Check one frame: when it already has captions burned in, they show twice and slide off the frame in the split screen; ask for the version without captions.
- **main:** one breakpoint per change of framing. Split-screen entry: `y` that moves the face to the lower half, with a `ramp` of 0.4 s at the timecode the timeline gives; exit: `y` 0 with a ramp ending when the panel leaves; a cut to a close inside the split keeps the split `y`. CapCut's `y` unit is half the frame height (960 px), downwards negative: 380 px down is -0.396. Take the value from `timeline.md` ("desce ~380 px") or from the author's split-screen project.
- **overlays:** each export at its own timecode from the exports table, never all at 00:00 unless the table says so.
- **divider:** every split-screen range gets the divider the author chose, a black line with a hard shadow drawn from the centre in 0.4 s with the entry keyframe, so the panel and the footage do not meet in a raw seam. Render it with `scripts/render_divider.sh <reel>/exports/NN-divisao.mov <seconds of the split range>` and add it as an overlay starting at the entry, `own_track: true`.
- **audio:** `00-sfx.wav` at 0.
- **punch_ins:** always, as the reference project's dynamic, each with its `t`, `end` and the `word` it lands on. The scripts take the scale and the sound from the reference project and refuse a punch-in that breaks the rules they can check.
  - Only where the face fills the frame in a medium shot: after the entrance, never in a split-screen range or its keyframe, never on a shot that is already a close-up. In a split screen the panel carries the rhythm, and a sudden zoom on the face pulls the eye away from the diagram the speech is explaining; on a close-up, the zoom crops the face to the eyes. A reel in split screen almost all the way through gets punch-ins only in its full-frame stretches, usually the hook; that is the right result, not a gap to fill.
  - On a word that carries the sentence (a name, a number, the claim), from its start in `words.json` to the end of the word or its short phrase, 0.6 to 1.0 s, a few seconds apart. A zoom on a filler word marks nothing, and back-to-back zooms stop reading as emphasis.
  - When `timeline.md` suggests a punch-in, take its time and scale: the overlay of that stretch was placed for that framing (a photo where a finger points stays under the finger only at the scale the timeline gives).
  - Otherwise look at one frame of the stretch at the punch-in scale: the zoomed head, hair included, must stay clear of every overlay. When it would touch one, lower the scale only as far as it takes (the author prefers a smaller punch-in with the head free to the reference's scale with hair under a print).
  - The micro-interaction sound is the punch-in's own sound, added by the scripts. Add no library sound over the panel: `00-sfx.wav` already gives each panel event the sound of its material.
- **words:** always, with the punch-ins, each with its `t`, `end` and `text`. The scripts take the template, the position above the head, the size, the click and the cut-out from the reference project, and refuse a word outside a full-frame stretch.
  - In the same stretches as the punch-ins, in the band above the head. While a scene overlay fills that band across (a print, a card), the overlay already marks the idea and the word stays out: over it the word hides the proof the hook shows, and below the chin it lands on the hands. A small sticker at one side does not fill the band: the word goes in, and the sticker stays on top of it. A reel whose full-frame stretches all have the band filled gets no word; say so in the handover.
  - The words of what the sentence is about: a name, a number, the claim. Never a function word ("nem", "o", "que"): alone on screen it marks nothing, and the author picked the name over "NEM" in the same stretch. A photo of the same person on screen does not replace the word: the author kept "MARK" and "ZUCKERBERG" with his photo up. One word on screen at a time, each from its start in `words.json` to the start of the next word shown or the end of its phrase. A name of two words shows as two flashes ("MARK", then "ZUCKERBERG"), as the reference shows "UMA" and then "FRASE"; a word shorter than the spoken word is fine. It may repeat the caption, as in the author's reference reel; inside a scene the stamp rule of the scenes still holds.
  - Behind the head by default: the scripts cut the person out of the recording into `exports/recorte-*.mov` and lay it over the word, so the hair covers the letters as in the reference. A word on a punch-in may go centred and larger (`"y": 0`, `"scale": 1.98` in the reference), over the face, with `"behind": false`.
  - The scripts shrink a word that would run past x 110 or 970, where Instagram crops the sides; a long word comes out small, so prefer a short one.
- **captions:** the SRT, the word timing from `words.json`, and every caption error `timeline.md` points out in `fixes`. In a reel with a split screen every caption sits at `y_split` (-0.71, on the chest under the panel), the hook and the close included, as in the author's approved reels; a reel without one keeps the reference project's height. Where the panel grows to fill the frame, the caption at `y_split` lands on the drawing: list each full-screen range in `y_ranges` (`[start, end, y]`) with a height in the band the scene leaves free (-0.71 when the scene keeps y 1480 down clear), and a cue whose middle falls in a range takes that height (2026-10-25, reel da urna: the author saw the caption over the full-screen animations). The scripts apply this.

Files you generate go in the reel's `exports/`, on the Windows drive, where CapCut can read them. Both outputs come from this plan through the skill's own scripts, so the CapCut project and the mp4 carry the same edit; never edit a copy of a script to add something the plan lacks.

Done when every row of the exports table, every split range, every caption fix and every punch-in suggestion in `timeline.md` is in the plan, and every full-frame medium-shot stretch has been considered for a punch-in and a word.

## 4a. CapCut project: write and check

Write only into an empty project the author created in the CapCut app. The app writes the ids, the `Timelines/<id>/` copy and the metadata a project needs; writing into such a project is what is confirmed to open on 9.6, and a folder made by hand is not. When the request names no empty project, or the named one does not exist in the drafts folder, ask the author to create one in the app with the reel's name and close CapCut, then stop until they confirm. A project of the same reel that already exists is the author's edit: leave it as it is.

CapCut must stay closed while you write: it saves its own state on close and erases the write. The script checks with `tasklist.exe` and refuses while CapCut runs; when it refuses, ask the author to close it.

Run `python3 scripts/assemble_draft.py plan.json --dry-run`, compare the tracks with the plan, then run it without `--dry-run`. The script backs the project up into `backup_dir` (outside the drafts folder, where CapCut would list the copy as a project), writes the root `draft_content.json` and every `Timelines/*/draft_content.json` (CapCut 9.x reads the copy), updates `draft_meta_info.json`, and validates references, ids and overlaps. It refuses a project that already has clips; pass `--force` only after the author agrees to replace it.

Done when the script prints `written:` with the tracks you planned.

## 4b. Final mp4: render and check

Run `scripts/render_mp4.py plan.json <reel>/exports/<reel name> - final.mp4 --preview 8` under the memory cap, with a Python that has numpy and fontTools. Look at frames 0 to 15 (the entrance: the frame moves in with a directional blur and mirrored edges, with no black bars; the one dark wedge in the top-right corner of frame 0 is in CapCut's own export too, so leave it), at the frames on each side of a punch-in's cut, at one frame of each word (letters behind the hair, nothing cut off at the sides), and at a caption that breaks into two lines, then render the whole reel without `--preview`. The script reproduces CapCut's own pieces from the reference project and the local CapCut cache:

- the entrance "Balançar para cima e para a direita", frame by frame from its shader (another entrance is reported and left out);
- the caption template: its font with the pt-BR accented capitals added when the font lacks them, the size, colour, stroke and shadow, pages of up to three words, lines broken where CapCut breaks them;
- the opening sounds, from the cache files the reference project uses;
- the punch-ins, as hard cuts around the frame centre, with the reference project's punch-in sound;
- the words in the reference's word template: its font, the effect's yellow and hard shadow, the template's size and position, with the person cut out over them.

When the cache lacks one of these files (another machine, a cleared cache), the script takes our own version from `scripts/own_assets.py` and prints which: a free font sized to the CapCut font's capitals and line width (Lexend for the caption, Kanit for the words) and a synthesized sound (camera click, reversed whoosh, mouse click). Render on, and name each stand-in in the handover, so the author knows what to compare. `"own_assets": true` in the plan uses ours even with the cache, for a side-by-side with CapCut's.

Done when the mp4 has the reel's length at 1080x1920 and 30 fps, and the frames you looked at match the plan.

## 5. Hand over

Tell the author where the output is, what is in it (each track, or each layer of the mp4), what to check (the entrance and opening sounds, the speech audible, the split-screen keyframe, captions in the template), and each punch-in and each word on screen with its time, so they can drop one (or why no word went in), and what stayed for them (the impact sound the timeline leaves to them). For a CapCut project, say where the backup is and ask them to keep CapCut closed if a fix is needed.
