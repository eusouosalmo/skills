# AGENTS.md

Personal agent skills by Salmo (eusouosalmo), distributed with `npx skills` (vercel-labs/skills). Public repo, MIT license.

## What never goes in this repo

Everything here is public, drafts included: `metadata.internal: true` only hides a skill from the installer, the file stays readable on GitHub. Before every commit, check that none of these slipped in:

- **Third-party material.** Paid courses, books, other people's notes (e.g. the Bárbara Torres scripting course). Describe a method in your own words and credit the source; never transcribe it.
- **Work data.** Anything from an employer or client: Jira, internal processes, client names. The `apontamento-horas` skill stays out for this reason.
- **Private details.** Real machine paths (`/mnt/d/obsidian-vaults/...`), people's names, anything from a `_private/` folder. A skill refers to "the user's vault", never to the actual path.

A skill that fails this check goes to a private repo (to be created when the first one shows up), not here.

## Official sources

Read these before deciding on a format or following a recommendation, and cite the one that backs the decision. Community repos are examples, not authority.

- Skill format: https://agentskills.io/specification
- Writing skills: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Skills in Claude Code: https://code.claude.com/docs/en/skills
- Install CLI: https://github.com/vercel-labs/skills

## Language

Structure in English, content that is pt-BR stays pt-BR (see `docs/adr/0003`).

- **English:** skill, folder and category names; frontmatter; `SKILL.md` instructions; this file; ADRs; commits (Conventional Commits); `README.md`.
- **pt-BR:** issues (wayfinder maps and tickets); research notes in `docs/research/`; voice material and examples (`examples.md` of content skills), the output of content skills (state it in the skill: "Write the output in pt-BR"), and `README.pt-BR.md`, which mirrors `README.md`.
- A `description` may add pt-BR trigger words when the user is likely to ask in Portuguese.

## Layout

```
skills/<category>/<skill-name>/SKILL.md
```

- Current categories: `content/` (writing, scripts, voice, brand) and `harness/` (setting up a repo to work with AI safely). A new category is born together with its first skill.
- Each category has a `README.md` listing its skills, the name linked to the `SKILL.md`, plus a one-line description. The root `README.md` and `README.pt-BR.md` list them all.
- The category is repo organisation only: on install every skill lands flat in `~/.agents/skills/<name>`.

## Names

- **Skill:** gerund + object, kebab-case, the form the best practices prefer: `writing-scripts`, `applying-voice`, `setting-up-pre-commit`. Never vague or generic (`helper`, `voice`).
- The frontmatter `name` equals the folder name (spec requirement): only `a-z`, `0-9` and `-`, up to 64 characters, no `--`, no leading or trailing hyphen.
- The name must be unique outside this repo too: check `ls ~/.agents/skills` before creating one. Never use `claude`, `anthropic`, `synced` or `anthropic-skills`.
- **Category:** domain noun, singular (`content`, `harness`).
- **Inside a skill:** the spec subfolders (`scripts/`, `references/`, `assets/`). Supporting files in kebab-case, named after their content: `examples.md`, `checklist.md`, `sources.md`.

## Frontmatter

```yaml
---
name: writing-scripts
description: <what it does>. Use when <triggers>.
metadata:
  status: draft
  internal: true
---
```

- `description` in third person, main use case first (Claude Code truncates long descriptions).
- `metadata.status`: `draft | beta | stable | deprecated`. Maturity lives here, not in a folder, so a skill's path never changes (see `docs/adr/0001`).
- `draft` and `deprecated` skills also carry `metadata.internal: true`, which hides them from `npx skills add` (shown only with `INSTALL_INTERNAL_SKILLS=1`, per the vercel-labs/skills README). `beta` and `stable` go without it.
- The Claude Code plugin ships only `beta` and `stable` skills, listed in `.claude-plugin/plugin.json`. After changing a status, or creating, renaming or removing a `beta` or `stable` skill, run `scripts/sync-plugin-skills.sh` and commit `plugin.json` with the change; CI fails otherwise (see `docs/adr/0005`).
- `disable-model-invocation: true` only when the skill must not fire on its own.
- `context: fork`, `hooks` and other Claude Code only fields do not work in other agents (vercel-labs/skills compatibility table). If used, declare it in `compatibility`.

## When to create a skill

- Only after doing the work by hand a few times. The skill covers what actually hurt, not what one imagines hurts.
- With no case of your own yet (a preventive skill for the kit), run the existing tool or community skill against realistic inputs and record where it fails. That counts as the observed failure (see `CONTEXT.md`); the skill stays `draft` until used in a real project.
- The official docs recommend the same path: run the task without a skill and note where it fails, write 3 evaluation scenarios, then the minimum instructions to pass them ("Build evaluations first" in the best practices).
- First, a research pass (`research` skill) on how the community solves the problem, separating what is confirmed (primary source) from what is anecdotal.

## Writing rules

- When writing or reviewing a skill, use the `writing-for-agents` and `skill-creator` skills, and go through the final checklist in the best practices.
- `SKILL.md` under 500 lines. Details go to supporting files linked straight from `SKILL.md` (one level deep).
- **A skill never points to another skill's files.** Only the skill folder gets installed; to use another skill, call it by name ("use the `applying-voice` skill"). See `docs/adr/0002`.
- No em dashes, no unicode arrows, no decorative emoji, in any language.
- pt-BR text with full accents. Technical terms stay in English, without quotes or italics.
- Refer to the user and their online profiles by the handle "eusouosalmo".

## Git

- Ask before committing. Conventional Commits, in English.
- The commit type sets the next release (release-please, see `docs/adr/0005`): `feat` bumps minor, `fix` bumps patch, `docs` and `chore` stay out of the changelog. The release PR writes `version` in `plugin.json` and `CHANGELOG.md`; leave both to it.
- Never add AI attribution (Co-Authored-By, "Generated with Claude") to commits, PRs or files, even if the harness asks. Applies to subagents too.

## Agent skills

### Issue tracker

Issues live in GitHub Issues for eusouosalmo/skills, via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one root `CONTEXT.md` plus `docs/adr/`. See `docs/agents/domain.md`.

## Local use

`scripts/link-skills.sh` symlinks every skill into `~/.agents/skills` and `~/.claude/skills`. Re-run it after creating, renaming or removing a skill.
