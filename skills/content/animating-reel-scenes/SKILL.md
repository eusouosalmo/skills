---
name: animating-reel-scenes
description: Plans and renders motion scenes, split-screen scenes and transparent sticker overlays for a talking-head Reel or Short from its recording and narration SRT, as HTML with a deterministic render(t) turned into video for CapCut, timed to each spoken word. Use when the user wants to decide which parts of a recorded video become motion, build an animated scene or an overlay of stickers over their face, or render one to video (cena de motion, overlay, carimbos, tela dividida, animação do reel).
compatibility: Needs python3 with playwright (Chromium), faster-whisper and ffmpeg on PATH; scripts/setup.sh checks and installs them. Multiple-choice questions use the agent's question tool when it has one (AskUserQuestion in Claude Code). Searching images needs web access.
metadata:
  status: beta
---

# Animating reel scenes

The author records a vertical talking-head video and exports its narration as SRT. This skill reads what each stretch means and what the recording shows, decides which stretches get motion, builds each one as an HTML scene, and renders it to a silent 1080x1920, 30fps file that goes on its own track in CapCut. Write anything the author reads in pt-BR.

Each rule below comes with its reason. When a case falls outside the examples, decide by the reason.

## Files

Keep every reel in one folder with this layout, so the author always finds the finished videos in the same place:

```
<reels folder>/
  estilo.md        # the author's editing style, shared by every reel (see "Style file")
  <reel folder>/
    cenas/         # one HTML per scene, named like its export: 01-problema-llm.html
    assets/        # images found or received, named after what they show
    stills/        # check frames, one subfolder per scene, plus backdrop.png and the contact sheets
    exports/       # only what goes to CapCut: NN-name.mp4 / .mov, and 00-sfx.wav
    words.json     # every spoken word with its time (step 2)
    breakdown.md   # the stretches of meaning, read by the agent only (step 2)
    timeline.md    # the plan and one row per export with start and end in HH:MM:SS:FF, then suggestions for the edit and credits
```

Number scenes and overlays by their order on the timeline (`01-`, `02-`, ...) so they import into CapCut in order. Update `timeline.md` whenever a timecode or file changes.

## Setup

Before the first still, run `bash scripts/setup.sh`. It checks python3, playwright and its Chromium, faster-whisper and ffmpeg, and prints the install command for whatever is missing on this OS. Installing is the author's call: show them the commands, or have them run `bash scripts/setup.sh --install`, which asks before each one (some need sudo). Run each script with the python the setup reports for it.

## Asking the author

Every question to the author, at the start and at each gate, is multiple choice: the recommended option first and marked as such, two to four options, and room for a free answer. Use the agent's question tool when it has one (AskUserQuestion in Claude Code); otherwise write the options as a numbered list. A choice answered in one click keeps the author deciding instead of writing, and the recommended default lets them move fast when they agree.

When the author asks for something a rule here advises against (a whole sentence typed over the caption, a fade, an explanation in steps over the face), build what they asked when it can be built, say which rule it bends and why, and offer the rule's version as the recommended option. The request is theirs to make, and the reason is what lets them decide; a silent compromise between the two gives them neither.

## Style file

`estilo.md` holds what this author wants from an edit, as patterns with their reasons: "stickers carry one spoken word, because a second copy of the caption competes with the face", not "the pyramid scene had three labels". Read it before planning; it wins over this skill's defaults wherever they differ, because it is this author's taste. Taste shapes how a thing is drawn; it never swaps the hook form the script chose (step 3). Keep it out of public repositories.

- **No style file yet:** offer to start one from two to four reels the author likes. For each, read frames every 2 s (`ffmpeg -i ref.mp4 -vf fps=1/2,scale=270:480 frames/f_%03d.png`) and its words (`scripts/transcribe.py ref.mp4`), then write down what repeats: formats, text on screen, rhythm, sound, transitions.
- **After every verdict** (step 7): add or adjust the pattern behind it, with the reason and the date.

## 1. Interview

Find out what the plan depends on, asking only what the folder does not already answer:

1. **Recording:** the video file of the take. Word timing, framing, gestures and split screen all read it.
2. **Script:** the script file, when there is one. Its `Formato`, the `Forma:` of the hook visual and any `Volta à analogia:` line feed the breakdown.
3. **Screen mode** of the whole video, asked with all four as options: mixed, by stretch; split screen for the whole reel; without face (the recording's voice under scenes the whole time); full screen with the face at the turns (scenes explain, the face comes back for the hook, the turns and the close). Recommend the mode the script's format names (see [references/breakdown.md](references/breakdown.md), "Format and screen mode"), with the format as the reason; with no named format, recommend mixed, by stretch. In the reference reels the mode is part of the format: a metaphor world that fills the frame does not exist with the face on screen all the time.
4. **Style and look:** `estilo.md` and the design system (tokens, components, video and motion guidelines). When there is no design system, ask the author to bring one (exported files, or pulled from Claude Design with `/design-sync`); without one, go on with plain styling and let the author adjust as the scenes come out.
5. **References:** reels the author wants this one to resemble, when there is no style file yet.

The design system guides the look without boxing it in. Binding: palette and the role of each colour, typography, shape language (border, shadow, radius, texture), safe margins and the caption zone. Free, inside those: new kinds of element and motion beyond its tokens (curves, durations, choreography), since its repertoire of stamped cards is what made scenes look alike. One exception to the design system: captions. The reel's captions go over the whole video in CapCut, so a scene carries no caption strip of its own and keeps the caption zone free, even when the design system has a caption component. Two captions on screen at once read as a mistake.

Done when you have the recording (or the author said there is none), the script or its absence, the screen mode, and the paths of the style file and design system (or the author said there are none).

## 2. Time the words and break the speech down

Time every word first: `python scripts/transcribe.py recording.mp4 --srt narration.srt -o words.json`. The SRT only marks where each phrase starts and ends; Whisper measures each word in the audio, so a sticker lands on the frame its word is said instead of a guess within the phrase. Text comes from the SRT, which the author corrected, and only the times from Whisper, which mishears names. Without a recording, estimate within each cue and tell the author the timing is approximate.

Then read the recording as contact sheets, so a gesture of one second is not lost between frames read every 2 s:

```
ffmpeg -i recording.mp4 -vf "fps=1,scale=180:320,tile=6x5" stills/contato_%02d.png
ffmpeg -i recording.mp4 -t 3 -vf "fps=4,scale=180:320,tile=4x3" stills/contato_gancho.png
```

Each tile is one second (the hook sheet, a quarter of a second). Then write `breakdown.md`: the speech split into stretches of meaning (not cues, which split mid-phrase), each with the fields, the fixed list of intents and the searches in [references/breakdown.md](references/breakdown.md). Read it now. The breakdown is where the plan learns what each stretch means and what the take shows: a plan made from the words alone follows the spoken word instead of the idea, and misses the finger pointing at what the speech names.

Done when every spoken word belongs to a stretch, every stretch has its fields filled with an intent from the list and the frame times it cites, and every image the plan will put on screen has been searched or marked as asked.

## 3. Plan the scenes

The intent of each stretch picks its destination, following the screen mode (the table in [references/breakdown.md](references/breakdown.md)). In mixed mode the face is the default and every other destination the exception, because the person talking is what holds trust and attention in a talking-head video:

- **Face** for introductions, opinions and transitions. These carry the author's judgement or presence, which a built scene would only delay.
- **Sticker overlay** for caveats, the CTA and a term to keep. The face stays on screen and a short sticker marks the key words as each sentence lands. A run of caveats is one overlay file.
- **Image over the face** (a second overlay size) for the source, the subject or the image a gesture points at, for a few seconds with the face still on screen.
- **Full-screen scene** when the viewer understands faster by seeing than by hearing and the drawing needs the whole frame: a sequence of steps, a contrast between two outputs, a quantity, code.
- **Split screen** (scene on top, face below) when the explanation is long and both the drawing and the face matter: the viewer follows the diagram without losing the person.
- **Source shot**, a kind of full-screen scene: the page of the primary source with the cited sentence highlighted as it is said, when the claim carries the point and showing where it comes from is the proof.

**Hook.** The hook takes the visual hook form the script names in `Forma:`; without one, choose it in the breakdown from the hook's words, the format and the gestures of the take, and propose it at the gate. In a video with the face, the face stays in the frame during the hook and the form enters as the table in [references/breakdown.md](references/breakdown.md) says (overlay, or split screen from frame 0); a full-screen scene opens the video only in the without-face mode. Swap the script's form for only one of three reasons, said at the gate with the script's form among the options: the recording asks for another (a gesture with meaning, a take with no free space); the screen mode cannot hold it (use the table's variant); an asset is missing (keep the form with a labelled placeholder and offer the swap). The viewer decides to stay in the first seconds, and the form was chosen for that; falling back to the bare face by habit drops it.

**Gesture with meaning keeps the face.** A stretch whose take carries a gesture or object with meaning stays on the face (stickers clear of the hands) or goes to split screen with the gesture in the bottom half; never to a full-screen scene that hides it. A scene that repeats the gesture (steps while counting on the fingers) enters on each finger.

**Naming.** A stretch with the intent `nome` returns to the scene of the image it names, in the same destination and composition, with each spoken name as a literal label on its part. The same composition is what lets the viewer recognise the return.

**Climax.** When the breakdown marks a `clímax`, propose an impact screen at its anchor word (step 5). When it marks none, write "sem clímax" with the reason; forcing one turns the technique into a tic.

One concept per scene: split when two parts ask for different reading paces. In a reel about a sorting algorithm, the quick list of where it is used and the slow step-by-step of a swap are two scenes. Scenes need not touch each other: face time between them is fine. In the whole-video modes there is one scene file for the whole reel instead (see [references/formats.md](references/formats.md)).

Write the plan into `timeline.md`:

- **One line per scene or overlay:** number, name, destination, reason, start and end in CapCut timecode `HH:MM:SS:FF` at 30fps (`python3 scripts/timecode.py --srt narration.srt` converts cue times), what is seen, what moves and the word that triggers each entrance. Every line stands on its own, readable without the others; "idem" or "same scene" leaves the author unable to match it to its stretch. When a destination rests on the take, cite the frame (time and what it shows). Inside a scene, `t = absolute time - scene start`.
- **Density regime** for the video, and any change at a turn with its reason (step 5, "Composition").
- **Visual events:** for every scene in the without-face mode, every split-screen panel and every explanation stretch of the face-at-the-turns mode, each new state with its time, and each **rest** with its reason (step 5, "Rhythm").
- **Climax** with its stretch and reason, or "sem clímax" with the reason.
- **Sound effects:** a sound for every motion event, so what moves on screen also lands in the ear: each object that appears, each line traced, each state change, each scene or overlay coming in and going out, and its own line for the impact screen, marked as impact, with the sound left to the author. Vary the sound by the kind of event, keep it under the speech, and let `estilo.md` set the density for this author.
- **Suggestions for the edit:** cuts the author makes in CapCut on the recording itself (punch-in zoom, black and white for an aside), with the time and the reason. Transitions the design system forbids (wipes, glitches) only when `estilo.md` allows them.
- **Credits:** a section headed `## Créditos para a legenda`, one line per image or clip found that asks for credit, ready for the post caption.

Before the gate, count the intervals in the list of visual events, merging entries less than a second apart into one beat: wherever the rhythm rule applies, no stretch of more than 4 s without a new state outside a declared rest, and at least 3 events per 10 s. Fix the plan where it fails.

Gate: show the plan with the screen mode, the density regime, the hook form and its reason, the climax (or "sem clímax") and each image found with its source and licence, and ask whether to go ahead, with options (recommended first): build as planned; adjust a named scene; change the format mix; redo the plan. When one scene rests on a visual metaphor that is not obvious from its line, you may add one draft still of it. Wait for the answer: a plan fixed here costs no render.

Done when every stretch has a destination with its reason, every scene and overlay has its line in `timeline.md`, the intervals pass, and the author approved the plan.

## 4. Get the assets

Before building a scene, list what it shows and decide where each piece comes from by the job it does on screen:

| Job on screen | Where it comes from | Why |
|---|---|---|
| **Proof**: shows that a claim is true. Whenever the speech says something happens (it runs, it plays, it beats), the proof is footage of it happening | Ask the author. When the speech refers to someone else's public demonstration, offer the official video of it as an option at the gate. | A stand-in, drawn or found elsewhere, changes what is being proved, and an illustration that looks like real output reads as proof. |
| **Fact**: a number, date or name stated on screen, including the datum for whoever pauses | Open the primary public source itself (the company's site or announcement, the paper, the official docs) and give the author the URL. When you cannot reach it, say the fact is unchecked; coverage that disagrees does not make the speech wrong. When the fact carries the point, show the source itself as a source shot. Example content that only shows a shape (a ciphertext in hex, a truncated key) needs no source; the breakdown marks it as shape. | The screen must say what the source says, and coverage rounds and misquotes; the author checks before posting. |
| **Illustration** in the design system's style (character, icon, diagram) | Build it, or write an image prompt for the author to run (solid magenta background, for chroma key into a transparent sprite). | It has to match the design system, which stock images do not. |
| **The author's recording** (a screen capture of their browser or phone, frames or a stretch of the face take) | Ask the author; never recreate it. Show it inside a frame in the scene. | It is their own material, and a drawn copy reads as a fake. |
| **Third-party image** (photo of a public person the speech names, a brand's logo, a product, a page) | Search for it in the breakdown, by the rules in [references/images.md](references/images.md), with source URL, author, licence and credit line. Ask the author when nothing usable turns up, and when the reel sells something (sponsored, or a CTA for the author's product). | A licensed image found before the gate lets the author approve the real picture; the licence covers the photographer, not the person or the brand, which is why those limits stay. |
| **Third-party footage** (film, game, keynote) | Find it at its official source and give the URL and the exact span (start and end, a few seconds); the author downloads or records it. Say whose rights it carries and that film, game and music clips often trip Instagram's rights detection. | A short quoted excerpt with credit is allowed when it is not the point of the new work; downloading without the source's own download button is the author's call. |
| **A real person's likeness** | Only the found photo that identifies them, cut out at most. Never generate one, never change a face or expression. | Their image belongs to them. |

Example from another subject: in a reel about a database benchmark, the author's own run is proof (ask), the vendor's published latency is a fact (look up and cite), the database's logo is a third-party image (search the brand's own page), and a cartoon server is an illustration (build).

One sentence can carry two jobs. A number about something running ("it answers in 200 ms", "it does 10 a second") is a fact to check and an event to show: look the number up and ask for the footage of it running. And footage of a product running inside someone else's game, app or site is proof and third-party material at once: ask for it once, naming whose rights it carries.

Ask before building. While a proof or third-party asset is pending, build the rest and leave its slot as a visible placeholder labelled with what goes there.

Also ask for a screenshot of the edit in CapCut at a moment with the face and the caption on screen, saved as `stills/backdrop.png`. It shows what a raw frame does not: where the caption sits, how big it is and how it already highlights words, so stickers avoid both and do not repeat its highlight. Then check the head's position over each overlay's stretch in the contact sheets: the head moves between takes.

Done when every piece on screen has its source: asked for (the question written to the author), looked up (with the URL), found (with URL and licence), or built.

## 5. Build the scene

One HTML file per scene with a global `render(t)` that sets every element from `t` alone, so a still and a video frame at the same `t` match. Take entrance times from `words.json`. Hide elements with `display:none`, so a hidden element takes no layout space. A tweening library such as GSAP is fine inside `render(t)` when it is seeked to `t`. Split screens, the whole-video modes, source shots, the image over the face and the sound track have their own layout and scripts: read [references/formats.md](references/formats.md) when the plan has any of them.

### Words on screen

The caption already writes the speech out, so a sticker earns its place by marking, not by repeating:

- **What to stamp:** the term the viewer has to keep (a name, a number, the claim a caveat makes), not the reasoning around it. Highlights help people remember far more than they help them understand.
- **How often:** rarely. One sticker per caveat or CTA, one on screen at a time. A highlight only stands out against a background with no other highlights; marking everything works like marking nothing.
- **Which words:** one to three, taken from what the author says, entering on the frame the word is spoken, with the stamp entrance and then still. A sticker in other words than the caption reads as a second message.
- **Same meaning as the sentence:** a sticker or label, read alone, says what the sentence it marks says. A negation (não, nunca, nem, sem, nenhum) stays in its words, counted inside the one to three with any seal beside them, or in its drawing (the term struck through, a NUNCA seal). When the negation sits far from the term, it may take a compact form ("nem sempre", "sem", "zero") as long as the term is the one spoken. The viewer reads a sticker at a glance, and the "não" is the first word lost when a sentence is cut.
- **Never a whole spoken sentence** in an overlay: next to the caption it is a second written copy of the speech, and on-screen text identical to the narration hurts learning.
- **A sentence in a motion scene** (no face, the caption still on): close to the speech but slightly shortened. Reworded a little beats verbatim; reworded heavily loses as much as verbatim.

Example from another subject: in a reel about password managers, the caveat "mas ele não te protege de phishing" gets one sticker, "sem proteção contra phishing" or "phishing" struck through, stamped as the word is said.

### Choreography

What moves, in what order, and how one state becomes the next. Each pattern below carries the explanation; a scene of stamped cards swapped by dry cuts carries only the words.

- **Transform instead of cutting.** The object already on screen changes shape, grows or gains a part to become the next state; the same DOM element changes. A continuous change lets the eye follow the object from one state to the next. Dry cuts belong to stickers and overlays, and to the start of a new event.
- **Fixed stage.** One drawing stays, and each idea changes one part of it.
- **Show the process the speech names.** When the explanation depends on a process (mixing, encrypting, compressing, hashing), the pieces move as the verb says (two paints fall into a pot and swirl; the glass cracks and breaks), one change per step, each step on its word. Only the before and after are enough when the change from one to the other is obvious. When the speech states a property of the process (it cannot be undone, it loses information, it goes one way only), prove it with an attempt that fails; never draw the state the speech denies, not even with a "?" or a dashed outline. The picture seen alone says what the sentence says.
- **Trace where the path carries meaning.** A connector or arrow (its direction is the information), including the route of anything the speech sends from one place to another (a message, a packet, a drop of paint), which traces ahead of it on the verb of sending, an outline assembled part by part in the order the speech lists them (a box's border traced on its name, then each division on the word of the field it opens; draw that border as an SVG path even when the design system has a window or card component for the box, since a CSS border cannot trace), an emphasis mark over what the speech points at now (a circle, an underline or a bracket traced around the piece on the word that points at it, as in "esse campo aqui" circling the field; the same when the speech points at a place where something happens, "no caminho" bracketing the path, even when a character or icon also enters there, since the icon alone does not point): these draw themselves, and each trace ends inside the word that names it, in under 1 s. Text, icons, labels and stickers enter whole. The growing line tells the eye where to look; that is the reason, so a trace with no direction to show is only delay.
- **Settle.** Each state comes to rest before the next word that asks for movement.
- **Variety.** Each new idea gets a kind of element the scene has not used yet (a drawn object, a running number, code, a character, a chart); the same idea comes back with the same drawing, so the viewer reads the repeat as the same thing.

### Composition

Each scene sits in one of two **density regimes**, chosen for the video and changed only at a turn with the reason in the plan:

- **One object:** one large piece at the centre that transforms. The main piece spans at least 2/3 of the stage's width, centred, in every state, the ones in the middle of a transformation included; empty space around it is fine, an empty half from pushing it aside is not. Fits a mechanism or analogy that transforms.
- **Zoned panel:** each kind of information in a fixed place, the zones covering the stage edge to edge in both directions, from the top margin down to the caption zone, none empty without a reason (emptying at a turn is one). Size the zones to the stage first and the pieces to their zone, so a band of empty stage under the diagram never appears. Fits a process in steps or data that accumulates.

The stage is the frame minus the safe margins and the caption zone, or the 1080x960 top panel in a split screen. Small loose pieces in the middle ground are what both regimes avoid: they leave the frame half empty and read as decoration. Stickers in an overlay are exempt; they are small on purpose.

**Naming scenes and data for whoever pauses.** In the scene of a `nome` stretch, each spoken name labels the part it names, never only as loose text, a window or an icon apart. The datum the breakdown found (a size, an algorithm, a count) sits on the piece it describes ("AES-256" on the lock), smaller than the label, readable in a phone screenshot, out of the caption zone. The label says what the piece is, the datum says how much or which one; in a card of its own, the datum turns back into a wall of text. A number that changes with the animation can run as a counter.

### Rhythm

Wherever the screen carries the explanation (a scene in the without-face mode, a split-screen panel, an explanation stretch in the face-at-the-turns mode), aim for at least 3 **visual events** per 10 s and never more than 4 s without a new state. A visual event is a new state that holds and changes a visible part of the frame, about a fiftieth of it or more (some 200 by 200 px of the 1080x1920 frame, in the panel too): a piece entering at the stage's scale, a transformation, a move across the stage. A small piece that moves (a magnifier sliding to the next item) changes too little to count; grow it, or move the piece it points at. A label, a dot or a highlight on a small piece does not count, so a plan full of small entrances still reads as a still screen; count only the events that pass this bar, and when they fall short, make the change bigger rather than adding small ones. Count beats, not entrances: changes less than a second apart (the drop falls, the paint swirls) read as one beat, and the eye then waits for the next. Spread the explanation's beats one to three seconds apart, each on its own word, instead of bunching two or three right after one word and leaving the next five seconds still. Where a stretch has only small changes (a stamp, a piece that stretches), add one change at the stage's scale on its key word, or declare that stretch a rest. A **rest** declared in the plan (the climax, the impact screen, a turn that empties the stage) may hold up to about 6 s. The reference reels without a face run 3.6 to 4.3 events per 10 s; a still screen under a voice reads as a slide. Overlays and the face are outside this rule.

### Impact screen

At the climax the breakdown marked, the scene takes the whole stage for 0.5 to 1.5 s, cut in hard on the anchor word, once per video. What fills it: the result itself grown to fill the stage when it is a colour or object already in the scene (the shared colour floods the frame), so the object transforms instead of being cut; otherwise the accent colour with at most one keyword from the speech or one object. The exit is free: a cut, or a transformation back to the stage. Never a full-screen saturated red, and never in quick succession: flashes above three per second are an accessibility hazard (WCAG 2.3.1). By screen mode: it fills the frame without a face, only the panel in a split screen (the face below reacts), and with the face or in an overlay it is a full-screen insert the author places in CapCut. A highlight works because it is rare, which is why there is only one.

### Overlays

`html, body` transparent (drop any background the design system sets). The viewer watches the author's face and reads the captions, so overlays have two sizes:

- **Sticker:** in the free area of the recording frame, between the top safe margin and the top of the head in the usual chest-up framing, never over the face or the caption zone.
- **Image over the face:** the source (a cover, a page), the subject (a logo, an object) or the image a gesture points at, in the top half of the frame, fading into transparency down to the forehead, never over the eyes, the mouth or the caption zone; for up to about 4 s, still or with one move (enter, settle, leave). Never a label, a diagram in steps or text that repeats the speech: longer or busier, it competes with the face, which is the reason to be in this mode. A CTA in close-up with no free band above the head may use this size.

A hook form in an overlay may reach below the band toward where a gesture points, by the same limits as the image over the face. An explanation in steps with the face present goes to the split screen, never to an overlay.

Done when the scene has a `render(t)` covering its whole duration and every sticker, label and choreography item passes the rules above.

## 6. Check stills, then render

1. `python3 scripts/render.py stills cenas/NN-name.html 1.0 4.2 ... --backdrop stills/backdrop.png --out stills/NN-name` writes each still alone and composited over the recording frame. Pick times at every entrance, at the densest moment, inside each process and on the impact screen.
2. Look at every still: inside the safe margins; nothing over the face or the caption zone; text fits its sticker; the main piece spans 2/3 of the stage or the zones cover it; every sticker and label read alone says what its sentence says; no frame draws a state the speech denies; the impact screen fills its stage. Fix and repeat.
3. Gate: show the composited stills and ask, with options (recommended first): render; adjust a named still; back to the plan. Render only after the author approves, also when the request asks for the finished file or you would call the render a draft: placement and wording are fixed on stills in seconds, while every change after a render costs a new render.
4. Render:
   - overlay: `python3 scripts/render.py video cenas/NN-name.html DURATION exports/NN-name.mov --alpha`, which writes QuickTime Animation (qtrle), the alpha format that kept its transparency in CapCut. Deliver only this file: a VP9 `.webm` with alpha came out black there, and ProRes 4444 runs to hundreds of MB. Ask the author to test the `.mov` in CapCut before the next scene.
   - full scene: `python3 scripts/render.py video cenas/NN-name.html DURATION exports/NN-name.mp4`.
   - split screen, whole-video modes and sound track: as in [references/formats.md](references/formats.md).

   Run at most two `render.py` at a time, stills included, and a longer batch in the background with a log per file. Each run opens its own Chromium at 1080x1920 and pipes frames into ffmpeg; eight at once exhausted the memory of a 16 GB WSL machine, which restarted with nothing written.

Done when every file is in `exports/`, its row in `timeline.md` has the start and end timecode, and the author has the paths.

## 7. Verdict

Ask the author for a verdict on the delivered reel, with options (recommended first): approved; approved with changes (which); redo a named scene. Turn every reason they give into a pattern in `estilo.md`, written as the pattern and its why, with an example from another subject when the case alone would not show it.

Done when the verdict is recorded and `estilo.md` reflects it.
