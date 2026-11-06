# Effects catalog

Read in step 3, after the destinations are set, to pick the effects to offer at the plan gate; and whenever the author asks what can be done in a reel ("o que dá pra fazer?", "que efeitos tem?").

An effect here is a named addition the author can say yes or no to, on top of the destinations of step 3. The catalog holds the mechanics (what it is, when it fits, how it is built, its limits); how it looks comes from the design system and `estilo.md`. Names are in pt-BR because the author picks them by name.

## Offering effects

1. **Candidates.** For each stretch of the breakdown, read the "Fits" line of every effect below and note the ones whose moment the stretch has. A stretch with a gesture, a quoted message or a denied myth usually has one; most stretches have none, and that is fine.
2. **Budget.** An effect is an emphasis, and an emphasis works because it is rare: at most one effect per stretch, never in two stretches in a row, and about one per 15 s of reel, the hook and the climax included. When candidates exceed the budget, keep the ones on the stretches that carry the point.
3. **Taste.** `estilo.md` wins: an effect the author turned down is not offered again for the same kind of moment unless they ask, and one they approved is the first choice for the same kind of moment. Record each answer there after the verdict, with the reason.
4. **At the gate**, in the plan, a block "Efeitos propostos": one line per effect with the stretch, the anchor word and its time, the effect's name and the reason in a sentence. Ask with a multi-select question: the recommended effects first, each as its own option, plus "ver o catálogo". For an effect this author has never seen in one of their reels (not in `estilo.md`), add one draft still of it over `stills/backdrop.png`, so they choose by the picture and not by the name.
5. **Asked for the catalog**, show the effects grouped by moment (gancho, virada, prova, pedido, clímax), one line each with its name and what the viewer sees, ready ones first, then the ones still on the way with what they wait for.

Each effect is a visual event: on a panel or a scene it counts in the rhythm of step 5, and in an overlay it gets its sound in `window.SFX` like any entrance.

## Behind the head

Some effects sit behind the author: the head covers part of them, which puts the author inside the scene instead of under a sticker. Build them as a transparent overlay `.mov` like any overlay, and mark the row in `timeline.md` "atrás da cabeça"; the `reel-finish` skill lays a cut-out of the person over that overlay, in the CapCut project and in the mp4. Limits, because the cut-out is made from the recording at full frame:

- Only where the face fills the frame: not in a split screen or its keyframe, not during the opening entrance.
- Up to 8 s. Longer, it stops being an effect on a stretch and becomes a set the whole reel lives in.
- What must be read stays clear of the head: the head covers the middle of the frame from the top of the hair down, so a word goes above the hair or wide enough that it reads with the middle covered. Check on the still with the head in mind: the stills show the overlay over the face, and only the finished preview shows the hair in front.

## Ready

| Effect | What the viewer sees | Fits | Build | Limits |
|---|---|---|---|---|
| **palavra na parede** | One or two words of the speech, huge, on the wall behind the author, entering on the frame they are said | the hook with the form "texto grande"; the subject's name; the claim at a turn | overlay behind the head; the words in the design system's display type, at least 250 px tall | the stamp rules of step 5 (spoken words, same meaning as the sentence); stays between x 110 and 970, even when a word that long has to shrink; a word that only repeats a caption flash of `reel-finish` is one or the other, not both |
| **palavra riscada** | The same giant word, and a line traced across it on the word that denies it | a myth or a common belief the speech denies ("todo mundo acha que...", "não é X") | as above, with the line as a traced SVG path ending inside the negation word | the line uses the design system's colour for an error; never draw the denied state without the line |
| **sala apagada** | The room goes dark behind the author, who stays lit | a confession, the turn into the problem, the climax with the face on screen | overlay behind the head: the design system's darkest ink at 40 to 60% over the whole frame, cut in dry on the anchor word with a `lock` sound (a light switch), held 2 to 6 s, cut out dry | once per reel; never a saturated colour; may hold a palavra na parede on top |
| **pilha atrás da cabeça** | Prints, headlines or pages land one by one on the wall behind the author, tilted, each on the word that names it | proof by quantity ("todo mundo está falando disso"), a list of cases, cited sources | overlay behind the head with the source prints of the script (or found by the image rules), each with its credit line | three to five prints; each one is a third-party page: one quoted sentence at most, credit in `## Créditos para a legenda` |
| **comentário que chega** | A comment or message card types itself in and posts, in the band above the head | the speech answers a viewer's question or a message the author got ("me perguntaram...", "recebi isso") | sticker overlay in the design system's card shape, never a copy of the platform's interface | only real comments or messages, the sender's name and photo blurred unless they are a public profile who posted it publicly; when the author reads it aloud, the card shows it before they start and then only the key words stay highlighted |
| **botão seguir** | A follow button in the design system's shape is pressed and turns into "seguindo" | the spoken CTA to follow | sticker overlay in the band above the head, pressed on the word of the ask; when the author points at it, the press lands where the finger points | once, on the CTA; the button is drawn, not a copy of the platform's |
| **quadro congelado com seta** | The recording freezes on a frame and an arrow or circle traces to what matters in it, then the video goes on | a gesture or object with meaning in the take (the phone held up, the finger pointing), when the speech names it | full-screen scene with that frame of the recording as its background (`ffmpeg -ss <t> -i recording.mp4 -frames:v 1`) and the trace on top; the voice goes on underneath | mixed mode only; 0.8 to 1.5 s, since the mouth stops while the voice goes on; the trace ends inside the word that names the thing |
| **arrasta antes e depois** | A divider slides across one image and reveals the other underneath | a contraste of two states of the same thing (before and after, wrong and right) | in the contraste scene or panel, the two states stacked, the top one clipped by the divider's position from `render(t)` | the divider crosses on the word of the change, in under 1 s; both states are the same framing, so only the change moves |

Already in the chain, offered by their own rules and not counted again: sticker (step 5, "Overlays"), image over the face, split screen and the whole-video modes, impact screen, source shot, sound by material ([formats.md](formats.md)), and in `reel-finish` the punch-in and the template word behind the head.

## On the way

Offer these only as "ainda não dá", with what they wait for, when the author asks for something they would solve:

- **empurrão lento:** the frame pushes in slowly (about 1.0 to 1.08 over 3 to 5 s) on a serious or personal line. Waits for `reel-finish` to render a gradual zoom; today it has only the hard punch-in.
- **mira no rosto, órbita, adesivo que segue a cabeça:** brackets that lock on the face as the frame follows it, objects circling the head (behind it on the far side), a sticker that moves with the head. Wait for a face track of the recording that the scenes can read.
- **silêncio antes do clímax:** the sound effects drop out for about 0.4 s before the impact screen, so it lands harder. Waits for `scripts/sfx.py` to carve the gap.

## Not offered

- A copy of a platform's own interface (the comment box, the phone's switches, the messages app): it reads as the real app, and the design system's card says the same thing in the author's look.
- Glitch bars, wipes and colour grades as a look: the design system forbids the first two, and a grade is the author's taste; offer one only when `estilo.md` asks for it.
- Effects that change the author's appearance (a magazine cover of them, a filter on the face): their image is theirs to change, and a generated or altered face is never made.
