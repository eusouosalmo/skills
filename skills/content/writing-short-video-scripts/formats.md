# Formats

Twelve formats in four families. A **format** is a kind of video reusable on any subject; a **format family** groups formats that share the same motor, the thing that pulls the viewer from one block to the next. Each format lists its blocks in order with the job of each, the hook pattern from [hooks.md](hooks.md) it asks for (when it asks one), how it closes and the subject it fits. Use the block names in the script's `Bloco` column.

- [A. Process as a ladder](#a-process-as-a-ladder-processo-em-escada)
- [B. Everyday mystery](#b-everyday-mystery-mistério-do-cotidiano)
- [C. Analogy for beginners](#c-analogy-for-beginners-analogia-para-quem-começa)
- [D. The developer's pain](#d-the-developers-pain-dor-do-dev)
- [Picking formats to offer](#picking-formats-to-offer)

In every format, each block is caused by the one before it (a **ladder**): something breaks or stays unexplained, so the next block comes in. A block that could swap places with its neighbour turns the video into a list.

## A. Process as a ladder (processo em escada)

Motor: a causal chain. Fits a system, pipeline or process the viewer uses without seeing inside.

### System that grows by problems (sistema que cresce por problemas)

1. **Versão mínima:** the simplest version that works, for few users or little data.
2. **Degraus:** pressure rises in steps; at each step something breaks, and one new piece comes in to fix only that. Name the problem before the piece.
3. **Virada:** the video turns on itself: every piece has a cost, and adding a piece no problem asked for is the mistake.
4. **Regra e ferramenta:** the rule behind every step (add a piece only against a real problem) and a question the viewer can apply to any system.

Close: delivers a tool. Fits: architecture, infrastructure, any system that grew over time.

### Process walked by a single case (processo percorrido por um caso só)

1. **O caso:** one concrete item (a commit, a request, an order) with enough detail to be that one, not a generic one.
2. **Etapas:** the item crosses the process one stage at a time; each stage is explained as the item passes through it, and one stage stops it, with the reason.
3. **Camada extra:** after the process looks complete, one more layer the viewer did not know (what happens when it still fails).
4. **Síntese:** each part of the process summed up as the one question it answers.

Close: delivers a tool (the questions). The process already exists and is walked; in the system that grows, it is built piece by piece. Fits: CI/CD, a request's path, a checkout flow.

### Journey of an object end to end (jornada de um objeto de ponta a ponta)

1. **Cena:** a person does an everyday action with a destination and a short real time (sends a photo, pays at a card machine).
2. **Etapas:** the object of that action goes through the system; at each stage it changes form (compressed, split, labelled), and the change is the concept.
3. **Volta:** the way back, in a few sentences, in reverse.
4. **Mapa de sintomas:** what goes wrong at each stage and where to look.
5. **Ressalva:** the limit of the model the video used.

Close: delivers a tool (the symptom map) and a caveat; the last line goes back to the opening scene and its time. Fits: networks, payments, anything with layers or hops. A variant of the single case, with an object that transforms.

## B. Everyday mystery (mistério do cotidiano)

Motor: a belief the viewer holds, contradicted. Fits a phenomenon the viewer lives without knowing why.

### Paradox solved in layers (paradoxo resolvido em camadas)

1. **Experimento mental:** a scene the viewer can picture leads to an absurd prediction.
2. **Explicação famosa:** the known explanation, which then falls short.
3. **Camada verdadeira:** the real answer, in one sentence the viewer can repeat.
4. **Última camada:** one more layer that turns the answer again, often bringing back the explanation that fell.
5. **Frase do cotidiano:** a closing line that makes the viewer's everyday experience recall the video.

Hook: unsaid question (pergunta não dita). The scene or prediction makes the viewer form the question alone; no line asks it. Close: changes an everyday experience. Fits: behaviours of systems everyone sees (why the loading bar lies, why the queue next to you moves faster).

### Experiment that reproduces everyday life (experimento que reproduz o cotidiano)

1. **Frustração:** a situation every viewer has lived.
2. **Causas negadas:** the obvious causes ruled out one by one.
3. **Experimento:** a controlled setup that reproduces the problem without any of those causes.
4. **Mecanismo:** step by step, inside the experiment.
5. **Segundo experimento:** a change that makes the problem go away, and the opening scene read again with it.

Hook: exclusion (exclusão). The proof comes before the question: the obvious causes are denied in the opening lines. Close: the opening scene explained, with something the viewer can do. Fits: performance and concurrency problems that appear with no error.

### Absurd comparison that splits two metrics (comparação absurda que separa duas métricas)

1. **Afirmação absurda:** a claim that sounds like a joke and is true in one metric.
2. **Conta em voz alta:** the proof as short arithmetic, one factor per sentence, in units the viewer pictures.
3. **Troca de métrica:** the same comparison in the other metric, and the winner flips.
4. **Regra:** the two metrics named as two things, and when each side wins.
5. **Mundo real:** a real case where the absurd side was used.

Hook: half-truth (meia-verdade). The opening claim is true in one metric only, and the video later shows the metric where it is false; it sounds exaggerated, so the next sentence anticipates the objection. Close: the rule of when each side wins. Fits: throughput against latency, read against write, average against worst case.

## C. Analogy for beginners (analogia para quem começa)

Motor: a world the viewer already masters. Fits a concept that sounds hard to someone starting out.

### Problem in the analogy, solution in pieces (problema na analogia, solução em peças)

1. **Falha na analogia:** an everyday scene where something goes wrong in a way the viewer recognises.
2. **Transferência:** the same failure in the technical area, said in one or two sentences.
3. **Solução em cena:** back in the analogy, the object that solves the failure appears and solves it there, while the viewer watches it work.
4. **Nome:** only then the object gets the technical name and its definition. The subject may be named earlier as a label (in the hook, for instance); what waits for the scene is "a solução se chama X" or "X é...".
5. **Peças:** the object opens into its parts, each part with its term, each said through what it does in the scene.
6. **Volta à falha:** the failure from the start, now solved. The return happens on screen; the spoken lines stay in the subject's words.

Close: the failure solved, then a CTA born from it. Fits: tools and protocols with a few named parts (containers, key exchange, version control).

### Routine that becomes a list of concepts (rotina que vira lista de conceitos)

1. **Rotina:** an everyday task the viewer has done, announced as already holding the concepts.
2. **Etapas:** the task walked in order; each step shows a gesture, and the concept's name comes after the gesture. A fixed refrain when naming ("e isso é X") may mark the count; it is optional.
3. **Contagem:** one task, N concepts, summed up in one sentence.

Hook: the viewer's situation (situação do espectador), with an unexpected consequence: knowing the routine means knowing the area. Close: the count. Fits: first concepts of an area (variables and conditions, addresses and packets).

## D. The developer's pain (dor do dev)

Motor: a habit of the viewer's that has a price. Fits a practice the viewer does today and pays for without knowing.

### Symptom, cure and dose (sintoma, cura e dose)

1. **Sintoma:** the symptom as the viewer sees it in their own code, and the name of the remedy right away.
2. **Caso:** the symptom in one concrete case, with its cost growing.
3. **Cura:** the remedy applied to the same case.
4. **Teste:** a new case arrives and the cure holds.
5. **Princípio:** the principle behind the remedy.
6. **Dose:** when the remedy is not worth it.

Hook: the viewer's situation (situação do espectador), shown as code or output on screen in the first second. Close: a caveat (the dose). Fits: patterns, indexes, refactorings.

### Common doubt answered in passing (dúvida comum respondida de passagem)

1. **Pergunta:** a "por que tu não..." question that presumes a habit of the viewer's, with the viewer in it.
2. **Ameaça:** what goes wrong, in first person ("eu consigo...").
3. **Mecanismo e prova:** how it happens, with one line of proof.
4. **Solução:** the fix.
5. **Ressalva:** what the fix does not cover.

Hook: the viewer's situation (situação do espectador), as the question itself. Close: a caveat. The answer can run while the author does an everyday task on camera. Fits: security and production habits (a token in localStorage, `SELECT *`).

### Study with fine print (estudo com letra miúda)

1. **Preço:** a habit of the viewer's gets a price.
2. **Estudo:** a real study that measured it, with how it measured.
3. **Achado:** the main finding with its number, which looks like the lesson.
4. **Letra miúda:** the turn: the gain sits on the cheap side, and the real cost is elsewhere.
5. **Correção e ressalvas:** the practical fix and where it does not work.
6. **Dilema:** a trade-off question with no right answer.

Hook: the viewer's situation (situação do espectador), with an unexpected consequence: the habit costs. Close: a dilemma, then the source. Needs a real study the author points to or that is found and checked; never an invented one. Fits: AI, tooling and productivity claims.

### Tool swap with one number (troca de ferramenta com um número)

1. **O que tu usa:** the tool the viewer uses and the cost they want to avoid.
2. **O que eu achei:** the alternative, placed by something the viewer knows ("um X, só que...").
3. **Número:** one number before and after, in the same unit and the same test.

Close: hands the tip to the same viewer the opening named. Offer it only when the notes carry a measurement of the author's own.

## Picking formats to offer

Read the notes for their motor and offer the formats whose motor matches:

- a system, pipeline or path the viewer does not see inside: family A;
- something the viewer lives every day without knowing why: family B;
- a concept that scares a beginner, with an everyday world that maps onto it: family C;
- a habit of the viewer's with a cost (a symptom, a doubt, a measured study): family D.

Notes often fit more than one motor; that is where offering formats from different families helps.
