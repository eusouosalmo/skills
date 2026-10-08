---
name: animating-reel-scenes
description: Plans and renders motion scenes, split-screen scenes and transparent sticker overlays for a talking-head Reel or Short from its recording and narration SRT, as HTML with a deterministic render(t) turned into video for CapCut, timed to each spoken word. Use when the user wants to decide which parts of a recorded video become motion, build an animated scene or an overlay of stickers over their face, or render one to video (cena de motion, overlay, carimbos, tela dividida, animação do reel).
compatibility: Needs python3 with playwright (Chromium), faster-whisper and ffmpeg on PATH; scripts/setup.sh checks and installs them. Multiple-choice questions use the agent's question tool when it has one (AskUserQuestion in Claude Code).
metadata:
  status: beta
---

# Animating reel scenes

The author records a vertical talking-head video and exports its narration as SRT. This skill decides which stretches get motion, builds each one as an HTML scene, and renders it to a silent 1080x1920, 30fps file that goes on its own track in CapCut. Write anything the author reads in pt-BR.

Each rule below comes with its reason. When a case falls outside the examples, decide by the reason.

## Files

Keep every reel in one folder with this layout, so the author always finds the finished videos in the same place:

```
<reels folder>/
  estilo.md        # the author's editing style, shared by every reel (see "Style file")
  <reel folder>/
    cenas/         # one HTML per scene, named like its export: 01-problema-llm.html
    stills/        # check frames, one subfolder per scene, plus backdrop.png
    exports/       # only what goes to CapCut: NN-name.mp4 / .mov, and 00-sfx.wav
    words.json     # every spoken word with its time (step 2)
    timeline.md    # one row per export with start and end in HH:MM:SS:FF, then suggestions for the edit
```

Number scenes and overlays by their order on the timeline (`01-`, `02-`, ...) so they import into CapCut in order. Update `timeline.md` whenever a timecode or file changes.

## Setup

Before the first still, run `bash scripts/setup.sh`. It checks python3, playwright and its Chromium, faster-whisper and ffmpeg, and prints the install command for whatever is missing on this OS. Installing is the author's call: show them the commands, or have them run `bash scripts/setup.sh --install`, which asks before each one (some need sudo). Run each script with the python the setup reports for it.

## Asking the author

Every question to the author, at the start and at each gate, is multiple choice: the recommended option first and marked as such, two to four options, and room for a free answer. Use the agent's question tool when it has one (AskUserQuestion in Claude Code); otherwise write the options as a numbered list. A choice answered in one click keeps the author deciding instead of writing, and the recommended default lets them move fast when they agree.

When the author asks for something a rule here advises against (a whole sentence typed over the caption, a fade), build what they asked, say which rule it bends and why, and offer the rule's version as the recommended option. The request is theirs to make, and the reason is what lets them decide; a silent compromise between the two gives them neither.

## Style file

`estilo.md` holds what this author wants from an edit, as patterns with their reasons: "stickers carry one spoken word, because a second copy of the caption competes with the face", not "the pyramid scene had three labels". Read it before planning; it wins over this skill's defaults wherever they differ, because it is this author's taste. Keep it out of public repositories.

- **No style file yet:** offer to start one from two to four reels the author likes. For each, read frames every 2 s (`ffmpeg -i ref.mp4 -vf fps=1/2,scale=270:480 frames/f_%03d.png`) and its words (`scripts/transcribe.py ref.mp4`), then write down what repeats: formats, text on screen, rhythm, sound, transitions.
- **After every verdict** (step 6): add or adjust the pattern behind it, with the reason and the date.

## 1. Interview

Find out what the plan depends on, asking only what the folder does not already answer:

1. **Recording:** the video file of the take. Word timing, framing and split screen all read it.
2. **Format:** where each kind of stretch goes (see step 2), with "mixed, by stretch" as the recommended default.
3. **Style and look:** `estilo.md` and the design system (tokens, components, video and motion guidelines). When there is no design system, ask the author to bring one (exported files, or pulled from Claude Design with `/design-sync`); without one, go on with plain styling and let the author adjust as the scenes come out.
4. **References:** reels the author wants this one to resemble, when there is no style file yet.

The design system's guidelines are the source of truth for the look: safe margins, stage, sticker entrance, cuts, colour by role, typing pace. One exception: captions. The reel's captions go over the whole video in CapCut, so a scene carries no caption strip of its own and keeps the caption zone free, even when the design system has a caption component. Two captions on screen at once read as a mistake.

Done when you have the recording (or the author said there is none), the format default, and the paths of the style file and design system (or the author said there are none).

## 2. Plan the scenes

Time every word first: `python scripts/transcribe.py recording.mp4 --srt narration.srt -o words.json`. The SRT only marks where each phrase starts and ends; Whisper measures each word in the audio, so a sticker lands on the frame its word is said instead of a guess within the phrase. Text comes from the SRT, which the author corrected, and only the times from Whisper, which mishears names. Without a recording, estimate within each cue and tell the author the timing is approximate.

Go through the speech by stretch of meaning, not by cue (auto-transcribed cues split mid-phrase). Give each stretch one destination:

- **Face** for the hook, introductions, opinions and transitions. These carry the author's judgement or presence, which a built scene would only delay. The hook especially: the viewer decides to stay in the first seconds, looking at the person.
- **Sticker overlay** for caveats, the CTA and a term to keep. The face stays on screen and a short sticker marks the key words as each sentence lands. A run of caveats is one overlay file.
- **Full-screen scene** when the viewer understands faster by seeing than by hearing and the drawing needs the whole frame: a sequence of steps, a contrast between two outputs, a quantity, code.
- **Split screen** (scene on top, face below) when the explanation is long and both the drawing and the face matter: the viewer follows the diagram without losing the person.
- **Source shot**, a kind of full-screen scene: the page of the primary source with the cited sentence highlighted as it is said, when the claim carries the point and showing where it comes from is the proof.

The face is the default and every other destination the exception, because the person talking is what holds trust and attention in a talking-head video. One concept per scene: split when two parts ask for different reading paces. In a reel about a sorting algorithm, the quick list of where it is used and the slow step-by-step of a swap are two scenes. Scenes need not touch each other: face time between them is fine.

Then mark, from `words.json`:

- **Sound effects:** the moments a sound helps land a beat (a sticker stamp, a check, a cut to a full scene). Few and soft, like the stickers: a sound on every event turns into noise.
- **Suggestions for the edit:** cuts the author makes in CapCut on the recording itself (punch-in zoom, black and white for an aside), with the time and the reason. Transitions the design system forbids (wipes, glitches) only when `estilo.md` allows them.

Write each scene and overlay with its number, name, destination, reason and start and end in CapCut timecode `HH:MM:SS:FF` at 30fps into `timeline.md` (`python3 scripts/timecode.py --srt narration.srt` converts cue times). Inside a scene, `t = absolute time - scene start`.

Gate: show the plan and ask whether to go ahead, with options (recommended first): build as planned; adjust a named scene; change the format mix; redo the plan. Wait for the answer: a plan fixed here costs no render.

Done when every stretch has a destination with its reason, every scene and overlay has its row in `timeline.md`, and the author approved the plan.

## 3. Get the assets

Before building a scene, list what it shows and decide where each piece comes from by the job it does on screen:

| Job on screen | Where it comes from | Why |
|---|---|---|
| **Proof**: shows that a claim is true. Whenever the speech says something happens (it runs, it plays, it beats), the proof is footage of it happening | Ask the author. | A stand-in, drawn or found elsewhere, changes what is being proved, and an illustration that looks like real output reads as proof. |
| **Fact**: a number, date or name stated on screen | Open the primary public source itself (the company's site or announcement, the paper, the official docs) and give the author the URL. When you cannot reach it, say the fact is unchecked; coverage that disagrees does not make the speech wrong. When the fact carries the point, show the source itself as a source shot. | The screen must say what the source says, and coverage rounds and misquotes; the author checks before posting. |
| **Illustration** in the design system's style (character, icon, diagram) | Build it, or write an image prompt for the author to run (solid magenta background, for chroma key into a transparent sprite). | It has to match the design system, which stock images do not. |
| **Third-party material** (game or film footage, a book cover, a brand's logo) | Ask the author if they have it and can use it, and say whose rights it carries. | Someone else holds the rights, and the file stays out of any public repo. |
| **A real person** (photo, likeness) | Ask the author. Never generate one. | Their image belongs to them. |

Example from another subject: in a reel about a database benchmark, the author's own run is proof (ask), the vendor's published latency is a fact (look up and cite), the database's logo is third-party (ask), and a cartoon server is an illustration (build).

One sentence can carry two jobs. A number about something running ("it answers in 200 ms", "it does 10 a second") is a fact to check and an event to show: look the number up and ask for the footage of it running. And footage of a product running inside someone else's game, app or site is proof and third-party material at once: ask for it once, naming whose rights it carries.

Ask before building. While a proof or third-party asset is pending, build the rest and leave its slot as a visible placeholder labelled with what goes there.

Also ask for a screenshot of the edit in CapCut at a moment with the face and the caption on screen, saved as `stills/backdrop.png`. It shows what a raw frame does not: where the caption sits, how big it is and how it already highlights words, so stickers avoid both and do not repeat its highlight. Then read frames of the recording every 2 s (`ffmpeg -i recording.mp4 -vf fps=1/2,scale=270:480 stills/frames/f_%03d.png`): the head moves between takes, so check its position over each overlay's stretch, and note gestures worth syncing to.

Done when every piece on screen has its source: asked for (the question written to the author), looked up (with the URL), or built.

## 4. Build the scene

One HTML file per scene with a global `render(t)` that sets every element from `t` alone, so a still and a video frame at the same `t` match. Take entrance times from `words.json`. Hide elements with `display:none`, so a hidden element takes no layout space. Split screens, source shots and the sound track have their own layout and scripts: read [references/formats.md](references/formats.md) when the plan has any of them.

Words on screen. The caption already writes the speech out, so a sticker earns its place by marking, not by repeating:

- **What to stamp:** the term the viewer has to keep (a name, a number, the claim a caveat makes), not the reasoning around it. Highlights help people remember far more than they help them understand.
- **How often:** rarely. One sticker per caveat or CTA, one on screen at a time. A highlight only stands out against a background with no other highlights; marking everything works like marking nothing.
- **Which words:** one to three, taken from what the author says, entering on the frame the word is spoken, with the stamp entrance and then still. A sticker in other words than the caption reads as a second message.
- **Never a whole spoken sentence** in an overlay: next to the caption it is a second written copy of the speech, and on-screen text identical to the narration hurts learning.
- **A sentence in a motion scene** (no face, the caption still on): close to the speech but slightly shortened. Reworded a little beats verbatim; reworded heavily loses as much as verbatim.

Example from another subject: in a reel about password managers, the caveat "mas ele não te protege de phishing" gets one sticker, "phishing", stamped as the word is said.

Overlays: `html, body` transparent (drop any background the design system sets). The viewer watches the author's face and reads the captions, so stickers go in the free area of the recording frame, between the top safe margin and the top of the head in the usual chest-up framing, never over the face or the caption zone.

Done when the scene has a `render(t)` covering its whole duration and every sticker's words pass the rules above.

## 5. Check stills, then render

1. `python3 scripts/render.py stills cenas/NN-name.html 1.0 4.2 ... --backdrop stills/backdrop.png --out stills/NN-name` writes each still alone and composited over the recording frame. Pick times at every entrance and at the densest moment.
2. Look at every still: inside the safe margins, nothing over the face or the caption zone, text fits its sticker. Fix and repeat.
3. Gate: show the composited stills and ask, with options (recommended first): render; adjust a named still; back to the plan. Render only after the author approves, also when the request asks for the finished file or you would call the render a draft: placement and wording are fixed on stills in seconds, while every change after a render costs a new render.
4. Render:
   - overlay: `python3 scripts/render.py video cenas/NN-name.html DURATION exports/NN-name.mov --alpha`, which writes QuickTime Animation (qtrle), the alpha format that kept its transparency in CapCut. Deliver only this file: a VP9 `.webm` with alpha came out black there, and ProRes 4444 runs to hundreds of MB. Ask the author to test the `.mov` in CapCut before the next scene.
   - full scene: `python3 scripts/render.py video cenas/NN-name.html DURATION exports/NN-name.mp4`.
   - split screen and sound track: as in [references/formats.md](references/formats.md).

Done when every file is in `exports/`, its row in `timeline.md` has the start and end timecode, and the author has the paths.

## 6. Verdict

Ask the author for a verdict on the delivered reel, with options (recommended first): approved; approved with changes (which); redo a named scene. Turn every reason they give into a pattern in `estilo.md`, written as the pattern and its why, with an example from another subject when the case alone would not show it.

Done when the verdict is recorded and `estilo.md` reflects it.
