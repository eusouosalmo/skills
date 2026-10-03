# Skills for engineering with AI

My agent skills for software architecture, programming, AI and SaaS. Some also help me create the content I make on these topics.

Generating code got cheap. What still sets software apart is the engineering around it: architecture, tests, and the harness that keeps an agent on track. These skills are how I put that into practice, in my projects and in the videos I make.

They are small, composable and born from real work: a skill only lands here after I've done the job by hand a few times. Read them, fork them, adapt them to your stack and your voice.

I share how I build with AI on [Instagram](https://www.instagram.com/eusouosalmo/) and [YouTube](https://www.youtube.com/@eusouosalmo) (@eusouosalmo) and at [eusouosalmo.dev](https://eusouosalmo.dev).

[Leia em português](README.pt-BR.md)

## Install

```bash
npx skills@latest add eusouosalmo/skills
```

The installer asks which skills to install and into which agents (Claude Code, Codex, Cursor and others). For a single skill:

```bash
npx skills@latest add eusouosalmo/skills --skill <name>
```

## Skills

- [creating-skills](skills/harness/creating-skills/SKILL.md) (beta): creates or changes a skill from an observed failure, checked with evals.

In draft, hidden from the installer:

- [setting-up-git-guardrails](skills/harness/setting-up-git-guardrails/SKILL.md): per-project git guardrails for coding agents, with interactive and AFK profiles.

| Category | What it holds |
|---|---|
| [content](skills/content/README.md) | Writing, video scripts, voice and brand. Output in pt-BR |
| [harness](skills/harness/README.md) | Setting up a repo to work with AI safely, including unattended (AFK) runs, and creating the skills it uses |

## How this repo works

Every skill follows the [Agent Skills specification](https://agentskills.io/specification). Conventions (naming, maturity, language) are in [AGENTS.md](AGENTS.md) and the reasons behind them in [docs/adr](docs/adr). The structure owes a lot to [Matt Pocock's skills](https://github.com/mattpocock/skills).

## License

[MIT](LICENSE)
