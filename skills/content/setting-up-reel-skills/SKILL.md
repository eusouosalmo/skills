---
name: setting-up-reel-skills
description: Sets up the reel skills on a machine once, finding the author's reels folder, scripts folder, style file, design system and CapCut projects and writing their paths into a Paths section of the style file at the root of the reels folder. Use when the user installs the reel skills, moves to a new machine or moves one of those folders (configurar o kit de reels, setup das skills).
disable-model-invocation: true
compatibility: disable-model-invocation is a Claude Code field; in other agents, run the skill by name. Multiple-choice questions use the agent's question tool when it has one (AskUserQuestion in Claude Code).
metadata:
  status: draft
  internal: true
---

# Setting up the reel skills

The reel skills (`writing-short-video-scripts`, `cutting-raw-takes`, `animating-reel-scenes`, `finishing-reels`, `editing-reels`) work inside a reel folder and read the author's style file, `estilo.md`, at the root of the reels folder, one level above every reel. This skill puts the style file there and writes into it where everything else lives, so no skill has to ask again. Write every message to the author in pt-BR.

Nothing here is required: a reel skill without a path asks for it or uses its default, so a first-time creator with no style file, design system or CapCut project can skip this skill entirely. What it saves is the same questions on every reel.

The style file is private: it holds the author's taste and their machine's paths. Write only there, never into a skill folder (an installed skill may be a link into a public repository, and an update rewrites it) and never into an always-loaded file such as `~/.claude/CLAUDE.md`, which every session of every project would carry.

## 1. Explore

Look before asking. For each path, collect the candidates that exist on this machine, with the evidence:

| Key | What it is | Evidence |
|---|---|---|
| `reels` | the folder holding one subfolder per reel | subfolders with `brutos/`, `timeline.md`, `legenda.srt` or `exports/` |
| `scripts` | where the author keeps video scripts | Markdown files with a `## Teleprompter` or `# Roteiro:` heading, often in a notes vault |
| `style_file` | the current `estilo.md` | a file named `estilo.md`; a `timeline.md` line "Estilo:" pointing to it |
| `design_system` | the tokens and components scenes are drawn with | a folder with `tokens.css` or a `project/` export; a `timeline.md` line "Design system:" |
| `capcut_drafts` | CapCut desktop's projects folder | `<user>/AppData/Local/CapCut/User Data/Projects/com.lveditor.draft/`, under `/mnt/<drive>/Users/` in WSL |
| `capcut_reference_project` | the author's project whose editing style the finished reel copies | a project the style file or a `timeline.md` names as "Referência" or "molde" |

Search where these live (the home folder and the root of each mounted drive, a few levels deep), not the whole disk: a full scan of `/mnt` from WSL takes minutes.

Done when every key has its candidates or is marked as not found.

## 2. Ask, one key at a time

A path the request already gives ("o design system tá em ~/design") is the answer for its key: confirm it exists and do not ask. For each other key, ask as a multiple-choice question with the best candidate first, marked as recommended, and its evidence in one line; offer "outro caminho" and "não tenho", which writes `none`. A key with a single clear candidate still gets confirmed in one click: a wrong path here sends every later reel to the wrong place.

Done when every key has an answer.

## 3. Put the style file at the root of the reels folder

- **It lives elsewhere:** move it to `<reels>/estilo.md` and leave a symbolic link at the old place, so whatever pointed there (a script, an eval) still finds it. Say both paths.
- **There is none:** create `<reels>/estilo.md` with a title and the Paths section only; the skills fill in the author's taste from their verdicts.
- **It is already there:** leave it.

Done when `<reels>/estilo.md` exists and is the only real copy.

## 4. Write the Paths section

Write this block right after the file's title. Keys stay in English, so every skill finds them; values are paths as this machine's shell sees them (`/mnt/d/...` in WSL), checked to exist:

```markdown
## Paths

Written by setting-up-reel-skills on <date>. Run it again after moving a folder or on a new machine.

- reels: <path>
- scripts: <path or "none">
- design_system: <path or "none">
- capcut_drafts: <path or "none">
- capcut_reference_project: <project name or "none">
```

Running again replaces only this block and keeps the rest of the file as it is. Show the block before writing and say what changed against the old one.

Done when the block is in the file, every path in it exists (or is `none`), and the author has seen it.
