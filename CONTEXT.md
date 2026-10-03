# Skills

A public collection of agent skills and the method used to create and evaluate them.

## Language

### Creating a skill

**Observed failure**:
Something that went wrong when actually run, never only imagined: an agent doing a real task without the skill (or with its previous version), or, when there is no such case yet, the existing tool or community skill for the job run against realistic inputs. The only valid reason to create or change a skill.
_Avoid_: imagined problem, nice-to-have

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
