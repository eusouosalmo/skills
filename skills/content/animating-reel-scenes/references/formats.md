# Formats with their own layout

Read when the plan has a split screen, a source shot or sound effects.

## Split screen

The scene on top, the author's face below, for the length of the stretch.

1. Build the scene at 1080x1920 as usual, with everything in the top half (y 250 to 940): the top safe margin still applies, and the bottom half will be replaced. Keep the scene's own drawing out of y 940 to 960, so the seam stays clean.
2. Render it opaque: `python3 scripts/render.py video cenas/NN-name.html DURATION exports/NN-name-top.mp4`.
3. Pick the face crop from the recording frames of that stretch: the 960 px tall band that starts a little above the head (`--face-y`, usually 300 to 500 in a chest-up framing). The caption then falls on the author's chest, as in the full-face shots.
4. Compose: `python3 scripts/split.py exports/NN-name-top.mp4 recording.mp4 --start <scene start in s> --face-y <y> -o exports/NN-name.mp4`, then delete the `-top` file. The export is silent and covers the recording for that stretch; the speech stays on the recording's audio.

Check one still of the composed file before handing it over: the face fills the bottom half and the mouth sits above the caption.

## Source shot

The primary source of a fact, on screen, with the cited sentence highlighted as it is said.

1. `python3 scripts/source_shot.py "<url>" "<exact sentence from the page>" -o cenas/assets/NN-fonte` writes the page crop (`.png`, 1080 px wide, text at double size) and the sentence's boxes (`.json`, one per line it wraps to). The sentence must be copied from the page as written.
2. In the scene, show the image inside the stage with the page's URL in small mono text on top (the viewer sees where it comes from), and grow a highlight (the design system's yellow) over each box, line by line, from the time the author starts saying it in `words.json`.
3. Credit stays on screen the whole shot. The page is someone else's text: quote one sentence, never a whole page, and only to support what is said.

## Sound effects

One audio file for the whole reel, so the author drops it once at 00:00:00:00.

1. List the events from the plan in `cenas/sfx.json`: `[{"t": 12.31, "kind": "pop"}, ...]`, with `t` on the reel's clock from `words.json`. Kinds: `pop` (sticker stamp), `tick` (highlight or typed word), `whoosh` (cut to a full-screen scene), `ding` (a check or a right answer).
2. `python3 scripts/sfx.py cenas/sfx.json exports/00-sfx.wav --duration <reel length in s>`. The sounds are synthesised, so there is no sample to license.
3. Add the row to `timeline.md` (start 00:00:00:00) and tell the author to set its volume under the speech in CapCut.
