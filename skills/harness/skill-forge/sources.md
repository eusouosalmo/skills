# Sources

This skill describes its method in its own words. No text is copied from the sources below. The full research behind the phased design is in the repo that publishes this skill, at `docs/research/skills-que-evoluem-com-uso.md`.

## Format and conventions

- **Agent Skills specification**: https://agentskills.io/specification. Frontmatter fields and limits, folder layout, progressive disclosure.
- **Evaluating skill output quality** (agentskills.io): https://agentskills.io/skill-creation/evaluating-skills. The `evals/evals.json` format, runs with and without the skill in a clean context, starting with two or three cases and adding assertions after the first round of outputs, human feedback. Also https://agentskills.io/skill-creation/optimizing-descriptions for near-misses in the trigger test.
- **writing-for-agents** (Matt Pocock, MIT): https://github.com/mattpocock/skills. The writing itself is delegated to that skill by name.

## Why a draft starts early and hardens in use (branches A and B)

- **Skill authoring best practices** (Anthropic): https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices. Evaluations before extensive documentation, and in the same page a skill built from a task done for real and refined from usage. The final checklist that `references/checklist.md` summarises.
- **skill-creator** (anthropics/skills, Apache 2.0): https://github.com/anthropics/skills/tree/main/skills/skill-creator. Ideas only: draft before tests, the snapshot of the previous version as baseline, generalising from feedback instead of patching the test case.
- **Who Validates the Validators?** (Shankar et al., 2024): https://arxiv.org/abs/2404.12272. Criteria drift: people define and revise evaluation criteria while reading outputs, which is why assertions are written after the smoke run.
- **AI Evals FAQ** (Hamel Husain and Shreya Shankar): https://hamel.dev/blog/posts/evals-faq/. Evaluators for errors discovered in real data, not imagined ones.
- **SkillsBench** (Li et al., 2026, preprint): https://arxiv.org/abs/2602.12670. Curated skills helped; skills written without running the task did not. Basis for the seed case.
- **SkillEvolver** (Zhang et al., 2026, preprint): https://arxiv.org/abs/2605.10500. A tested draft refined from real failures beat a hand-curated skill. Basis for branch B.
- **Trace2Skill** (Ni et al., 2026, preprint): https://arxiv.org/abs/2603.25158. Lessons consolidated across several runs beat editing per case: the consolidation in B step 5 and in D.
- **Agentic Context Engineering** (Zhang et al., ICLR 2026): https://arxiv.org/abs/2510.04618. Rewriting a whole playbook collapsed it and lowered accuracy below baseline: edits by delta, rewrites only through C.
- **writing-skills** (obra/superpowers, Jesse Vincent, MIT): https://github.com/obra/superpowers/tree/main/skills/writing-skills. No skill when a control run does not fail, and mechanical constraints automated instead of written: the gates in A step 2. Its strict eval-first stance is why a discipline rule always gets a scenario in B step 3.

## Triggering (A step 5)

- **AGENTS.md outperforms skills in our agent evals** (Vercel, 2026-01-27): https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals. Skills often went uninvoked, the most common measured failure, so the trigger check is never skipped.
- **Extend Claude with skills** (Claude Code): https://code.claude.com/docs/en/skills, and **Monitoring usage**: https://code.claude.com/docs/en/monitoring-usage. How invocation works and how to count it in real use (skill name in the telemetry events).

## Promotion and grading (branch C)

- **Demystifying evals for AI agents** (Anthropic, 2026-01-09): https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents. Evals built from real failures, and the cost of waiting too long to write them: promotion is the point where they are no longer optional.
- **Evaluation best practices** (OpenAI): https://developers.openai.com/api/docs/guides/evaluation-best-practices and **Testing Agent Skills Systematically with Evals**: https://developers.openai.com/blog/eval-skills. Real failures drive coverage; waiting until release to evaluate is an anti-pattern.
- **Adding Error Bars to Evals** (Miller, 2024): https://arxiv.org/abs/2411.00640. A handful of scenarios cannot measure small differences, so three scenarios are a smoke test and the user's verdict decides.
- **Large Language Models are not Fair Evaluators** (Wang et al., 2023): https://arxiv.org/abs/2305.17926. Position bias in model judges: each pair judged twice with the order swapped.

## Grounding each new rule (B step 2)

- The user's preference, from the sessions that built `reel-script` and `post-caption`, where each correction was checked against studies and official docs before it became a rule. Searched the best practices above: they support it only in part, asking that configuration values be justified (no "voodoo constants") and that skills be refined "based on observed behavior rather than assumptions"; neither speaks of grounding instructions in sources.
