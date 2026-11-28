---
name: reel-edit
description: Edits a talking-head Reel or Short from its raw clips and script to the finished reel, as a CapCut project or a final mp4, by running the reel-cut, reel-motion and reel-finish skills in order with the author's approval between them. Use when the user hands over the raw recordings of a reel and wants it edited end to end (edição completa, do bruto ao reel pronto, edita tudo).
compatibility: Needs the reel-cut, reel-motion and reel-finish skills installed, plus what each of them needs. scripts/edicao.py needs Python 3.8+ on Linux, macOS or WSL (it locks with fcntl). Multiple-choice questions use the agent's question tool when it has one (AskUserQuestion in Claude Code).
metadata:
  status: beta
---

# Editing reels

The author records a talking-head reel in raw clips from a script and wants the finished reel back. Three skills do the work, in this order, each with its own rules: `reel-cut` (the rough cut), `reel-motion` (scenes, overlays and their sounds) and `reel-finish` (the CapCut project or the final mp4). This skill holds what falls between them: the questions asked once, the gates, and what each step hands the next. Write every message to the author in pt-BR.

## 1. Before any heavy work

Ask what the chain depends on, in one round, before transcribing anything:

- **The script.** When the reel folder has no script, ask for it and wait. The cut splits lines and picks the take by it (register included), and the scenes take the format, the hook's visual form and the facts to check from it; without it the hook falls back to whatever the take suggests. Offer, recommended first: send the script; go on without it (the cut follows the recording and the hook form is proposed at the plan gate).
- **The output form**, unless the request names it: CapCut project (opens in the app to adjust and export; needs an empty project created in the app and CapCut closed), final mp4 (ready to post, no CapCut), or both. One answer covers the whole chain.

The cut's own form is the chain's call, not a question: the next steps need the cut video, its SRT and `cortes.json`, so tell `reel-cut` to deliver its loose files and skip its output question.

Then create the state file with `python3 scripts/edicao.py start <reel-folder> --title <title> --output capcut|mp4|both --script <file>|none`.

Done when the script is in the folder (or the author chose to go on without it), the output form is known and `edicao.md` exists.

## 2. Run the chain

| Step | Skill | Gate: stop and wait for the author | Hands the next step |
|---|---|---|---|
| Cut | `reel-cut` | the takes table | the cut, `legenda.srt`, `cortes.json` in the reel folder |
| Scenes | `reel-motion` | the plan, then the stills | `words.json`, `timeline.md`, `exports/` |
| Finish | `reel-finish` | none of its own: the output form is already known | the project or the mp4 |

At each gate, show what the skill shows there and stop until the author answers, also when the author is away. A request for the finished reel ("edita tudo", "me entrega pronto") is the goal, not a delegation: the author asked to approve the takes and the stills, and a gate passed on an assumed answer costs a render to undo. Only an explicit delegation in the author's words ("decide por mim") lets a gate pass, and the delegation goes in `timeline.md` and, as the quote, in `approve`.

**Final mp4 and what the scenes leave to the author.** `reel-motion` leaves some choices for the author to make in CapCut, such as the sound of the impact screen. In an mp4 there is no CapCut step, so ask for each of them at the stills gate (options: a library sound from the reference project, a synthesized hit, no sound) and put the answer in the plan: left open, it ships as a silent moment the author can only fix with a new render.

## 3. Record every stop with `edicao.py`

`edicao.md` in the reel folder is the edit's state: the step reached, each gate's answer in the author's words, the files made. The work stops at every gate and may resume in a new session, on another agent or after the context is compacted (which keeps only the start of a skill invoked earlier), so the state file is the only memory that survives. `scripts/edicao.py` is its only writer: it validates the file on every read and writes it whole, so a hand edit is the one way to break a resume. Each verb's flags and an example are in `python3 scripts/edicao.py <verb> --help`.

- **At each gate:** `hold --step <skill> --kind approval --reason <the gate> --file <what the author looks at>`, show the author what the gate shows, and end the turn.
- **On the author's answer:** `approve --via live --quote "<their words>"`, first-hand only, then go on. Changes asked at the gate are not an approval: redo them and show the gate again, still on hold.
- **Work only the author can do** (the empty CapCut project): `hold --kind human-step`; when they say it is done, `log` it.
- **A failure that needs a decision:** `hold --kind problem`; `log` the decision taken.
- **Work done with no stop** (the final mp4 or project): `log --step <skill> --note <what> --file <path>`.
- **Resuming:** run `status <reel-folder>` first, before anything else, then invoke the skill of its `step` again and follow its `next`.

When a verb refuses, its JSON says what to do next: follow it, and leave `edicao.md` as the verb left it.

Done when the author approved each gate, `status` shows no open stop, and the output of the chosen form exists and is logged.
