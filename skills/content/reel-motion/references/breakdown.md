# Breakdown

Read in step 2, before writing `breakdown.md`, and again in step 3 for the destination table and the hook forms.

## Fields of a stretch

Write `breakdown.md` in the reel folder, one block per stretch of meaning, in the order spoken:

```
## 04 | 32,1-41,8 s | passos
- Conceito: a mistura das tintas é a troca de chaves
- Âncoras: "misturo" 33,40; "pingo" 35,12; "marrom" 40,96
- Gravação: take 2, cabeça centralizada até y 900 (frame 34 s); faixa livre acima da cabeça; sem gesto com sentido
- Pede na tela: duas tintas caem no mesmo pote e giram até o marrom
- Nomeados: nenhum
- Dado: "Curve25519" (https://...whitepaper.pdf), ou "sem dado: <motivo>" (só em `nome`)
- Exemplo de forma: texto cifrado em hex (forma, não fato)
```

- **Concept:** the idea of the stretch in one line, in your words.
- **Intent:** one from the list below.
- **Anchors:** the words that trigger entrances, with their time from `words.json`.
- **Recording:** the take and where the head is, citing the time of a frame; the free space; a gesture or object that carries meaning, with its time; a change of take, with its time. A hand moving as the author talks is not a gesture with meaning; pointing at something, counting on the fingers, holding up a phone with a screen are. Background and gaze stay out: the set does not change, and contrast comes from the design system.
- **Asks on screen:** what the stretch asks to be seen, including the verb of any process it names.
- **Named:** every person, brand or product the speech names. Each is a candidate; search for an image only for the ones the plan puts on screen (a gesture points at it, the hook form is "source or subject over the face", or the name carries the stretch). Rules in [images.md](images.md).
- **Datum** (stretches with the intent `nome` only): one fact the speech does not say, from the primary source with its URL, or "sem dado" with the reason. The search is never skipped: a datum found and left unused was the failure this rule fixes.
- **Shape example:** example content (ciphertext, key, hash) marked as shape, so no one mistakes it for a fact.

## Intents and destinations

The intent picks the destination. Mixed mode follows the rules of step 3; the whole-video modes reassign:

| Intent | What the stretch does | Mixed, by stretch | Without face | Face at the turns | Split screen, whole reel |
|---|---|---|---|---|---|
| gancho | the first seconds | the hook form (table below) | the hook form, full screen | the hook form, with the face | the hook form; the opening the table gives |
| apresentação | who is talking | face | scene | face | face, panel at rest or emptied |
| opinião | the author's judgement | face | scene | face | face, panel at rest or emptied |
| transição | a turn between parts | face | scene, the stage at rest or emptied | face | panel at rest or emptied |
| ressalva | a caveat | sticker overlay | scene | sticker overlay | panel |
| pedido | the CTA | sticker overlay, or image over the face in close-up | scene | face with a sticker or image over the face | panel |
| passos | a sequence | full screen or split screen | scene | scene | panel |
| contraste | two outputs side by side | full screen or split screen | scene | scene | panel |
| quantidade | a number or scale | full screen or split screen | scene | scene | panel |
| código | code read on screen | full screen or split screen | scene | scene | panel |
| prova | the claim's evidence | source shot, or the proof footage | same | same | panel |
| nome | the technical name of what an analogy or image stood in for | the scene of that image, same destination and composition, recomposed with each name as a label | same | same | panel |
| clímax | the point where the mechanism fires | the destination of the explanation around it, plus the impact screen | same | same | same, the impact screen in the panel |

A gesture with meaning overrides a full-screen destination in any mode with a face (step 3).

**Nome.** The speech gives the technical name of something an image stood in for: an analogy, a metaphor or an everyday scene that represented the subject ("o carteiro é o servidor"). Naming a technical thing the scene already showed as itself (the broken JSON, then "isso é structured output") is not `nome`; the stretch keeps its own intent. When the script's visual carries `Volta à analogia:`, the stretch it marks is the `nome` stretch; without it, find the stretch yourself, since hand-written scripts carry no marks.

**Clímax.** The peak of the mechanism: the point where the explanation fires (the queue stops, the step that decides). The moment that pays the hook's question counts only when it is also what reveals the mechanism. At most one per video; a list, a tutorial or a "how X works" with no peak has none.

## Format and screen mode

When the script names its format, recommend this screen mode in step 1:

| Format family | Formats | Recommended mode |
|---|---|---|
| Processo em escada | sistema que cresce por problemas; processo percorrido por um caso só; jornada de um objeto de ponta a ponta | without face, or full screen with the face at the turns |
| Processo em escada | processo percorrido pelo próprio vídeo | split screen, whole reel |
| Mistério do cotidiano | paradoxo resolvido em camadas; experimento que reproduz o cotidiano; fenômeno explicado pela exceção | without face |
| Mistério do cotidiano | comparação absurda que separa duas métricas | mixed, by stretch |
| Analogia para quem começa | problema na analogia, solução em peças; rotina que vira lista de conceitos; catálogo numa família de analogias | split screen, whole reel |
| Analogia para quem começa | fatura explicada linha por linha | full screen with the face at the turns |
| Dor do dev | sintoma, cura e dose | without face |
| Dor do dev | dúvida comum respondida de passagem; estudo com letra miúda; troca de ferramenta com um número | mixed, by stretch |

## Visual hook forms

The script's `Forma:` names one of five forms. Where each one enters in a video with the face:

| Form | In the hook, with the face |
|---|---|
| fonte ou assunto sobre o rosto | image over the face in the free space; with a gesture with meaning, where it points |
| imagem que se monta na palavra | overlay when it is one object; split screen from frame 0 when it is a drawing that grows |
| resultado mostrado antes | split screen from frame 0, the result in the panel, then it comes apart |
| comparação parada | split screen from frame 0 |
| texto grande (the subject's or the series' name) | overlay, 1 to 4 words |
| só rosto e cenário | nothing |

Without the face, every form fills the frame from frame 0, and its single object is never a placeholder. With no `Forma:` in the script, choose from the hook's words, the format when recognisable and the gestures of the take, and write the choice and its reason in the hook's stretch.
