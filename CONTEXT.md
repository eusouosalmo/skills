# Skills

A public collection of agent skills and the method used to create and evaluate them.

## Language

### Creating a skill

**Observed failure**:
Something that went wrong when actually run, never only imagined: an agent doing a real task without the skill (or with its previous version), or, when there is no such case yet, the existing tool or community skill for the job run against realistic inputs. One of the two valid reasons to create or change a skill; the other is a reference gap.
_Avoid_: imagined problem, nice-to-have

**Reference gap**:
A technique that a high-performing reference uses and that the baseline's output lacks, shown by running the baseline on the same kind of input. The other valid reason to create or change a skill: measured, like an observed failure, so it is never a nice-to-have by another name.
_Avoid_: inspiration, best practice

**Baseline**:
The run of an eval scenario without the skill, or with the previous version when changing one. The skill is judged against it.
_Avoid_: control, before

**Eval scenario**:
One realistic prompt plus what a good result looks like (expected output, assertions, human feedback). Three of them, drawn from observed failures, come before the skill is written.
_Avoid_: test case, example

**Assertion**:
A verifiable statement about an eval scenario's output, checked with concrete evidence. Covers what is objective; style is left to human feedback.
_Avoid_: check, rule

**Human feedback**:
A person's verdict on the subjective quality of an eval scenario's output. Empty feedback means the output was good.
_Avoid_: review, approval

**Near-miss**:
A prompt that shares keywords with a skill but asks for something else, so the skill must not trigger on it.
_Avoid_: negative example

### Voice

**Voice**:
How eusouosalmo sounds in any channel: open with a concrete scene, anchor every idea in a real number, error or example, use a metaphor only when it explains, stay honest and free of hype. It does not change between channels.
_Avoid_: tone, style

**Register**:
What changes with the channel while the voice stays the same: the form of address ("tu" or "você"), the catchphrases, the sentence length. There are two: spoken and written.
_Avoid_: voice (when only the form of address or catchphrases differ)

### Harness

**Harness**:
Everything set up in a project around the coding agent so it gets things right more often: context and spec on the way in, the loop in the middle, verification on the way out, plus guardrails, state between iterations and observability. Built per project, improved from observed failures. Not the agent program itself.
_Avoid_: setup, scaffolding

**Guardrail**:
Something that stops an action before it runs: a deny rule, a blocking hook, branch protection on the server. Says nothing about whether the work is right.
_Avoid_: rule, convention (a guardrail is enforced, not asked for)

**Verification**:
Something that tells whether the work is right or done: tests, type checks, lint, review, quality gates. Fed back to the agent so it can correct itself. A blocking verification needs a guardrail so the agent cannot disarm it (`--no-verify`, deleting tests).
_Avoid_: guardrail, backpressure, sensor

### Script

**Script**:
The production script for a short video: the spoken lines and the visual for each block, alternative hooks, and the claims to check before recording.
_Avoid_: roteiro final, draft (a draft is any unreviewed version)

**Teleprompter text**:
Only the spoken lines of a script, one sentence per line, with no labels, plus the estimated duration. What is read while recording.
_Avoid_: script (when only the lines are meant)

**Hook**:
The opening of a video that keeps the promise of its first frame or title, so the viewer stays. In a follower-question video, the question itself.
_Avoid_: intro, gancho genérico

**Visual hook**:
What the screen does in the first three seconds, with or without text. Big text is one kind of visual hook, not the only one.
_Avoid_: thumbnail, texto do gancho

**Format**:
A kind of video, nameable before the subject is known and reusable on another one: a paradox solved in layers, a list, myth and truth.
_Avoid_: structure (one video's blocks), template

**Structure**:
The sequence of blocks of one specific video, each with its time and job. An instance of a format.
_Avoid_: format, skeleton

**Technique**:
One device, of script or visual, that fits any format: a re-hook, an analogy, a fixed character in the centre. Moving it to another video does not change that video's format.
_Avoid_: trick, format

**Reference sheet**:
The analysis of one reference reel through two lenses, script and visual, in a fixed set of fields so sheets can be compared.
_Avoid_: ficha (in English text), review

### Scenes

**Breakdown**:
The speech split into stretches of meaning, each noted with its concept, its intent from a fixed list, the anchor words with their times, and what it asks to show. Comes before the scene plan and feeds it; read by the agent, not by the author. Decupagem, in pt-BR.
_Avoid_: enriquecimento, leitura de sentido, plan

### Distribution

**Status**:
How mature one skill is: draft, beta, stable or deprecated. Set per skill, in its frontmatter; decides whether the skill is offered to install.
_Avoid_: version, stage

**Release**:
A numbered version of the whole repo, with its changelog entry and tag. Users of the plugin move from one release to the next; a skill's status does not change with it.
_Avoid_: version of a skill, deploy
