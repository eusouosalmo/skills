# Sources

This skill describes its method in its own words. No text is copied from the sources below.

- **Skill authoring best practices** (Anthropic): https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices. Evaluations before documentation, three scenarios from observed failures, Claude A writes and Claude B uses, the final checklist that `references/checklist.md` summarises.
- **Agent Skills specification**: https://agentskills.io/specification. Frontmatter fields and limits, folder layout, progressive disclosure.
- **agentskills.io guides**: https://agentskills.io/skill-creation/evaluating-skills and https://agentskills.io/skill-creation/optimizing-descriptions. The `evals/evals.json` format, runs with and without the skill in a clean context, assertions with evidence, human feedback, near-misses for the trigger test.
- **skill-creator** (anthropics/skills, Apache 2.0): https://github.com/anthropics/skills/tree/main/skills/skill-creator. Ideas only: the snapshot of the previous version as baseline, generalising from feedback instead of patching the test case, optional description optimisation.
- **writing-for-agents** (Matt Pocock, MIT): https://github.com/mattpocock/skills. The writing itself is delegated to that skill by name.
- **writing-skills** (obra/superpowers, Jesse Vincent, MIT): https://github.com/obra/superpowers/tree/main/skills/writing-skills. No skill without a failing run first, and the advice to automate mechanical constraints instead of writing a skill for them.
