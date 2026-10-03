---
name: creating-skills
description: Creates or changes an agent skill from an observed failure, checked with evals against a baseline. Use when the user asks to create a skill (criar skill), fix or improve an existing one, or turn instructions they keep repeating into a skill.
metadata:
  status: beta
---

# Creating skills

The same six steps cover a new skill and a change to an existing one. For a change, the **baseline** is the current version and every existing scenario runs again.

## 1. Read the conventions

Read the repo's `AGENTS.md` or `CLAUDE.md` for where skills live, naming, frontmatter, language and what may go in the repo. Without either, the rules are the [Agent Skills specification](https://agentskills.io/specification) and Anthropic's [skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).

Done when you know the skill's folder and name.

## 2. Find the observed failure

An **observed failure** is something that went wrong in an actual run. It comes from one of two places:

- a session the user reports: get the prompt, what the agent did and what it should have done;
- a run of the task without the skill (for a change, with the current version) on real material from the user's work: a real PR, file, script or past prompt.

Material made up for the occasion produces an imagined failure. When there is no real case at hand, ask the user for one and wait.

Two gates, before any file is written:

- **No failure, no skill.** If the task runs fine without a skill, say so and stop.
- **Mechanical failure, no skill.** If the rule is mechanical and code can check it (a command that must always run, a format, a forbidden pattern), it belongs in a git hook, an agent hook, a script or one line of `AGENTS.md`, because a skill is instructions the agent can skip and a hook runs every time. Recommend that, set it up if the user agrees, and create no skill.

Done when each failure is written as: prompt, what happened, what should have happened.

## 3. Write the evals and run the baseline

Read [references/evals-format.md](references/evals-format.md) now.

1. Write three eval scenarios in `evals/evals.json` inside the skill folder, one per observed failure. For a change, add a new scenario for the new failure and keep the existing ones.
2. For a model-invoked skill, write `evals/trigger-queries.json`: three prompts that should trigger it and three near-misses.
3. Run each scenario once in a fresh subagent with a clean context: without the skill, or for a change, with a snapshot of the current version. Save each report in the workspace.
4. Write the assertions from what the baseline actually did, and grade the baseline.

Done when every scenario has a recorded baseline run that fails at least one assertion. A scenario the baseline already passes tests nothing: replace it. If every scenario passes, the skill adds nothing; tell the user and stop.

## 4. Write the minimum SKILL.md

Use the `writing-for-agents` skill for the writing. Write only what turns the baseline's failed assertions into passes; for a change, the smallest diff that fixes the new failure. The description takes the form "Does X. Use when Y.", main use case first.

Done when every failed assertion maps to an instruction in the skill.

## 5. Run with the skill and compare

1. Run every scenario with the skill in a fresh subagent and grade it the same way. For a change, that means old and new scenarios.
2. Run each trigger query once on the model in use and check that the skill loads exactly when it should. The full protocol (about 20 queries, several runs, train and validation split) is for when the trigger fails in real use; if the `skill-creator` skill is available, use it for that.
3. Show the user each output next to its baseline and record their verdict in the scenario's `human_feedback`. Style is the user's call; leave it ungraded.

If the difference between the two runs is unclear, run that scenario again.

## 6. Iterate and finish

Fix the cause, not the test case: the skill will meet prompts the scenarios never had. After each fix, run every scenario again.

Done when every assertion passes on every scenario, every `human_feedback` is empty, and [references/checklist.md](references/checklist.md) passes.
