# Skills para engenharia com IA

Minhas skills de agente para arquitetura de software, programação, IA e SaaS. Algumas também me ajudam a criar o conteúdo que eu faço sobre esses temas.

Gerar código ficou barato. O que ainda diferencia um software é a engenharia em volta: arquitetura, testes e o harness que mantém o agente nos trilhos. Estas skills são como eu coloco isso em prática, nos meus projetos e nos vídeos que eu faço.

Elas são pequenas, combináveis e nascem do trabalho real: uma skill só entra aqui depois que fiz o trabalho na mão algumas vezes. Leia, faça fork, adapte para a sua stack e a sua voz.

Eu mostro como construo com IA no [Instagram](https://www.instagram.com/eusouosalmo/) e no [YouTube](https://www.youtube.com/@eusouosalmo) (@eusouosalmo) e em [eusouosalmo.dev](https://eusouosalmo.dev).

[Read in English](README.md)

## Instalação

```bash
npx skills@latest add eusouosalmo/skills
```

O instalador pergunta quais skills e em quais agentes instalar (Claude Code, Codex, Cursor e outros). Para uma skill só:

```bash
npx skills@latest add eusouosalmo/skills --skill <nome>
```

## Skills

- [creating-skills](skills/harness/creating-skills/SKILL.md) (beta): cria ou altera uma skill a partir de uma falha observada, conferida com evals.

Em draft, escondidas do instalador:

- [setting-up-git-guardrails](skills/harness/setting-up-git-guardrails/SKILL.md): guardrails de git por projeto para agentes de código, com perfis interativo e AFK.
- [writing-as-eusouosalmo](skills/content/writing-as-eusouosalmo/SKILL.md): escreve e revisa texto na voz do eusouosalmo, no registro falado ou escrito conforme o canal.
- [writing-short-video-scripts](skills/content/writing-short-video-scripts/SKILL.md): escreve roteiros de vídeo curto a partir das anotações do autor, com gancho, um CTA falado e texto de teleprompter cronometrado.
- [writing-post-captions](skills/content/writing-post-captions/SKILL.md): escreve a legenda de um vídeo curto para Instagram, TikTok, YouTube Shorts ou LinkedIn a partir do roteiro, complementando o vídeo com um pedido, crédito da fonte e hashtags dentro do limite da plataforma.

As instruções das skills são escritas em inglês; as skills de conteúdo entregam o resultado em português.

| Categoria | O que reúne |
|---|---|
| [content](skills/content/README.md) | Escrita, roteiro, voz e marca. Resultado em pt-BR |
| [harness](skills/harness/README.md) | Setup de repositório para trabalhar com IA com segurança, inclusive em modo AFK, e criação das skills que o agente usa |

## Como o repositório funciona

Toda skill segue a [especificação Agent Skills](https://agentskills.io/specification). As convenções (nomes, maturidade, língua) estão no [AGENTS.md](AGENTS.md), e o porquê de cada uma em [docs/adr](docs/adr). A estrutura deve muito às [skills do Matt Pocock](https://github.com/mattpocock/skills).

## Licença

[MIT](LICENSE)
