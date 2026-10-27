# README de repositório de skills

Resumo: os repositórios de skills mais vistos resolvem a primeira tela de dois jeitos. Os de autor (mattpocock/skills, obra/superpowers) abrem com uma frase de posicionamento e um parágrafo de porquê, e mandam para a instalação logo depois. Os de produto (AgriciDaniel/claude-seo, AgriciDaniel/claude-ads, Nutlope/hallmark, affaan-m/ECC) abrem com uma imagem larga, um título, uma linha que diz o resultado para quem usa e, em seguida, um quickstart ou uma demonstração. Quase todos dizem em uma frase o que o repositório faz e para quem, antes de qualquer comando. O que mais falta no README atual deste repo, comparado a eles: uma frase de abertura que diga o que a pessoa ganha (hoje a primeira frase diz o tema, não o resultado), um exemplo do que pedir ao agente, e a instalação mais curta logo no começo (hoje o caminho do plugin, com atualizar e remover, vem antes do `npx skills`, que é o mais curto). Imagem de cabeçalho é comum nos repositórios de produto e rara nos de autor; quando aparece, é larga (de 1200 a 2400 px de largura), muitas vezes com variante clara e escura via `<picture>`. O GitHub recomenda 1280 por 640 para a imagem de prévia em redes sociais, que é outra coisa, mas a mesma arte pode servir aos dois. Pesquisa de 2026-10-27, para a reescrita do `README.md` e do `README.en.md`. Não decide nada; a seção 6 lista as recomendações e a seção 7 os prompts de imagem.

## Sumário

1. [Fontes e método](#1-fontes-e-método)
2. [O que o README atual mostra](#2-o-que-o-readme-atual-mostra)
3. [Repositório por repositório](#3-repositório-por-repositório)
4. [Orientação oficial sobre README](#4-orientação-oficial-sobre-readme)
5. [Padrões que se repetem](#5-padrões-que-se-repetem)
6. [Recomendações para este repo](#6-recomendações-para-este-repo)
7. [Imagem de cabeçalho e prompts](#7-imagem-de-cabeçalho-e-prompts)

## 1. Fontes e método

Li o `README.md` de cada repositório no ramo padrão, baixado de `raw.githubusercontent.com` em 2026-10-27, e medi as imagens de cabeçalho baixando o arquivo (PNG pelo cabeçalho do arquivo, SVG pelo `viewBox`). Os repositórios de autor foram escolhidos pelo pedido; os demais pela busca da API do GitHub por "claude skills", ordenada por estrelas, mais os que têm imagem de cabeçalho. Os READMEs são exemplos, não autoridade (AGENTS.md); o que é recomendação vem da seção 4.

| Sigla | Fonte | Tipo |
| - | - | - |
| MPS | [mattpocock/skills, README](https://github.com/mattpocock/skills) | exemplo (autor) |
| ANT | [anthropics/skills, README](https://github.com/anthropics/skills) | exemplo (oficial da Anthropic, mas como repositório, não como guia de README) |
| SUP | [obra/superpowers, README](https://github.com/obra/superpowers) | exemplo (autor) |
| VAS | [vercel-labs/agent-skills, README](https://github.com/vercel-labs/agent-skills) | exemplo (empresa) |
| VSK | [vercel-labs/skills, README](https://github.com/vercel-labs/skills) | exemplo (CLI, não coleção) |
| SEO | [AgriciDaniel/claude-seo, README](https://github.com/AgriciDaniel/claude-seo) | exemplo (produto, com imagem) |
| ADS | [AgriciDaniel/claude-ads, README](https://github.com/AgriciDaniel/claude-ads) | exemplo (produto, com imagem) |
| MKT | [coreyhaines31/marketingskills, README](https://github.com/coreyhaines31/marketingskills) | exemplo (autor, conteúdo e marketing) |
| HAL | [Nutlope/hallmark, README](https://github.com/Nutlope/hallmark) | exemplo (produto, com imagem) |
| ECC | [affaan-m/ECC, README](https://github.com/affaan-m/ECC) | exemplo (produto, com imagem) |
| KDS | [K-Dense-AI/scientific-agent-skills, README](https://github.com/K-Dense-AI/scientific-agent-skills) | exemplo (coleção grande) |
| GHR | [GitHub Docs, About the repository README file](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) | primária |
| GHS | [GitHub Docs, Customizing your repository's social media preview](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview) | primária |
| GHP | [GitHub Docs, Basic writing and formatting syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) (seção Images e The Picture element) | primária |
| GHC | [GitHub Changelog, Specify theme context for images in Markdown GA (2022-08-15)](https://github.blog/changelog/2022-08-15-specify-theme-context-for-images-in-markdown-ga/) | primária |
| MAR | [makeareadme.com](https://www.makeareadme.com/), seção "Suggestions for a good README" | secundária (guia da comunidade) |

**O repositório "algaera".** Não achei repositório com esse nome. O candidato mais provável é **AgriciDaniel** (Agrici Daniel), cujo som se aproxima e cujos dois repositórios de skills mais estrelados (claude-seo e claude-ads) abrem com imagem de cabeçalho grande. Inferência pelo som do nome; vale confirmar com o dono.

## 2. O que o README atual mostra

Lido em [README.md](../../README.md) no commit `340fd73`.

- **Primeira tela:** título "Skills para engenharia com IA", sem imagem e sem badge. Três parágrafos: o tema ("arquitetura de software, programação, IA e SaaS", mais conteúdo), a tese ("gerar código ficou barato"), e como as skills nascem ("só entra aqui depois que fiz o trabalho na mão"). Depois, os links para Instagram, YouTube e site, e o link para a versão em inglês.
- **Instalação:** vem antes da lista de skills. Abre com um aviso sobre não instalar pelos dois caminhos, depois o plugin do Claude Code com instalar, atualizar e remover (seis comandos), e só então o `npx skills`, que é um comando.
- **Lista:** uma lista com marcador por skill, com status entre parênteses e uma linha de descrição; os rascunhos numa segunda lista; uma tabela de categorias no fim. As skills de engenharia e as de conteúdo aparecem misturadas na mesma lista.
- **Falta:** um exemplo do que pedir ao agente, um passo de setup depois de instalar (a `setup-eusouosalmo-skills` existe, mas está no fim da lista), e qualquer imagem ou demonstração.

## 3. Repositório por repositório

### mattpocock/skills (MPS)

- **Primeira tela:** logo pequena com variante clara e escura via `<picture>` e `prefers-color-scheme`, exibida com `width="369"`; o arquivo é PNG de 738 por 388 (2x). A logo é link para a newsletter. Título "Skills For Real Engineers", um badge do skills.sh.
- **Primeiros parágrafos:** uma frase de posicionamento ("My agent skills that I use every day to do real engineering - not vibe coding"), um parágrafo que nomeia a alternativa e o problema dela (GSD, BMAD e Spec-Kit "take away your control"), um parágrafo de valores (pequenas, adaptáveis, combináveis, qualquer modelo) e a chamada para a newsletter.
- **Instalação:** título "Installation (30-second setup)", em três passos numerados: pegar as skills (um `<details>` recolhido por agente: Claude Code, Codex, Copilot, Gemini, qualquer outro via `npx skills`), rodar `/setup-matt-pocock-skills`, e "Bam - you're ready to go". Uma frase antes explica a diferença entre plugin (atualiza sozinho) e skills.sh (arquivos editáveis) e avisa para não instalar os dois.
- **Porquê:** seção "Why These Skills Exist" organizada por falha do agente ("#1: The Agent Didn't Do What I Want", "#2: The Agent Is Way Too Verbose"...), cada uma com "The Problem" e "The Fix" apontando para as skills que resolvem.
- **Lista:** seção "Reference", por categoria (Engineering, Productivity), uma linha por skill com o nome em negrito e link para o `SKILL.md`.

### anthropics/skills (ANT)

- **Primeira tela:** uma nota apontando para o padrão em agentskills.io, um badge, título "Skills" e uma definição de skill em duas frases ("folders of instructions, scripts, and resources that Claude loads dynamically..."), seguida de links para a documentação.
- **Instalação:** por superfície (Claude Code, Claude.ai, API). No Claude Code, `/plugin marketplace add` e `/plugin install`, e **um exemplo de pedido**: "Use the PDF skill to extract the form fields from `path/to/some-file.pdf`".
- **Lista:** não lista skill por skill; aponta para as pastas `skills/`, `spec/` e `template/`.

### obra/superpowers (SUP)

- **Primeira tela:** sem imagem e sem badge. Título e uma frase: "a complete software development methodology for your coding agents, built on top of a set of composable skills". Depois um sumário longo.
- **Como funciona:** seção "How it works" logo depois do sumário, em prosa narrativa, do ponto de vista de quem usa ("As soon as it sees that you're building something, it doesn't just jump into trying to write code...").
- **Instalação:** uma subseção por agente (mais de quinze), o que empurra o resto para baixo.
- **Lista:** "The Basic Workflow" em sete passos numerados, cada um com o nome da skill e quando ela dispara; depois "Skills Library" por categoria (Testing, Debugging, Collaboration, Meta), nome e uma frase curta.

### vercel-labs/agent-skills (VAS) e vercel-labs/skills (VSK)

- **VAS:** título, uma frase ("A collection of skills for AI coding agents"), a menção ao formato Agent Skills e um badge. A lista vem antes da instalação: uma seção por skill, com um parágrafo e uma lista "Use when". A instalação é um comando só. A seção "Usage" dá três exemplos de pedido em blocos de código ("Deploy my app", "Review this React component for performance issues").
- **VSK:** título, uma frase ("The CLI for the open agent skills ecosystem"), uma linha de agentes suportados e uma fileira de badges grandes (`style=for-the-badge`). A instalação é o primeiro título.

### AgriciDaniel/claude-seo (SEO)

- **Primeira tela:** imagem SVG animada de 1200 por 420 com alt text descritivo; título centralizado; duas linhas em negrito com o resultado ("Free, open-source SEO audits inside Claude Code. Rank higher in Google and get cited by AI search."); uma barra de navegação com âncoras (Install, Demo, Results...); sete badges; um selo do Trendshift.
- **Primeiros parágrafos:** "Claude SEO is a free SEO plugin for Claude Code. Give it any website and it runs a full SEO audit in 10 to 15 minutes, then hands you a clear action plan", seguido de cinco itens do que é checado.
- **Demonstração:** "See it in action" logo em seguida, com dois GIFs do terminal.
- **Instalação:** fica mais para baixo, depois de resultados, comandos e preço.

### AgriciDaniel/claude-ads (ADS)

- **Primeira tela:** banner SVG de 1200 por 548 com variante clara e escura via `<picture>`, exibido a `width="100%"`, com `<title>` e `<desc>` dentro do SVG. Título e dois parágrafos: o que faz ("Give it your ad account data and it tells you what is working, what is broken, and what to fix first") e para quem ("agencies, consultants, and in-house marketing teams"), mais o que ela não faz ("It does not change your accounts on its own").
- **Quickstart:** cinco passos numerados, do comando de instalação ao primeiro relatório, seguidos de um diagrama "how it works" em três etapas (também claro e escuro).
- **Lista:** tabela "What you can do" com três colunas: "You want to", "Run", "You get".

### coreyhaines31/marketingskills (MKT)

- **Primeira tela:** sem imagem. Título e um parágrafo que diz o que é, para quem ("technical marketers and founders") e com quais agentes funciona. Depois links do autor e uma seção de parceiros, que empurra o conteúdo para baixo.
- **Como funciona:** "What are Skills?" em duas frases e "How Skills Work Together" com um diagrama em texto, mostrando a skill base que todas as outras leem primeiro.
- **Lista:** tabela de duas colunas (skill, descrição), gerada por script. As descrições copiam o início do `description` ("When the user wants to...") e são cortadas com reticências.
- **Instalação:** oito opções, a primeira `npx skills`, com uma dica sobre rodar o comando de dentro do agente.

### Nutlope/hallmark (HAL)

- **Primeira tela:** título, uma linha em negrito ("A design skill for Claude Code, Codex, Cursor and OpenCode that refuses to look AI-generated"), uma linha de links, "Made by Together AI", e a imagem de Open Graph do site reaproveitada (PNG de 1200 por 630).
- **Lista:** galeria de capturas dos temas em tabela HTML, com nome e uma linha cada.
- **Instalação:** um comando `npx skills add`, uma tabela por agente (onde a skill fica e como chamar) e uma linha para quando a skill não dispara sozinha: "name it: use hallmark to build ...".

### affaan-m/ECC (ECC) e K-Dense-AI/scientific-agent-skills (KDS)

- **ECC:** abre com imagem PNG de 2400 por 1350 (16 por 9) a `width="100%"`, selos de ranking e uma lista de dezesseis idiomas. Primeira tela tomada por imagem e selos; o texto que explica vem depois.
- **KDS:** catorze badges e cinco blocos de aviso antes da primeira frase que diz o que é ("A collection of 177 scientific and research skills for AI agents"). Exemplo do contrário do que se procura: o recém-chegado precisa rolar para saber o que é.

## 4. Orientação oficial sobre README

Confirmado em fonte primária:

- **O que um README costuma dizer** (GHR): o que o projeto faz, por que é útil, como começar, onde pedir ajuda, quem mantém. "A README is often the first item a visitor will see."
- **Tamanho** (GHR): o GitHub corta o que passar de 500 KiB e gera sozinho um sumário pelos títulos (menu "Outline").
- **Imagens** (GHP): para imagem do próprio repositório, usar link relativo; o elemento `<picture>` é suportado.
- **Imagem por tema** (GHC): `<picture>` com `<source media="(prefers-color-scheme: dark)">` mostra uma imagem no tema escuro e outra no claro; disponível desde 2022-08-15.
- **Prévia em redes sociais** (GHS): PNG, JPG ou GIF com menos de 1 MB; no mínimo 640 por 320, e 1280 por 640 "for best display". PNG com transparência é aceito, mas o GitHub sugere fundo sólido na dúvida, porque nem toda plataforma lida bem com transparência. É configurada em Settings, Social preview, não no README.

Guia da comunidade (MAR, não é fonte oficial): nome que se explica, descrição do que faz especificamente e do que diferencia das alternativas, badges, visuais (capturas ou GIF), instalação pensando num iniciante, uso com "the smallest example of usage", suporte, contribuição.

## 5. Padrões que se repetem

O que aparece em quase todos os bem avaliados (contagem minha nos onze READMEs da seção 3):

1. **Uma frase de abertura que diz o que é e o resultado para quem usa**, antes de qualquer comando (MPS, SUP, VAS, SEO, ADS, MKT, HAL). As melhores falam do resultado ("tells you what is working, what is broken, and what to fix first", ADS; "refuses to look AI-generated", HAL), não do tema.
2. **O porquê em termos de problema.** MPS organiza a seção inteira por falha do agente; SUP conta o fluxo do ponto de vista de quem usa; MPS e HAL nomeiam o que estão evitando (vibe coding, AI slop).
3. **Instalação curta e cedo, com o resto recolhido.** MPS usa `<details>` por agente e "30-second setup"; ADS e MPS numeram os passos até o primeiro resultado, incluindo o passo de setup depois de instalar. Os que listam tudo aberto (SUP, MKT) empurram o conteúdo para longe.
4. **Exemplo do que pedir.** ANT, VAS e HAL mostram a frase que a pessoa digita; ADS mostra o comando e o que ele devolve.
5. **Lista agrupada por categoria ou por tarefa, uma linha por skill.** MPS e SUP por categoria; ADS por "You want to / Run / You get". As linhas curtas e escritas para o leitor leem melhor que o `description` copiado (MKT corta com reticências).
6. **Imagem de cabeçalho só nos de produto.** SEO, ADS, HAL e ECC têm imagem larga; MPS tem logo pequena; ANT, SUP, VAS, MKT e KDS não têm. A imagem não substitui a frase: SEO e ADS ainda põem título e uma linha logo abaixo.
7. **O que atrapalha:** muitos badges, avisos e parceiros antes da primeira frase (KDS, MKT, ECC).

O que um recém-chegado precisa na primeira tela, juntando GHR e os padrões: o que é (uma frase), o que ganha e para quem (uma ou duas frases), um sinal de que é sério (autor, licença, ou um badge), e o primeiro passo (um comando). Inferência minha; nenhuma fonte define "primeira tela".

## 6. Recomendações para este repo

Inferências a partir das seções 3 a 5; não testadas com leitores.

1. **Trocar a primeira frase pelo resultado, não pelo tema.** Hoje: "Minhas skills de agente para arquitetura de software, programação, IA e SaaS." Algo no molde de ADS e HAL: o que o agente passa a fazer com elas, em uma frase, e para quem (quem programa com agente e quem cria conteúdo sobre isso). A tese "gerar código ficou barato" é forte e cabe como segundo parágrafo, como o porquê de MPS.
2. **Dizer as duas frentes logo no começo, com um exemplo de cada.** O repo serve a dois públicos (engenharia com IA e criação de vídeo curto). Uma linha por frente, com uma frase do que pedir ao agente ("crie uma skill a partir desta falha", "escreva o roteiro deste reel a partir das minhas notas"), no estilo de ANT e VAS.
3. **Quickstart de três passos antes dos detalhes.** No molde de MPS: (1) instalar, com o `npx skills` primeiro por ser um comando só e servir a qualquer agente; (2) rodar a `setup-eusouosalmo-skills` quando for usar as skills de reel; (3) pedir algo. O plugin, com atualizar e remover, vai para um `<details>` recolhido ou uma seção mais abaixo, mantendo o aviso de não instalar pelos dois caminhos.
4. **Agrupar a lista por frente.** Separar "Engenharia e harness" de "Conteúdo e vídeo curto", em vez da lista única atual mais a tabela de categorias no fim. Para as de reel, que funcionam em sequência, uma lista numerada do fluxo (roteiro, corte, animação, finalização, legenda), como "The Basic Workflow" de SUP, diz de uma vez a ordem de uso.
5. **Manter o porquê e a origem, mas mais abaixo.** "Uma skill só entra aqui depois que fiz o trabalho na mão" é o diferencial (o equivalente ao "not vibe coding" de MPS). Cabe numa linha na abertura e numa seção "Por que estas skills" depois da lista.
6. **Poucos sinais, sem poluir.** No máximo um ou dois badges (licença, skills.sh), como MPS e VAS. Evitar a fileira de KDS e ECC antes da primeira frase.
7. **Links do autor depois do primeiro passo.** Instagram, YouTube e site vêm hoje no primeiro bloco; em MPS, ADS e SEO o autor aparece depois da explicação ou no fim.
8. **Imagem de cabeçalho opcional, larga e sem texto gerado.** Ver seção 7.

## 7. Imagem de cabeçalho e prompts

**É comum?** Nos de produto, sim (SEO, ADS, HAL, ECC); nos de autor, quase não (só a logo pequena de MPS). Para um repositório pessoal, a imagem ajuda mais na prévia quando o link é compartilhado (GHS) do que dentro do README.

**O que mostram:** SEO, uma cena ilustrada do que a ferramenta faz (robôs subindo de posição); ADS, um terminal digitando o comando; HAL, a peça de divulgação do site; ECC, arte de marca. MPS, só a logo. Todos com alt text que descreve a imagem.

**Tamanhos e formatos medidos:**

| Repo | Formato | Tamanho | Claro e escuro |
| - | - | - | - |
| MPS | PNG | 738 por 388, exibida a 369 de largura | sim, `<picture>` |
| SEO | SVG animado | 1200 por 420 | não |
| ADS | SVG | 1200 por 548, a 100% | sim, `<picture>` |
| HAL | PNG | 1200 por 630 (imagem de Open Graph) | não |
| ECC | PNG | 2400 por 1350, a 100% | não |
| Prévia social do GitHub (GHS) | PNG, JPG ou GIF | 1280 por 640 recomendado, menos de 1 MB | um só arquivo; fundo sólido na dúvida |

**Sugestão:** uma arte de 1280 por 640, PNG com fundo sólido, que serve de prévia social (GHS) e de cabeçalho no README, com link relativo (GHP) a partir de uma pasta como `docs/assets/`. Se quiser variante clara e escura, duas versões com `<picture>` (GHC). O título e a frase de abertura ficam no Markdown, logo abaixo da imagem, como em SEO e ADS, para não depender da imagem para explicar o repo e para o texto ser traduzível entre o `README.md` e o `README.en.md`. Alt text descrevendo a cena.

**Texto dentro da imagem:** geradores de imagem costumam errar letras e palavras, sobretudo em frases longas e fora do inglês (relato comum de quem usa; não achei fonte primária que meça). Por isso os prompts abaixo pedem nenhum texto. Se quiser o nome "eusouosalmo/skills" na arte, o mais seguro é gerar sem texto e sobrepor depois num editor, ou montar a arte em SVG como ADS.

**Prompt 1 (bancada de engenharia e conteúdo):**

> Wide 2:1 banner illustration, 1280x640. A calm, minimal developer workbench seen from slightly above, split into two halves that blend in the middle. Left half: a dark code editor window with abstract colored lines, a small terminal, and modular blocks snapping together like building pieces, suggesting composable tools for an AI coding agent. Right half: a vertical smartphone frame showing a talking-head video, a teleprompter strip, a film timeline with clips and waveform, suggesting short-video content creation. A thin glowing line connects both halves, like a pipeline. Flat vector style with soft gradients, deep navy background, accents in electric blue and warm orange, generous empty space at the top for a title added later. No text, no letters, no logos, no watermark.

**Prompt 2 (skills como módulos, mais abstrato):**

> Wide 2:1 header image, 1280x640, solid dark background. A grid of small rounded square tiles floating in soft isometric perspective, each tile a simple line icon: a code bracket, a git branch, a shield, a checklist, a film clapper, a microphone, a pen, a play button. Some tiles click together into a short chain in the center, as if an agent is picking the right tools for a task. Clean geometric style, subtle glow, limited palette of navy, electric blue and one warm orange accent, lots of negative space on the left third for a title added later. No text, no letters, no numbers, no logos, no watermark.

Para a variante clara, trocar "deep navy background" ou "solid dark background" por "off-white background" e manter as mesmas cores de destaque.
