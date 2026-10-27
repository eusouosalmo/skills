# Final checklist

A summary, in this skill's own words, of the checklist in Anthropic's skill authoring best practices, plus the Agent Skills specification limits. The repo's own conventions (read in step 1) come on top.

## Frontmatter

- `name` equals the folder name: lowercase letters, digits and hyphens, up to 64 characters, no leading, trailing or double hyphen, no reserved word (`claude`, `anthropic`).
- `description` up to 1,024 characters, third person, saying what the skill does and when to use it, with the words a user would type. Main use case first.
- Fields outside the spec (`name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`) are declared in `compatibility` with the agent they need.

## Body

- `SKILL.md` under 500 lines. Material that only some runs need sits in a separate file, linked straight from `SKILL.md` with the condition for reading it.
- Every supporting file is one level deep. A file over 100 lines starts with a table of contents.
- Every step ends on a condition the agent can check.
- One term per concept, the same one everywhere.
- One default per choice, with an escape hatch only when needed.
- Examples are concrete. No dated instructions ("until August, use..."); old behaviour goes in a section of its own.
- Paths use forward slashes.

## Scripts (when the skill has any)

- A script handles its own errors and says what went wrong.
- Every constant has a reason written next to it.
- Dependencies are listed and checked before use.
- `SKILL.md` says whether to run each script or read it.
- Destructive or batch operations go through plan, validate, execute.

## Evals

- Three scenarios, each from an observed failure, each failing its baseline.
- Every scenario passes with the skill, and every `human_feedback` is empty.
- For a change: every scenario that existed before still passes.
- For a model-invoked skill: the trigger queries pass.
- Run on every model the skill is meant for; by default, the model in use.
