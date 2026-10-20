# Skills para engenharia com IA

Minhas skills de agente para arquitetura de software, programação, IA e SaaS. Algumas também me ajudam a criar o conteúdo que eu faço sobre esses temas.

Gerar código ficou barato. O que ainda diferencia um software é a engenharia em volta: arquitetura, testes e o harness que mantém o agente nos trilhos. Estas skills são como eu coloco isso em prática, nos meus projetos e nos vídeos que eu faço.

Elas são pequenas, combináveis e nascem do trabalho real: uma skill só entra aqui depois que fiz o trabalho na mão algumas vezes. Leia, faça fork, adapte para a sua stack e a sua voz.

Eu mostro como construo com IA no [Instagram](https://www.instagram.com/eusouosalmo/) e no [YouTube](https://www.youtube.com/@eusouosalmo) (@eusouosalmo) e em [eusouosalmo.dev](https://eusouosalmo.dev).

[Read in English](README.en.md)

## Instalação

Há dois caminhos. Escolha um: a mesma skill instalada pelos dois carrega duas vezes, uma como `<nome>` e outra como `eusouosalmo-skills:<nome>`.

Os dois instalam só as skills em beta ou stable. Os rascunhos ficam no repositório para leitura.

### Plugin do Claude Code

Versionado: você fica numa release até atualizar. Cada release e o changelog dela estão na página de [Releases](https://github.com/eusouosalmo/skills/releases).

```bash
claude plugin marketplace add eusouosalmo/skills
claude plugin install eusouosalmo-skills@eusouosalmo
```

As skills aparecem como `eusouosalmo-skills:<nome>`. Para atualizar, atualize o marketplace e depois o plugin (ou ligue a atualização automática do `eusouosalmo` em `/plugin`, Marketplaces):

```bash
claude plugin marketplace update eusouosalmo
claude plugin update eusouosalmo-skills@eusouosalmo
```

Para remover o plugin, ou o marketplace junto com o plugin:

```bash
claude plugin uninstall eusouosalmo-skills@eusouosalmo
claude plugin marketplace remove eusouosalmo
```

### npx skills, para qualquer agente

Sem versão: instala e atualiza a partir do último commit do `main`. Funciona com Claude Code, Codex, Cursor e outros agentes.

```bash
npx skills@latest add eusouosalmo/skills
```

O instalador pergunta quais skills e em quais agentes instalar. Para uma skill só, acrescente `--skill <nome>`. Para atualizar ou remover:

```bash
npx skills@latest update
npx skills@latest remove <nome>
```

## Skills

- [creating-skills](skills/harness/creating-skills/SKILL.md) (beta): cria ou altera uma skill a partir de uma falha observada, conferida com evals.
- [animating-reel-scenes](skills/content/animating-reel-scenes/SKILL.md) (beta): planeja quais trechos de um reel em talking-head viram motion e renderiza as cenas e os overlays transparentes de adesivos para o CapCut.
- [writing-short-video-scripts](skills/content/writing-short-video-scripts/SKILL.md) (beta): escreve roteiros de vídeo curto a partir das anotações do autor, com gancho, um CTA falado, texto de teleprompter cronometrado e os prints das fontes para a edição.
- [cutting-raw-takes](skills/content/cutting-raw-takes/SKILL.md) (beta): corta os brutos de um reel em talking-head num corte seco, escolhendo a tomada de cada fala e tirando bastidor e pausas longas, com uma tabela de tomadas aprovada antes do render.
- [setting-up-reel-skills](skills/content/setting-up-reel-skills/SKILL.md) (beta): configura as skills de reel numa máquina uma vez, achando a pasta dos reels, a dos roteiros, o arquivo de estilo, o design system e os projetos do CapCut e gravando os caminhos numa seção Paths do arquivo de estilo.

Em draft, fora dos dois caminhos de instalação:

- [editing-reels](skills/content/editing-reels/SKILL.md): edita um reel em talking-head dos brutos e do roteiro até o reel pronto, como projeto do CapCut ou mp4, chamando em ordem a cutting-raw-takes, a animating-reel-scenes e a finishing-reels, com a aprovação do autor entre elas.
- [finishing-reels](skills/content/finishing-reels/SKILL.md): monta o reel pronto, como projeto do CapCut ou como mp4 final sem CapCut, com o corte, os overlays das cenas, os keyframes e a divisão da tela dividida, os sfx, a abertura, os punch-ins e as palavras em destaque com som e a legenda no estilo de um projeto do próprio autor.
- [setting-up-git-guardrails](skills/harness/setting-up-git-guardrails/SKILL.md): guardrails de git por projeto para agentes de código, com perfis interativo e AFK.
- [writing-as-eusouosalmo](skills/content/writing-as-eusouosalmo/SKILL.md): escreve e revisa texto na voz do eusouosalmo, no registro falado ou escrito conforme o canal.
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
