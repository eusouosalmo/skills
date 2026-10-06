---
name: writing-post-captions
description: Writes the caption (post text, description) for a short video on Instagram, TikTok, YouTube Shorts or LinkedIn from its script, with a first line for search, what the video left out, one ask, source credit and hashtags within the platform's limits. Use when the user asks for a post caption or video description (legenda do reel, descrição do short, texto do post, hashtags). Not for subtitles or SRT files.
compatibility: scripts/check-caption.py needs Python 3.8+.
metadata:
  status: draft
  internal: true
---

# Writing post captions

A **caption** is the written text posted with a video: what shows under a Reel or a TikTok, the title and description of a Short, the text of a LinkedIn post with the video attached. It is not the subtitle burned into the video. Write the output in pt-BR.

The caption works next to the video, not instead of it: whoever reads it has just watched, or is deciding whether to. So it **complements** the video. It never retells the script.

## 1. Gather the context

Read the script or the video's notes. Before writing, you need:

- **platform**: Instagram, TikTok, YouTube Shorts or LinkedIn. When the request does not say, ask and wait: links, hashtags, register and what the first line does all change with it ([platforms.md](platforms.md));
- **the video's spoken ask**, usually its last line (a question for the comments, for example);
- **series**: whether the video is part of one and, if so, the next video's topic when it is already decided;
- **source**: the book, article or video the content comes from, if any, and where its link lives (bio, platform link field). When there is a link, ask whether it is commissioned (affiliate); if it is, the caption carries `#publi` in its first line.

Ask only for what the request and the script leave out. Done when the platform and the spoken ask are known and every other gap is a question to the author.

## 2. Write the caption

Read [platforms.md](platforms.md) for the chosen platform now. In order:

1. **First line: the topic and an open question.** Name the topic with the words the audience would search ("testes automatizados", "migração de banco"), because the platform search reads the caption. Then leave something open: the reader's situation or the question the video answers. Never copy the spoken hook (they just heard it) and never give away the video's answer (it closes the curiosity that makes them watch or tap "mais"). Up to about 125 characters, which is what shows before "mais" on Instagram; platforms.md says what changes elsewhere.
2. **Body: what the video did not say.** One or two short paragraphs with what did not fit in the speech: the exact name, number, command or symbol the speech had to spell out loud, a step the video skipped, a caveat. Take facts only from the script and the author's notes; a detail you know that they lack goes to "Para o autor" as a suggestion, never into the caption. A sentence that only says again what the video said leaves. State the fact, not how it was checked: the doc section, the page or "conferido na documentação" goes to "Para o autor", because it serves whoever checked, not whoever reads.
3. **One ask, different from the video's.** The video already made its ask; a caption that repeats it is a second call asking the same thing, and two asks in one post earn less than one. For eusouosalmo, the caption's ask is to follow, with the handle written out so it becomes a link: "Me segue no @eusouosalmo pra ...". When the video is part of a series, the reason is the next video: name its topic when known, otherwise "o próximo". Promise only a next video that exists or is planned. Never ask for a specific word, a tag, a share or a like ("comenta EU QUERO", "marca quem precisa ver", "compartilha se concorda"): Instagram and LinkedIn stop recommending posts that do.
4. **Source as its own last line.** "Fonte: <obra>, de <autor> (link na bio)". The source is a credit, never the subject of a sentence in the body ("o livro mostra que..."). The link mention is a pointer, not a second ask.

Done when the first line names the topic without the hook's words, every body sentence adds something the speech lacks, and the caption holds exactly one ask.

## 3. Pass it through the voice

Use the author's voice skill on the caption (for eusouosalmo, the `writing-as-eusouosalmo` skill), telling it the platform and nothing about register: it picks the register from its own table of channels. Being read does not make a caption the written register.

Done when the voice skill's own check passes.

## 4. Suggest hashtags

After the caption, suggest hashtags separately so the author decides: up to the platform's maximum (platforms.md), each one a term the audience would search for this video's topic ("#testesautomatizados", not "#tecnologia"). Specific and directly related is what every platform asks for; hashtags do not raise reach on Instagram, they only add a search term. When the author has decided on no hashtags, suggest none.

Done when every suggested hashtag names this video's topic and their count is within the platform's maximum.

## 5. Check and deliver

Save the caption to a file and run `scripts/check-caption.py <file> --platform <platform> --script <script-file>`. Fix every finding; the first-line length is a warning, since the cut-off varies by device.

Deliver:

```markdown
## Legenda (<platform>)

<the caption, ready to paste>

## Hashtags sugeridas

<up to the platform's maximum, or "nenhuma">

## Para o autor

- <every question and [falta: ...], and any fact to check before posting>
```

Before handing it over, go through [checklist.md](checklist.md). Done when the script prints "no findings" (or only the length warning) and every checklist item holds.
