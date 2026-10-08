# Skills for engineering with AI

My agent skills for software architecture, programming, AI and SaaS. Some also help me create the content I make on these topics.

Generating code got cheap. What still sets software apart is the engineering around it: architecture, tests, and the harness that keeps an agent on track. These skills are how I put that into practice, in my projects and in the videos I make.

They are small, composable and born from real work: a skill only lands here after I've done the job by hand a few times. Read them, fork them, adapt them to your stack and your voice.

I share how I build with AI on [Instagram](https://www.instagram.com/eusouosalmo/) and [YouTube](https://www.youtube.com/@eusouosalmo) (@eusouosalmo) and at [eusouosalmo.dev](https://eusouosalmo.dev).

[Leia em português](README.pt-BR.md)

## Install

Two ways in. Pick one: installing the same skill both ways loads it twice, once as `<name>` and once as `eusouosalmo-skills:<name>`.

Both install only the skills in beta or stable. Drafts stay in the repo to read.

### Claude Code plugin

Versioned: you stay on a release until you update. Each release and its changelog are on the [Releases](https://github.com/eusouosalmo/skills/releases) page.

```bash
claude plugin marketplace add eusouosalmo/skills
claude plugin install eusouosalmo-skills@eusouosalmo
```

Skills show up as `eusouosalmo-skills:<name>`. To update, refresh the marketplace and then the plugin (or turn on auto-update for `eusouosalmo` under `/plugin`, Marketplaces):

```bash
claude plugin marketplace update eusouosalmo
claude plugin update eusouosalmo-skills@eusouosalmo
```

To remove the plugin, or the marketplace together with its plugin:

```bash
claude plugin uninstall eusouosalmo-skills@eusouosalmo
claude plugin marketplace remove eusouosalmo
```

### npx skills, for any agent

Not versioned: it installs and updates from the latest commit on `main`. Works with Claude Code, Codex, Cursor and other agents.

```bash
npx skills@latest add eusouosalmo/skills
```

The installer asks which skills to install and into which agents. For a single skill, add `--skill <name>`. To update or remove:

```bash
npx skills@latest update
npx skills@latest remove <name>
```

## Skills

- [creating-skills](skills/harness/creating-skills/SKILL.md) (beta): creates or changes a skill from an observed failure, checked with evals.
- [animating-reel-scenes](skills/content/animating-reel-scenes/SKILL.md) (beta): plans which stretches of a talking-head reel become motion and renders the scenes and transparent sticker overlays for CapCut.

In draft, not installed by either path:

- [setting-up-git-guardrails](skills/harness/setting-up-git-guardrails/SKILL.md): per-project git guardrails for coding agents, with interactive and AFK profiles.
- [writing-as-eusouosalmo](skills/content/writing-as-eusouosalmo/SKILL.md): writes and reviews text in the voice of eusouosalmo, spoken or written register by channel.
- [writing-short-video-scripts](skills/content/writing-short-video-scripts/SKILL.md): writes short video scripts from the author's notes, with hook, one spoken CTA and timed teleprompter text.
- [writing-post-captions](skills/content/writing-post-captions/SKILL.md): writes the caption for a short video on Instagram, TikTok, YouTube Shorts or LinkedIn from its script, complementing the video with one ask, source credit and hashtags within the platform's limits.

| Category | What it holds |
|---|---|
| [content](skills/content/README.md) | Writing, video scripts, voice and brand. Output in pt-BR |
| [harness](skills/harness/README.md) | Setting up a repo to work with AI safely, including unattended (AFK) runs, and creating the skills it uses |

## How this repo works

Every skill follows the [Agent Skills specification](https://agentskills.io/specification). Conventions (naming, maturity, language) are in [AGENTS.md](AGENTS.md) and the reasons behind them in [docs/adr](docs/adr). The structure owes a lot to [Matt Pocock's skills](https://github.com/mattpocock/skills).

## License

[MIT](LICENSE)
