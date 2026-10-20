---
name: writing-short-video-scripts
description: Writes short video scripts (Reels, Shorts, TikTok) from the author's notes, with hook, structure, one spoken CTA, teleprompter text timed to the target duration and prints of its sources for the edit. Use when the user asks for a reel or short video script, to restructure one, or for the source prints of one (roteiro, reels, vídeo curto, teleprompter, prints das fontes).
compatibility: Capturing source prints needs python3 with playwright and its Chromium (pip install playwright && python3 -m playwright install chromium).
metadata:
  status: beta
---

# Writing short video scripts

A **script** is the production text of one short video: the spoken lines with the visual for each block, alternative hooks, and the claims to check before recording. Write the output in pt-BR.

## 1. Set the video's context

A creator asking for a "roteiro" from notes means a video script. Before structuring, you need:

- **platform and format**: Reels, Shorts or TikTok, and the target duration (default 60 to 90 s);
- **objective**: inform or start a conversation. The objective picks the CTA;
- **one idea**: one video carries one idea. When the notes hold several (two concepts from the same chapter), propose one angle per video, each with its own hook, and write one script per angle;
- **the case opens, the mechanism is the subject**: when the notes bring a case (a bug, an incident, a strange behaviour), the video's idea is the mechanism the case lets the viewer see, not the diagnosis of the case. "O deploy caiu numa sexta" opens the video, and the subject is how a rollback works. The author's guesses about an unknown cause stay hypotheses. The idea is set when it can be written without the case ("como um sistema de comentários aguenta milhares de respostas");
- **format**: the kind of video, from [formats.md](formats.md) (read it now). When the request names a format, use it; when that format does not fit the notes, say why and suggest one that does. When the request names none, offer 2 or 3 formats whose motor matches the notes, from different families when the notes allow, each by its pt-BR name with one line on why it fits these notes.

Ask for whatever the request leaves out, the format included, and wait: write no script blocks until the answers come. Done when platform, duration, objective, the single idea and the format of this video are known.

## 2. Separate the knowledge from its source

The notes usually come from a source: a book, article, video or test. The video delivers the **knowledge** and the author's own case; the source is credit, not subject.

- The spoken lines teach the idea directly. They never narrate the reading ("tô lendo", "o livro diz", "no capítulo 2").
- The source goes in a `Crédito para a legenda` line at the end of the script.
- When the script depends on a concept the notes only name ("o artigo mostra um diagrama"), ask the author for their notes on that part of the source. Until they come, explain it from what you find in the research below.
- **Research the facts before writing.** Look up in a primary source (official documentation, specification, paper, the source's own text) every fact the video will state: the numbers and names of the concrete case, technical behaviour (operator, flag, version, default) and the definitions a contrast rests on. Per claim, stop at the first primary source that confirms it; after about three searches without one, the claim goes to `A checar antes de gravar` with what was tried. A claim about the source that the notes do not back (what the book says, its definitions, its examples) is checked the same way. The author's own story is never researched; it comes from the notes.
- **Capture the source while it is open.** For every source in `Conferido` whose page the edit can show (an article, a paper, an official page, a document), run `python3 scripts/capture_source.py <url> assets/<script file name>/NN-<source> --highlight "<the words of the claim as the page writes them>"`, numbered in the order the script uses them, next to the script file. It writes the top of the page and the passage marked in yellow, without ads and banners, so the edit shows the proof the speech cites instead of a drawing of it, and a print taken later may show a page that changed. When the script exits 2, the page writes the claim in other words or another language: read its text and run again with its words; a passage print without its mark proves nothing. When it exits 3, the site blocked the automated browser: the source becomes a **falta:** row for the author to capture. When the claim sits in a part that opens on click (a question in an FAQ), pass `--click "<its title>"`. Look at every print: a leftover ad, banner or empty box gets cropped or noted.
- When a source contradicts the notes, the script follows the source and the gap goes to the questions after the file ("tua nota diz X, a fonte diz Y, escrevi Y"). Never correct the notes silently, never record their error.
- A number the research did not confirm is spoken only as a hypothesis ("imagina", "digamos"); a number spoken as fact is in `Conferido`. An example case the author did not live (a made-up app, a sample table) opens as one ("imagina um app de entrega"), so its sizes and durations read as part of the hypothesis; outside that frame, a number is a fact.
- Without web access, every checkable fact the script states as fact, the definitions a contrast rests on included, goes to `A checar antes de gravar` with where to check it, and the delivery says the facts were not researched.
- The author's own story keeps the verb and degree of the notes. The notes' hedges stay ("por exemplo", "alguns meses"). A role, number or result never goes up a level: "liderei o projeto uma vez" stays that, never "sou tech lead". When the exact version sounds weak, say the honest contrast ("eu não era tech lead, mas tive que liderar como um").
- The author's story is told as past experience, free of date and employer, so the video still holds after a job change and exposes no one. Keep the problem, the public tool, what the author did and the result. Turn markers of time and place into a past event ("hoje", "atual", "na empresa onde eu tô" become "quando eu precisei", "uma vez"); an employer or client name becomes a category ("num e-commerce"); internal data, identifiable people and judgements about the company or colleagues leave. Generalising never changes the fact: one company stays one, not "várias empresas".

Done when no spoken line mentions the source, every fact the script states is either in `Conferido` with its link or in `A checar antes de gravar`, never in both, every source in `Conferido` whose page the edit can show has its `-trecho` print with the mark (or a note on why not), and every statement about the author matches the notes with no date or employer in it.

## 3. Build the format's structure

The script follows the blocks of the chosen format, in its order, and the `Bloco` column uses the format's block names. The format's blocks change only the order; every rule in this skill holds inside each of them. A block that states a principle or a rule ("Princípio", "Regra") is a claim and gets its reason in step 4. Beyond the format, every script keeps these rules:

- **Hook** (first 3 s): the opening lines of the format's first block are the hook, whatever that block is called ("Sintoma", "Afirmação absurda"); when the format's first block is a scene that does not hook (a long setup), add a `Gancho` block before it. Read [hooks.md](hooks.md) now: the hook comes from one of its patterns (the format's, when the format asks for one), follows its rule for terms, passes its five questions, and the two alternatives come from other patterns, each named. The hook never calls the viewer by role, and its terms win over the author's short word: "dev" in the notes becomes "desenvolvedor" in the hook. It names the video's subject, also when the format opens on a symptom or a scene: a video about indexes that opens on a slow query still says "índice" in the hook. The sentence after the hook follows "After the hook" in hooks.md. The hook's Visual cell starts with `Forma: <form>`, one of the five visual hook forms in hooks.md, the one the format points to, and then describes what is seen; the animation step confirms or changes it. No on-screen text repeats or sums up the spoken hook: big text enters only as the subject's or series' name (up to 4 words) or as a typed question the format opens with.
- **The author's case as proof.** Use the case from the notes; when it sums up specific things in a generic word ("usei várias ferramentas") and the notes do not say which, write `[falta: ...]` asking for them, worded so the sentence stands if the answer never comes. The `[falta: ...]` goes in even when the sentence already holds, because the author decides whether a case exists. Only once the author says there is none, keep the general sentence when it holds on its own or cut the passage. Never invent the case. Ask only for specifics the notes sum up; a new anecdote or an outcome the story works without is not a gap.
- **What the hook opens is paid off** before the last line. A case whose cause is unknown is paid off with pieces the body already built: the ending returns to the case naming which of them could cause it, marked as hypothesis ("não sei qual foi"), with no new suspect and no list of hypotheses.
- **One closing question.** The last spoken line is the CTA: one question born from the close, which the viewer answers in a word or a short sentence about themselves. When the format's close delivers a tool (a question to ask, a rule, a symptom map), the tool becomes the CTA: one question that has the viewer apply it to their own case ("Qual peça do teu sistema não passa nessas duas perguntas?"), never the tool's question followed by a second one. When the close is a caveat or a dilemma, the CTA comes out of it. Questions the video answers itself may sit in the body when the format asks for them; only the closing question waits for the viewer's answer.

An image or metaphor (a funnel, an iceberg, a traffic light) gets one **image passage**: from the first sentence of the image to the last spoken correspondence between a part of the image and the subject. It may cross blocks. Inside it, the spoken lines may use the image's words, as long as every part they use gets its correspondence said aloud ("o carteiro é o servidor"), because a listener maps the image onto the subject only when the mapping is said. A sentence that only restates the image ("e o cliente vai descendo" right after "pensa num funil") adds no meaning. After the last correspondence, every line, the CTA included, names the thing itself, never the part of the image: "quem já comprou uma vez", not "quem chegou no fundo do funil". Mapping people, roles or actions onto the image ("o cliente novo fica no topo do funil") is already using the image as vocabulary. Before writing, list the words that name the image's parts and movements (for a funnel: topo, meio, fundo, descer, cair, crescer), and write that list after the file; after the passage, no spoken line uses them. Test each later line heard alone, without the drawing: if it needs the picture, rewrite it in the words the audience uses about their own work.

Only the picture goes back to the image (the **return to the analogy**). When the format closes on the analogy's scene (problem in the analogy, a metaphor world kept as the setting), the return is required; in other formats it is allowed. The Visual cell of the block that returns starts with `Volta à analogia:` and repeats the composition of the failure scene, now solved, with the subject's terms said in the passage as labels over the image's parts ("servidor" over the carrier), so the eye links the two while the voice stays literal.

The spoken lines hold a single ask. A follow request ("me segue") belongs in the caption, where it does not cut the loop at the end of the video.

Done when every block of the format is in the script under its name, no spoken line after the image passage names a part of it, the return to the analogy (when the format closes on it) opens its Visual cell with `Volta à analogia:`, and the spoken lines end on one question that needs no image to answer, with no other question to the viewer after the format's close.

## 4. Earn every sentence

Every sentence either moves the idea forward or leaves, like Chekhov's gun: what appears gets used. Improve a sentence before cutting it.

First, the **ladder test**, block by block. For each body block after the first, name the problem the previous block left that brings this one in ("com dez mil respostas, a resposta fica enorme, então entra a paginação"), and make the block's spoken lines say it. If two blocks can swap places and the video still stands, the body is a list: rewrite it so each block answers what the previous one broke or left unexplained. A block or sentence that floats a possible cause of the opening case ("pode ser X", "pode pedir de outro jeito") is a suspect, not a step; cut it. Time order counts as a link only when each step needs the one before (you can only cook after buying), as in the routine format.

Then go through the spoken lines one sentence at a time:

1. **In the chain?** Delete the sentence and read its neighbours. If nothing is left unexplained, try to tie it to the idea in one clause; if that fails, cut it. Whatever the hook raises gets paid off before the CTA.
2. **Would the target viewer ask "por quê?" or "como assim?"** Advice, evaluations and claims the viewer must accept ("precisa escrever o teste antes", "pode virar um problema") almost always ask for it. Add the reason in one clause of up to about 12 words, with something concrete in it, something the viewer can picture or name (a version, an error, a tool, a number, an event): "porque o teste que já passa antes do código não testa nada". A reason that restates the claim in other words ("porque a área muda muito") does not count. When the reason is obvious to this audience, the sentence stays as it is. A claim tucked inside another sentence or inside a reason ("porque é ele que sobe pra produção e precisa revisar tudo antes") is still a claim and gets the same test.
3. **Vague reference?** A sentence resting on "isso", "aquilo", "coisa" or a category with no referent ("era coisa de quem viveu aquilo") gets the concrete referent or leaves. A "quem" with nothing after it ("só quem viveu sabia", "quem passou por ali") names no one: say what was lived ("quem já tinha visto a fila travar").
4. **Joined where the ear needs it.** For each pair of consecutive sentences, name the relation between them first, then the word. When the second is the cause of the first, write "porque" or "isso porque"; when it is the consequence, "então" or "por isso"; when it contrasts, "mas" or "só que". Join the two, up to about 20 words with at most one dependent clause. When the relation is only sequence or addition, write no connective: keep them apart or cut one. A connective the relation does not ask for ("então" before something that does not follow from the previous sentence) reads as filler; remove it. The hook and one turning-point line may stay short and dry on purpose.
5. **The author's words, once each.** Every sentence about an idea uses the author's own word for it ("deploy", never a synonym such as "subir pro ar" when the author says "deploy"). Any other content word that shows up in consecutive sentences, or more than three times in the video ("projeto", "funciona"), gets rewritten so the sentence needs it once.

Done when every body block says the problem that brings it in, every claim the viewer would question carries a concrete reason, every "porque" clause in the spoken lines names something concrete ("porque leva tempo", "porque a ferramenta muda", "porque é importante" name nothing the viewer can picture), no sentence fails the chain test, and no cause or contrast between consecutive sentences is left unsaid outside the hook and the turning point.

## 5. Pass the spoken lines through the voice

Use the author's voice skill on the spoken lines (for eusouosalmo, the `writing-as-eusouosalmo` skill, spoken register). Without a voice skill, mark the lines as provisional.

Done when the voice skill's own check passes.

## 6. Fit the duration

Count the words of the spoken lines (`wc -w`) and estimate the duration at 130 words per minute: 60 to 90 s is 130 to 195 words. Over the target, cut what the idea survives without: first what failed the chain test, then sentences that repeat another, then details the case does not need. Keep the hook, the CTA and every reason added in step 4; when they do not fit, cut a claim together with its reason.

Done when the count is inside the target.

## 7. Deliver

One file, two parts:

```markdown
# Roteiro: <angle>

Plataforma: <...> | Duração alvo: <...> | Objetivo: <...>

## Script

| Bloco | Fala | Visual |
|---|---|---|
| Gancho | ... | Forma: <visual hook form>. ... |

Padrão do gancho: <pattern of the main hook>

Ganchos alternativos:
- ... (<pattern>)

Conferido:
- <claim>: <link to the primary source>

A checar antes de gravar:
- <claim>: <where to check it, or what was tried>

Crédito para a legenda: <source>

## Referências visuais para edição

Prints em `assets/<script file name>/` (capturados em <date>, tela de 1280 px; `-topo` é o início da página, `-trecho` é o trecho marcado em amarelo).

| Bloco | Arquivo / o que capturar | Fonte | O que destacar na edição |
|---|---|---|---|
| ... | `NN-<source>-trecho.png` | <url> | <the spoken words the mark shows> |

## Teleprompter

<one spoken sentence per line, split at every period, no labels>

Duração estimada: <words> palavras, <seconds> s a 130 palavras por minuto.
```

The visual references table has one row per thing the Visual column shows from outside the script: each print, and what only the author can give, as a **falta:** row saying what to capture and where (a stretch of the author's own earlier video, a screen recording on their phone, a page behind a login), so the edit asks for it instead of drawing a stand-in. A print with a third party's personal data (the name, handle and photo of whoever wrote a comment) says **Embaçar** with what to blur, since the person did not agree to be in the video. When the author asks for the prints of a script already written, capture its sources the same way and add this section to that file.

After the file, list every `[falta: ...]` and question to the user, and each claim from step 4 with the concrete thing in its reason, so the author sees the check.

Before handing it over, go through [checklist.md](checklist.md): every correction the author has made to a script, so the next one does not need it again. Done when the file follows this shape, the teleprompter part holds only the spoken lines, and every checklist item holds.
