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
| spoken | video, teleprompter text, Instagram caption | "tu" ("teu", "tua", "te") | "bora lá", "macho", "o cara", "mandar a bala", "dar nome aos bois"; optional, at most one or two per text, only where eusouosalmo would say it anyway. None beats a forced one |
| written | site, article, README, LinkedIn | "você" | none |

An impersonal "você" as subject ("fica mais fácil você tirar uma ideia do papel") is fine in the spoken register; the viewer is still "tu".

Done when you have named the register. A channel not in the table: ask.

## 2. Write in the voice

Read [examples.md](examples.md) before writing in the spoken register.

- **Facts come only from the input.** Every fact, number, reason and result traces to the user's notes or draft. When the text needs one the input lacks (how it ended, why something happened), write `[falta: ...]` and ask; leave the gap open.
- **The author's story stays at the degree of the input.** A role, number or result never goes up a level ("liderei o projeto uma vez" never becomes "sou tech lead"), and hedges stay ("por exemplo", "alguns meses", "acho que"). A reader who finds one inflated detail stops trusting the rest.
- **Tell the author's story as past experience, with no date or employer.** The text is found months later and is read by colleagues: "hoje", "atual", "na empresa onde eu tô" become "quando eu precisei", "uma vez"; an employer or client name becomes a category ("num e-commerce"); internal data, identifiable people and judgements about the company leave. The problem, the public tool, what the author did and the result stay. Generalising never changes the fact: one company stays one.
- **Open with a concrete scene or the question itself**: when it happened, what you wanted, what you did. The idea comes after the scene.
- **Anchor every idea** in a real number, error or example from the input. A sentence that sums up specific things the user did or learned in a generic word ("fui aprendendo várias tecnologias") gets a `[falta: ...]` asking which ones; write it so it stands if the answer never comes, or cut it. Ask for nothing the text does not need: no new anecdote, no outcome the story works without, no example for a rule or principle the input states.
- **Keep the user's own words.** When the input names an idea in the user's words ("se aprofundar"), every sentence about that idea uses that word, including the ones you add, such as the closing question; never a synonym of yours. When repeating it sounds heavy, rewrite the sentence so it needs the word once; never swap in a synonym for variety. Any other content word that piles up (more than three times in a short text) or repeats in consecutive sentences, and any sentence said twice, gets rewritten the same way.
- **Use a metaphor only when it explains** something the audience would otherwise miss, and explain technical terms for someone starting out.
- **Tell it as one person talking**, in first person, sentences short enough to say in one breath. Short is not loose: when the next sentence is the cause, the consequence or a contrast of the previous one, join them with "porque", "então", "por isso", "mas" or "só que"; a plain sequence stays apart, without "e" glue. Plain words; honest about limits ("segundo a empresa", "não tem paper"); no hype, no guru promise, no academic jargon, no swearing.
- **Name what each sentence points to.** A sentence resting on "isso", "aquilo", "a situação", "o que já tinha" or a dry fragment ("Tinham visto.") gets its referent: what it was, who saw it.
- **Plain characters only**: commas, periods, colons and parentheses. Hyphenated lists for lists. No emoji in any channel.
- **Spoken register**: leave filler words ("basicamente", "né", "ali", "então" as filler) out of the text; they show up on their own when recording.

When reviewing, keep every fact and anchor of the draft and change how it sounds.

Done when the text is written and every fact in it traces to the input.

## 3. Check

1. Save the text to a file and run `scripts/check-voice.py <file> --register spoken|written`. Fix every finding; for "'você' in spoken register", keep only an impersonal "você".
2. Go through [checklist.md](checklist.md) for what the script cannot see.

Done when the script prints "no findings" (or only impersonal "você") and every checklist item holds. Then hand the text to the user, listing any `[falta: ...]`.
