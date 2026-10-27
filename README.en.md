# eusouosalmo's skills

Skills that teach your AI agent (Claude Code, Codex, Cursor and others) to do two jobs well: build and protect a project's code with AI, and produce short video from script to finished reel.

Each skill was born from work I did by hand a few times, and is tested against the same agent without it: only what changes the result stays.

[Leia em português](README.md)

## Get started in three steps

1. Install:

   ```bash
   npx skills@latest add eusouosalmo/skills
   ```

   The installer asks which skills to install and into which agents. Prefer the Claude Code plugin, which is versioned? See [other ways to install](#other-ways-to-install).

2. Going to use the reel skills? Run `/setup-eusouosalmo-skills` once. It finds your folders (reels, scripts, style, CapCut) and saves their paths, so no skill asks again.

3. Ask in plain words. The agent picks the skill from the request:

   - "write a reel script about Postgres indexes from these notes"
   - "cut the raw clips in this reel's folder and drop the bad takes"
   - "the agent forgot to run the tests again, turn this into a skill"

## Skills

### Short video, from script to post

In the order they enter a reel. All deliver their output in Portuguese.

1. [reel-script](skills/content/reel-script/SKILL.md) (beta): writes the script from your notes, with hook, one spoken CTA, timed teleprompter text and prints of its sources for the edit.
2. [reel-cut](skills/content/reel-cut/SKILL.md) (beta): joins the raw clips into a rough cut, picking the take to keep for each line and dropping backstage talk and long pauses, with a takes table approved before rendering.
3. [reel-motion](skills/content/reel-motion/SKILL.md) (beta): decides which stretches become animation and renders the scenes and sticker overlays, timed to each spoken word.
4. [reel-finish](skills/content/reel-finish/SKILL.md) (draft): puts the finished reel together, as a CapCut project or as the final mp4 without CapCut, with captions, sounds, punch-ins and split screen in the style of one of your projects.
5. [post-caption](skills/content/post-caption/SKILL.md) (draft): writes the post caption for Instagram, TikTok, YouTube Shorts or LinkedIn, with one ask, source credit and hashtags within the platform's limits.

And the ones working around that sequence:

- [reel-edit](skills/content/reel-edit/SKILL.md) (draft): does the whole edit, from raw clips to finished reel, running reel-cut, reel-motion and reel-finish in order, with your approval between them.
- [eusouosalmo-voice](skills/content/eusouosalmo-voice/SKILL.md) (draft): writes and reviews text in my voice, spoken or written by channel. A model for building a skill of your own voice.
- [setup-eusouosalmo-skills](skills/content/setup-eusouosalmo-skills/SKILL.md) (beta): sets up the kit on a machine once, finding the folders and files the skills read.

### Engineering with AI

- [skill-forge](skills/harness/skill-forge/SKILL.md) (beta): creates or fixes a skill from a failure you saw happen, checked with evals against the agent without the skill.
- [git-guardrails](skills/harness/git-guardrails/SKILL.md) (draft): installs, per project, a hook that stops the agent from running destructive git, with interactive and AFK profiles.

**Status:** `beta` and `stable` are installed by both paths. `draft` is still being tested and stays in the repo, to read or copy.

## Why these skills

Generating code got cheap. What still sets software apart is the engineering around it: architecture, tests, and the harness that keeps an agent on track. Content is the same: an agent writes a script in seconds, but it comes out generic, with unsourced facts and a weak hook.

A skill here is what I learned correcting the agent, written so it does not make the same mistake again. They are small and composable: read them, fork them, adapt them to your stack and your voice.

I share how I build with AI on [Instagram](https://www.instagram.com/eusouosalmo/), [YouTube](https://www.youtube.com/@eusouosalmo) and at [eusouosalmo.dev](https://eusouosalmo.dev).

## Other ways to install

Two ways in. Pick one: installing the same skill both ways loads it twice, once as `<name>` and once as `eusouosalmo-skills:<name>`.

<details>
<summary>npx skills, for any agent (not versioned)</summary>

Installs and updates from the latest commit on `main`. For a single skill, add `--skill <name>`. To update or remove:

```bash
npx skills@latest update
npx skills@latest remove <name>
```

</details>

<details>
<summary>Claude Code plugin (versioned)</summary>

You stay on a release until you update. Each release and its changelog are on the [Releases](https://github.com/eusouosalmo/skills/releases) page.

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

</details>

## How this repo works

Every skill follows the [Agent Skills specification](https://agentskills.io/specification). Skill instructions are written in English; content skills deliver their output in Portuguese. Conventions (naming, maturity, language) are in [AGENTS.md](AGENTS.md) and the reasons behind them in [docs/adr](docs/adr). The structure owes a lot to [Matt Pocock's skills](https://github.com/mattpocock/skills).

## License

[MIT](LICENSE)
