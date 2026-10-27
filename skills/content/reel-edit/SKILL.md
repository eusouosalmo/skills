---
name: reel-edit
description: Edits a talking-head Reel or Short from its raw clips and script to the finished reel, as a CapCut project or a final mp4, by running the reel-cut, reel-motion and reel-finish skills in order with the author's approval between them. Use when the user hands over the raw recordings of a reel and wants it edited end to end (edição completa, do bruto ao reel pronto, edita tudo).
compatibility: Needs the reel-cut, reel-motion and reel-finish skills installed, plus what each of them needs. Multiple-choice questions use the agent's question tool when it has one (AskUserQuestion in Claude Code).
metadata:
  status: draft
  internal: true
---

# Editing reels

The author records a talking-head reel in raw clips from a script and wants the finished reel back. Three skills do the work, in this order, each with its own rules: `reel-cut` (the rough cut), `reel-motion` (scenes, overlays and their sounds) and `reel-finish` (the CapCut project or the final mp4). This skill holds what falls between them: the questions asked once, the gates, and what each step hands the next. Write every message to the author in pt-BR.

## 1. Before any heavy work

Ask what the chain depends on, in one round, before transcribing anything:

- **The script.** When the reel folder has no script, ask for it and wait. The cut splits lines and picks the take by it (register included), and the scenes take the format, the hook's visual form and the facts to check from it; without it the hook falls back to whatever the take suggests. Offer, recommended first: send the script; go on without it (the cut follows the recording and the hook form is proposed at the plan gate).
- **The output form**, unless the request names it: CapCut project (opens in the app to adjust and export; needs an empty project created in the app and CapCut closed), final mp4 (ready to post, no CapCut), or both. One answer covers the whole chain.

The cut's own form is the chain's call, not a question: the next steps need the cut video, its SRT and `cortes.json`, so tell `reel-cut` to deliver its loose files and skip its output question.

Done when the script is in the folder (or the author chose to go on without it) and the output form is known.

## 2. Run the chain

| Step | Skill | Gate: stop and wait for the author | Hands the next step |
|---|---|---|---|
| Cut | `reel-cut` | the takes table | the cut, `legenda.srt`, `cortes.json` in the reel folder |
| Scenes | `reel-motion` | the plan, then the stills | `words.json`, `timeline.md`, `exports/` |
| Finish | `reel-finish` | none of its own: the output form is already known | the project or the mp4 |

At each gate, show what the skill shows there and stop until the author answers, also when the author is away. A request for the finished reel ("edita tudo", "me entrega pronto") is the goal, not a delegation: the author asked to approve the takes and the stills, and a gate passed on an assumed answer costs a render to undo. Only an explicit delegation in the author's words ("decide por mim") lets a gate pass, and the delegation goes in `timeline.md`.

**Final mp4 and what the scenes leave to the author.** `reel-motion` leaves some choices for the author to make in CapCut, such as the sound of the impact screen. In an mp4 there is no CapCut step, so ask for each of them at the stills gate (options: a library sound from the reference project, a synthesized hit, no sound) and put the answer in the plan: left open, it ships as a silent moment the author can only fix with a new render.

Keep `edicao.md` in the reel folder, updated at each gate: the step reached, each gate's answer, the files made. The work stops at every gate and may resume in a new session or after the context is compacted, which keeps only the start of a skill invoked earlier. When resuming, read `edicao.md` first and invoke the current step's skill again.

Done when the author approved each gate and the output of the chosen form exists.
