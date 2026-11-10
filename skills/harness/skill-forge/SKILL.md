---
name: skill-forge
description: Creates an agent skill early from real work and hardens it from the corrections made in use, with evals that grow until the skill is promoted. Use when the user asks to create a skill (criar skill), fix or improve an existing one (including when its evals fail), promote one to beta or stable, or turn instructions they keep repeating into a skill.
metadata:
  status: beta
---

# Creating skills

A skill starts as a **draft** from one or two real runs of the task, and every later correction makes it harder. Rigour grows with the skill's `metadata.status`: a draft needs a seed case and a side-by-side smoke run; a correction needs a log entry and, when it can come back, a regression scenario; a promotion needs the full baseline over every scenario collected along the way. The reason: evaluation criteria only show up once outputs exist, and a skill refined from real failures beats one written in advance (see [sources.md](sources.md)).

Pick the branch that matches the request, after step 0:

- **Create**: no skill exists yet. Go to A.
- **Correct**: the user reports something a skill got wrong, or asks to improve one. Go to B.
- **Promote**: the user asks to move a skill to beta or stable, or a change rewrites most of a skill. Go to C.
- **Prune**: a skill's lessons have piled up, or it nears 500 lines. Go to D.

## 0. Read the conventions

Read the repo's `AGENTS.md` or `CLAUDE.md` for where skills live, naming, frontmatter, statuses, language and what may go in the repo. Without either, the rules are the [Agent Skills specification](https://agentskills.io/specification) and Anthropic's [skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).

Done when you know the skill's folder, its name and its current status.

## A. Create a draft

1. **Get the seed case.** A **seed case** is the task done for real at least once: a session the user reports, a run of the task without a skill on real material from the user's work (a real PR, file, script or past prompt), or instructions the user keeps pasting. Write it down as: prompt, what happened, what should have happened. Material made up for the occasion gives an imagined case: ask the user for a real one and wait.
2. **Apply the three gates**, before any file is written:
   - **One-off, no skill.** If the task will not come back, the skill never pays for itself. Say so and stop.
   - **No failure, no skill.** If the task already runs fine without a skill, say so and stop.
   - **Mechanical, no skill.** If the rule is mechanical and code can check it (a command that must always run, a format, a forbidden pattern), it belongs in a git hook, an agent hook, a script or one line of `AGENTS.md`: a skill is instructions the agent can skip, a hook runs every time. Recommend that, set it up if the user agrees, and create no skill.
3. **Write the minimum SKILL.md.** Use the `writing-for-agents` skill. Write only what turns the seed case's "what happened" into "what should have happened". The description takes the form "Does X. Use when Y.", main use case first. Set `metadata.status: draft` and whatever else the repo's conventions ask for a draft.
4. **Smoke run.** Run the seed prompt twice, each in a fresh subagent with a clean context: once without the skill, once with it. Show the user the two outputs side by side and ask which is better. No assertions yet: they come from what the outputs reveal.
5. **Trigger run**, for a model-invoked skill. Write `evals/trigger-queries.json` with three prompts that should load the skill and three near-misses, run each once on the model in use, and fix the description until the skill loads exactly when it should. A skill that never fires is the most common measured failure, so this check is never skipped.
6. **Start the log.** Create `evals/corrections.md` with the seed case as its first entry (format in [references/evals-format.md](references/evals-format.md)).

Done when the draft exists, the user preferred the run with the skill, the trigger queries pass and the log holds the seed case. Tell the user the skill now improves through use: each time they correct it, this skill takes the correction (branch B).

## B. Correct from use

1. **Log the correction.** Add an entry to the skill's `evals/corrections.md`: date, prompt, what happened, what should have happened, and the lesson in one line. Ask the user to confirm the lesson before it becomes an instruction.
2. **Ground a new rule.** When the lesson brings a rule the skill does not have yet, taste included, search before writing it: the repo's research notes, then the official docs of the tool or platform, published studies and practitioners with their own data (use the `research` skill if available). Tell the user whether what you found supports the rule, contradicts it or supports it only in part, and add the source to the skill's `sources.md`. Only when the search finds nothing, record the rule as the user's preference and name where you searched: a rule recorded as preference without a search hides whether a source exists.
3. **Decide on a scenario.** Add a scenario to `evals/evals.json` when the failure could come back unnoticed or the rule is a discipline the agent is tempted to skip. Its prompt is the logged prompt, as reported; its assertions come from what actually happened. Keep existing scenarios as they are, even one with a similar prompt.
4. **Run the baseline on the new scenario** with a snapshot of the current version, in a fresh subagent. It must fail at least one assertion, or the scenario tests nothing: rewrite it from the logged failure.
5. **Edit by delta.** Make the smallest change that fixes the cause, not the test case: the skill will meet prompts no scenario has. When several corrections are pending, consolidate them into one edit instead of one patch each. Never rewrite the whole skill in this branch; a rewrite goes through C.
6. **Run with the change** every scenario whose assertions touch the edited section, plus the new one, and show the user each output next to its baseline. When the right behaviour fails an assertion because the assertion contradicts the scenario's expected output, the assertion is the bug: fix the eval and leave the skill as it is.

Done when the log entry has its confirmed lesson, every scenario run passes, and the user's verdict on the new output is recorded in its `human_feedback` (empty means good).

## C. Promote

Read [references/evals-format.md](references/evals-format.md) now.

1. **Check the entry condition.** For beta, the log shows at least three real uses, the latest with no new correction, and `evals/evals.json` holds at least three scenarios. For stable, the last three logged uses brought no new correction. Short of that, tell the user what is missing and stop.
2. **Run the full baseline.** Every scenario once in a fresh subagent without the skill (or with the previous released version), and once with the current version. Save each report in the workspace.
3. **Grade with evidence.** A pass needs evidence quoted from the output; no evidence either way is a fail. When a model judges two outputs against each other, judge each pair twice with the order swapped and keep only verdicts that agree. The decisive verdicts, and every matter of style, are the user's: show each output next to its baseline and record their verdict in `human_feedback`.
4. **Fix and rerun.** A failure sends you to B for that scenario, then every scenario runs again.

Done when every assertion passes on every scenario, every `human_feedback` is empty, [references/checklist.md](references/checklist.md) passes, and the status moves in every place the repo's conventions list it.

## D. Prune

1. Read the skill against its log and its scenarios. Mark the lines no lesson or scenario explains, the rules said twice, and the lessons that grew into a paragraph.
2. Cut or merge the marked lines, one batch at a time, and run every scenario after each batch. A line whose removal changes no output was a no-op: it stays out.

Done when every remaining line traces to a lesson, a scenario or the repo's conventions, and every scenario still passes.
