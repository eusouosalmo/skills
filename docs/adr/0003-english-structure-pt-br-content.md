# English structure, pt-BR content

Skill names, frontmatter, instructions, repo docs and commits are in English; voice material, examples and the output of content skills are in pt-BR, and `README.pt-BR.md` mirrors the README. English matches the skills ecosystem installed alongside (flat in `~/.agents/skills`), reaches pt, en and es readers, and lets names follow the gerund form the Anthropic best practices prefer (`writing-scripts`), which sounds odd in Portuguese. The voice itself only exists in Portuguese, so its examples stay pt-BR, and the instruction language does not set the output language.

## Considered Options

- All pt-BR, names as verb + object (`escrever-roteiro`): closest to how Salmo asks, but out of step with the ecosystem and odd for technical harness skills.
- Harness in English, content in pt-BR: breaks the best practices' advice to keep one naming pattern across a collection.

## Amendment: issues and research in pt-BR

Issues (wayfinder maps and tickets) and research notes in `docs/research/` are written in pt-BR. They are planning conversation and study material whose main reader is Salmo, and the discussion happens in Portuguese. Skills, ADRs, `AGENTS.md` and commits stay in English.
