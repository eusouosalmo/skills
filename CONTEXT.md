# Skills

A public collection of agent skills and the method used to create and evaluate them.

## Language

### Creating a skill

**Observed failure**:
Something an agent got wrong while doing a real task without the skill (or with its previous version). The only valid reason to create or change a skill.
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
How sa/mo sounds in any channel: open with a concrete scene, anchor every idea in a real number, error or example, use a metaphor only when it explains, stay honest and free of hype. It does not change between channels.
_Avoid_: tone, style

**Register**:
What changes with the channel while the voice stays the same: the form of address ("tu" or "você"), the catchphrases, the sentence length. There are two: spoken and written.
_Avoid_: voice (when only the form of address or catchphrases differ)
