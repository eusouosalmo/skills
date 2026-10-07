---
name: animating-reel-scenes
description: Plans and renders motion scenes and transparent sticker overlays for a talking-head Reel or Short from its narration SRT, as HTML with a deterministic render(t) turned into video for CapCut. Use when the user wants to decide which parts of a recorded video become motion, build an animated scene or an overlay of stickers over their face, or render one to video (cena de motion, overlay, carimbos, animação do reel).
compatibility: Needs python3 with playwright (Chromium) and ffmpeg on PATH; scripts/setup.sh checks and installs them.
metadata:
  status: beta
---

# Animating reel scenes

The author records a vertical talking-head video and exports its narration as SRT. This skill decides which stretches get motion, builds each one as an HTML scene, and renders it to a silent 1080x1920, 30fps file that goes on its own track in CapCut. Write anything the author reads in pt-BR.

Each rule below comes with its reason. When a case falls outside the examples, decide by the reason.

## Files

Keep every reel in one folder with this layout, so the author always finds the finished videos in the same place:

```
<reel folder>/
  cenas/       # one HTML per scene, named like its export: 01-problema-llm.html
  stills/      # check frames, one subfolder per scene: stills/01-problema-llm/
  exports/     # only the finished videos that go to CapCut
  timeline.md  # file, start and end in HH:MM:SS:FF, one row per export
```

Number scenes and overlays by their order on the timeline (`01-`, `02-`, ...) so they import into CapCut in order. `timeline.md` holds the table of where each export goes; update it whenever a timecode or file changes.

## Setup

Before the first still, run `bash scripts/setup.sh`. It checks python3, the playwright package, its Chromium and ffmpeg, and prints the install command for whatever is missing on this OS. Installing is the author's call: show them the commands, or have them run `bash scripts/setup.sh --install`, which asks before each one (some need sudo). If it says playwright lives in its venv, run the scripts with that venv's python.

## 1. Read the design system

Look for the author's design system in the project (tokens, components, video and motion guidelines). When there is none, ask the author to bring it: exported files, or pulled from Claude Design with `/design-sync` if they have it. Without one, go on with plain styling and let the author adjust as the scenes come out.

Its guidelines are the source of truth for the look: safe margins, stage, sticker entrance, cuts, colour by role, typing pace. Follow them as written, with one exception: captions. The reel's captions go over the whole video in CapCut, so a scene carries no caption strip of its own and keeps the caption zone free, even when the design system has a caption component. Two captions on screen at once read as a mistake.

Done when you know where the tokens, components and video guidelines are, or the author said there are none.

## 2. Plan the scenes

Go through the SRT by stretch of meaning, not by cue (auto-transcribed cues split mid-phrase). Give each stretch one destination:

- **Motion scene** when the viewer understands faster by seeing than by hearing: a sequence of steps, a contrast between two outputs, a quantity, code. The face is the default and motion the exception, because the person talking is what holds trust and attention in a talking-head video.
- **Face** for the hook, introductions, opinions and transitions. These carry the author's judgement or presence, which a built scene would only delay. The hook especially: the viewer decides to stay in the first seconds, looking at the person.
- **Sticker overlay** for caveats and the CTA. They are the author's judgement too, so the face stays on screen and a short sticker only marks the key words as each sentence lands. A run of caveats is one overlay file.

One concept per scene: split when two parts ask for different reading paces. In a reel about a sorting algorithm, the quick list of where it is used and the slow step-by-step of a swap are two scenes. Scenes need not touch each other: face time between them is fine.

Give every scene and overlay its start and end in CapCut timecode `HH:MM:SS:FF` at 30fps, the format the CapCut timeline shows: `python3 scripts/timecode.py --srt narration.srt` converts every cue. Inside the scene, `t = absolute time - scene start`.

Done when every stretch of the SRT has a destination with its reason, and every scene and overlay has a number, a name and a start and end timecode in `timeline.md`.

## 3. Get the assets

Before building a scene, list what it shows and decide where each piece comes from by the job it does on screen:

| Job on screen | Where it comes from | Why |
|---|---|---|
| **Proof**: shows that a claim is true. Whenever the speech says something happens (it runs, it plays, it beats), the proof is footage of it happening | Ask the author. | A stand-in, drawn or found elsewhere, changes what is being proved, and an illustration that looks like real output reads as proof. |
| **Fact**: a number, date or name stated on screen | Open the primary public source itself (the company's site or announcement, the paper, the official docs) and give the author the URL. When you cannot reach it, say the fact is unchecked; coverage that disagrees does not make the speech wrong. | The screen must say what the source says, and coverage rounds and misquotes; the author checks before posting. |
| **Illustration** in the design system's style (character, icon, diagram) | Build it, or write an image prompt for the author to run (solid magenta background, for chroma key into a transparent sprite). | It has to match the design system, which stock images do not. |
| **Third-party material** (game or film footage, a book cover, a brand's logo) | Ask the author if they have it and can use it, and say whose rights it carries. | Someone else holds the rights, and the file stays out of any public repo. |
| **A real person** (photo, likeness) | Ask the author. Never generate one. | Their image belongs to them. |

Example from another subject: in a reel about a database benchmark, the author's own run is proof (ask), the vendor's published latency is a fact (look up and cite), the database's logo is third-party (ask), and a cartoon server is an illustration (build).

One sentence can carry two jobs. A number about something running ("it answers in 200 ms", "it does 10 a second") is a fact to check and an event to show: look the number up and ask for the footage of it running. And footage of a product running inside someone else's game, app or site is proof and third-party material at once: ask for it once, naming whose rights it carries.

Ask before building. While a proof or third-party asset is pending, build the rest and leave its slot as a visible placeholder labelled with what goes there.

Also ask for a screenshot of the edit in CapCut at a moment with the face and the caption on screen, saved as `stills/backdrop.png`. It shows what a raw frame does not: the real framing, and where the caption sits, how big it is and how it already highlights words, so stickers avoid both and do not repeat its highlight. Without one, a frame of the recording still gives the framing: `ffmpeg -ss 105 -i recording.mp4 -frames:v 1 stills/backdrop.png`.

Done when every piece on screen has its source: asked for (the question written to the author), looked up (with the URL), or built.

## 4. Build the scene

One HTML file per scene with a global `render(t)` that sets every element from `t` alone, so a still and a video frame at the same `t` match. Hide elements with `display:none`, so a hidden element takes no layout space.

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
3. Show the composited stills to the author and stop. Render only after the author approves them, also when the request asks for the finished file or you would call the render a draft: placement and wording are fixed on stills in seconds, while every change after a render costs a new render.
4. Render:
   - overlay: `python3 scripts/render.py video cenas/NN-name.html DURATION exports/NN-name.mov --alpha`, which writes QuickTime Animation (qtrle), the alpha format that kept its transparency in CapCut. Deliver only this file: a VP9 `.webm` with alpha came out black there, and ProRes 4444 runs to hundreds of MB. Ask the author to test the `.mov` in CapCut before the next scene.
   - full scene: `python3 scripts/render.py video cenas/NN-name.html DURATION exports/NN-name.mp4`.

Done when the file is in `exports/`, its row in `timeline.md` has the start and end timecode, and the author has both paths.
