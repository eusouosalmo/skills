---
name: setup-eusouosalmo-skills
description: Sets up the eusouosalmo skills on a machine once, finding the folders and files the installed skills read (for the reel skills, the reels folder, scripts, style file, design system and CapCut projects) and writing their paths where those skills look. Use when the user installs these skills, moves to a new machine or moves one of those folders (configurar as skills, setup do kit).
disable-model-invocation: true
compatibility: disable-model-invocation is a Claude Code field; in other agents, run the skill by name. Multiple-choice questions use the agent's question tool when it has one (AskUserQuestion in Claude Code).
metadata:
  status: beta
---

# Setup of the eusouosalmo skills

Some skills of this kit read folders and files of the author's (where the reels live, the style file, the design system). This skill finds them once and writes their paths where those skills already look, so no skill asks again on every use. Write every message to the author in pt-BR.

Nothing here is required: a skill without a path asks for it or uses its default, so a first-time user can skip this skill entirely. Anyone may run it, a first-time creator or a technical user: the questions are plain multiple choice, and a path the request already gives is taken without asking.

Each **context** is a group of skills with its own paths and its own place to keep them:

| Context | Its skills | Read |
|---|---|---|
| Reels | `writing-short-video-scripts`, `cutting-raw-takes`, `animating-reel-scenes`, `finishing-reels`, `editing-reels` | [references/reels.md](references/reels.md) |

Set up a context only when at least one of its skills is installed (in the agent's skill list, or a folder next to this skill's); say which contexts were skipped and why.

The answers are private: they hold the author's machine paths and sometimes their taste. Write only where the context's file says, never into a skill folder (an installed skill may be a link into a public repository, and an update rewrites it) and never into an always-loaded file such as `~/.claude/CLAUDE.md`, which every session of every project would carry.

## 1. Explore

For each context set up, read its file and collect, for each of its keys, the candidates that exist on this machine with their evidence. Search where such things live (the home folder and the root of each mounted drive, a few levels deep), not the whole disk: a full scan of `/mnt` from WSL takes minutes.

Done when every key has its candidates or is marked as not found.

## 2. Ask, one key at a time

A path the request already gives ("o design system tá em ~/design") is the answer for its key: confirm it exists and do not ask. For each other key, ask as a multiple-choice question in plain words (what the folder is for, not the key's name), with the best candidate first, marked as recommended, and its evidence in one line; offer "outro caminho" and "não tenho", which writes `none`. A key with a single clear candidate still gets confirmed in one click: a wrong path sends every later use to the wrong place.

Done when every key has an answer.

## 3. Write

Write each context's answers as its file says. Keys stay in English, so every skill finds them; values are paths as this machine's shell sees them (`/mnt/d/...` in WSL), checked to exist. Show what will be written before writing, and on a second run say what changed against the old values; a second run replaces only this skill's block and keeps the rest of the file as it is.

Done when every context's block is written, every path in it exists (or is `none`), and the author has seen it.
