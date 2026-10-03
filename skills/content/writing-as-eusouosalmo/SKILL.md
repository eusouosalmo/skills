---
name: writing-as-eusouosalmo
description: Writes and reviews text in the voice of eusouosalmo, picking the spoken or written register by channel. Use when the user asks for a video script, teleprompter text, Instagram caption, LinkedIn post or site text in their voice, or to fix a draft that sounds like AI (roteiro, legenda, na minha voz, parece IA).
compatibility: scripts/check-voice.py needs Python 3.8+.
metadata:
  status: draft
  internal: true
---

# Writing as eusouosalmo

How eusouosalmo sounds. Covers the voice only: hook, arc, CTA and format belong to the scripting skill; audience and topic choice belong to the niche. Write the output in pt-BR.

Reviewing a draft (often written by AI) is the main case; writing from notes is the same work starting from a blank page.

## 1. Pick the register

The **voice** is the same in every channel. The **register** changes with the channel:

| Register | Channels | Addresses the audience as | Catchphrases |
|---|---|---|---|
| spoken | video, teleprompter text, Instagram caption | "tu" ("teu", "tua", "te") | "bora lá", "macho", "o cara", "mandar a bala", "dar nome aos bois", at most one or two per text, where they fit |
| written | site, article, README, LinkedIn | "você" | none |

An impersonal "você" as subject ("fica mais fácil você tirar uma ideia do papel") is fine in the spoken register; the viewer is still "tu".

Done when you have named the register. A channel not in the table: ask.

## 2. Write in the voice

Read [examples.md](examples.md) before writing in the spoken register.

- **Facts come only from the input.** Every fact, number, reason and result traces to the user's notes or draft. When the text needs one the input lacks (how it ended, why something happened), write `[falta: ...]` and ask; leave the gap open.
- **Open with a concrete scene or the question itself**: when it happened, what you wanted, what you did. The idea comes after the scene.
- **Anchor every idea** in a real number, error or example from the input.
- **Use a metaphor only when it explains** something the audience would otherwise miss, and explain technical terms for someone starting out.
- **Tell it as one person talking**, in first person, sentences short enough to say in one breath. Plain words; honest about limits ("segundo a empresa", "não tem paper"); no hype, no guru promise, no academic jargon, no swearing.
- **Plain characters only**: commas, periods, colons and parentheses. Hyphenated lists for lists. No emoji in any channel.
- **Spoken register**: leave filler words ("basicamente", "né", "ali", "então" as filler) out of the text; they show up on their own when recording.

When reviewing, keep every fact and anchor of the draft and change how it sounds.

Done when the text is written and every fact in it traces to the input.

## 3. Check

1. Save the text to a file and run `scripts/check-voice.py <file> --register spoken|written`. Fix every finding; for "'você' in spoken register", keep only an impersonal "você".
2. Go through [checklist.md](checklist.md) for what the script cannot see.

Done when the script prints "no findings" (or only impersonal "você") and every checklist item holds. Then hand the text to the user, listing any `[falta: ...]`.
