# Formats with their own layout

Read when the plan has a split screen, a source shot or sound effects.

## Split screen

The scene on top, the author's face below, for the length of the stretch.

1. Build the scene at 1080x1920 with the drawing in the top half; the bottom half belongs to the face. Centre the drawing in the 1080x960 panel, with equal space above and below and at least 170 px at the top: in a split the panel is the frame the eye reads, so a drawing pushed down by the full-frame top margin (250 px) looks misaligned. That 250 px figure is Meta's Reels ad guidance (about 14%); organic reels carry a smaller top bar. `assets/center-panel.js` does the centring; scenes that repeat one drawing share its box so nothing jumps at the cut.
2. **Default delivery, top panel only:** make the page transparent and put the background on a 1080x960 panel behind the drawing, then render a copy of the scene as `NN-name-topo.html`:

   ```css
   body { background: transparent !important; background-image: none !important; }
   .panel { position: absolute; left: 0; top: 0; width: 1080px; height: 960px; }  /* <div class="panel"> first in body, with the design system's background class */
   ```

   Render with `python3 scripts/render.py video cenas/NN-name-topo.html DURATION exports/NN-name-topo.mov --alpha`. In CapCut the author puts it over the recording and moves the video down until the face fills the bottom half, then places the caption. They frame their own face and caption better than a fixed crop, and the take keeps its own caption track.
3. **Composed delivery, only from a recording without burned-in captions:** render the scene opaque, pick `--face-y` from the frames of that stretch so the mouth sits above where the caption goes (start at the forehead when head-to-mouth is taller than the space left), and run `python3 scripts/split.py exports/NN-name-top.mp4 recording.mp4 --start <s> --face-y <y> -o exports/NN-name.mp4`. A crop of a captioned export carries the caption down into the platform's bottom bar, and shows it twice when the caption is also a live track.

Check one still before handing over: the drawing fits the top half, and in a composed file the face fills the bottom half with the mouth clear of the caption.

## Source shot

The primary source of a fact, on screen, with the cited sentence highlighted as it is said.

1. `python3 scripts/source_shot.py "<url>" "<exact sentence from the page>" -o cenas/assets/NN-fonte` writes the page crop (`.png`, 1080 px wide, text at double size) and the sentence's boxes (`.json`, one per line it wraps to). The sentence must be copied from the page as written.
2. In the scene, show the image inside the stage with the page's URL in small mono text on top (the viewer sees where it comes from), and grow a highlight (the design system's yellow) over each box, line by line, from the time the author starts saying it in `words.json`.
3. Credit stays on screen the whole shot. The page is someone else's text: quote one sentence, never a whole page, and only to support what is said.

## Sound effects

One audio file for the whole reel, so the author drops it once at 00:00:00:00.

1. In each scene, list its sounds next to its timing table, in seconds from the scene start: `window.SFX = [{"t": 0.68, "kind": "pop"}, ...];`. Keeping them beside `T` means a retimed entrance carries its sound with it. One event per entrance, line, state change, and the scene's own in (`whoosh` at 0) and out (`out` just before it ends); a dry cut between two states of the same drawing gets a `tick`, not a sweep.
2. Pick the kind by what happens: `pop` (sticker, note, node), `thud` (a change that matters, a block replaced), `tick` (small label, typed word, step), `draw` (line traced), `whoosh` and `out` (scene in and out), `ding` (a check, a loop that closes). Lower the `gain` of an event that lands on top of another.
3. `python3 scripts/sfx.py exports/00-sfx.wav --duration <reel length in s> --scene cenas/01-name.html <start s> --scene ...`. The sounds are synthesised, so there is no sample to license, and the track peaks near -10 dB, under a voice recorded near -3 dB.
4. Mix a preview with the recording's speech (`ffmpeg -i recording.mp4 -i exports/00-sfx.wav -filter_complex "[0:a][1:a]amix=inputs=2:duration=first:normalize=0[a]" -map 0:v -map "[a]" -c:v copy previa.mp4`) and listen before handing it over. Add the row to `timeline.md` (start 00:00:00:00).
