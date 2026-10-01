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

Ainda não há skills publicadas. Elas aparecem conforme a necessidade aparece no trabalho real.

As instruções das skills são escritas em inglês; as skills de conteúdo entregam o resultado em português.

| Categoria | O que reúne |
|---|---|
| [content](skills/content/README.md) | Escrita, roteiro, voz e marca. Resultado em pt-BR |
| [harness](skills/harness/README.md) | Setup de repositório para trabalhar com IA com segurança, inclusive em modo AFK |

## Como o repositório funciona

Toda skill segue a [especificação Agent Skills](https://agentskills.io/specification). As convenções (nomes, maturidade, língua) estão no [AGENTS.md](AGENTS.md), e o porquê de cada uma em [docs/adr](docs/adr). A estrutura deve muito às [skills do Matt Pocock](https://github.com/mattpocock/skills).

## Licença

[MIT](LICENSE)
