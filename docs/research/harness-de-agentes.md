# Harness de agentes de código: o que é e como se divide

Resumo: "harness" tem dois sentidos nas fontes. No sentido estreito, é o programa que embrulha o modelo (Claude Code, Codex, Agent SDK: loop, ferramentas, contexto, permissões). No sentido que importa para este repositório, é tudo o que o usuário monta em volta desse programa para que o agente acerte mais e se corrija sozinho: specs, contexto, checks, limites, isolamento. O modelo mental de três partes (spec na entrada, loop no meio, verificação na saída) se sustenta como esqueleto, e as fontes usam nomes próprios para cada parte. Mas ele deixa de fora quatro peças que todas as fontes tratam como separadas: o estado entre iterações, os guardrails (impedir ações), a observabilidade (ver o loop) e o laço de melhoria do próprio harness. As duas falhas observadas no teste de Ralph (tela vazia e loop sem fim) caem exatamente em duas dessas lacunas.

Pesquisa feita em 2026-10-01, sem ticket próprio, e ampliada em 2026-10-02 com o restante do material do site do Martin Fowler sobre o tema (seção 10). Complementa [guardrails-e-modo-afk.md](guardrails-e-modo-afk.md), que já cobre guardrails de git, sandbox, container, permission modes e as práticas básicas de loop AFK; aqui esses pontos aparecem só por referência.

## Sumário

1. [Método e níveis de confiança](#1-método-e-níveis-de-confiança)
2. [O que as fontes chamam de harness](#2-o-que-as-fontes-chamam-de-harness)
3. [Como cada fonte divide o harness](#3-como-cada-fonte-divide-o-harness)
4. [O modelo de três partes contra as fontes](#4-o-modelo-de-três-partes-contra-as-fontes)
5. [Guardrail x verificação](#5-guardrail-x-verificação)
6. [Condição de parada](#6-condição-de-parada)
7. [Observabilidade do loop](#7-observabilidade-do-loop)
8. [Harness por contexto: AFK local, VPS remota, interativo](#8-harness-por-contexto-afk-local-vps-remota-interativo)
9. [Como os autores empacotam o harness em skills](#9-como-os-autores-empacotam-o-harness-em-skills)
10. [O que mais o site do Martin Fowler diz](#10-o-que-mais-o-site-do-martin-fowler-diz)
11. [Onde as fontes concordam e divergem](#11-onde-as-fontes-concordam-e-divergem)
12. [Perguntas abertas para o desenho](#12-perguntas-abertas-para-o-desenho)
13. [Fontes](#13-fontes)

## 1. Método e níveis de confiança

Fontes primárias: a doc oficial do Claude Code (baixada em Markdown de code.claude.com), dois posts de engenharia da Anthropic, o post de harness engineering da OpenAI, o artigo da Birgitta Böckeler no site do Martin Fowler (mais os memos, artigos e verbetes do mesmo site listados na seção 10, lidos no HTML original em 2026-10-02), os posts do Geoffrey Huntley, do Mitchell Hashimoto, da HumanLayer e da LangChain, o README e os SKILL.md do repositório mattpocock/skills e o README do Sandcastle (via `gh api`), e o README do plugin ralph-wiggum no repositório anthropics/claude-code.

Cada prática traz os mesmos campos da nota de guardrails:

- **confirmado**: está na doc oficial de produto (Claude Code, Agent SDK).
- **convenção**: vários autores independentes fazem.
- **relato**: um autor afirma.

Posts de engenharia da Anthropic e da OpenAI contam como relato: descrevem experimentos de uma equipe, não comportamento de produto.

## 2. O que as fontes chamam de harness

### 2.1 O harness como o programa em volta do modelo

- **O que é:** a doc do Claude Code define "agentic harness" como as ferramentas, a gestão de contexto e o ambiente de execução que transformam um modelo num agente de código. Nas palavras do glossário, o Claude Code é o harness e o Claude é o modelo dentro dele. O harness fornece acesso a arquivos, shell, controle de permissão, carregamento de memória e o loop que encadeia as ações.
- **Por que existe:** separar o que o modelo raciocina do que o programa faz por ele.
- **Fonte:** [Glossary, Agentic harness](https://code.claude.com/docs/en/glossary#agentic-harness); [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works).
- **Confiança:** confirmado.

A mesma página descreve o "agentic loop" interno em três fases: reunir contexto, agir e verificar resultados, repetindo até terminar. Ou seja, mesmo sem nenhum Ralph, o Claude Code já tem um loop com verificação dentro de cada tarefa. O loop do Ralph é um segundo loop, por fora.

O post da Anthropic sobre agentes de longa duração usa o termo nesse sentido ao chamar o Agent SDK de "general-purpose agent harness", e no sentido amplo ao chamar de harness o conjunto de prompts, arquivos e sessões que ele monta por cima ([Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)).

### 2.2 Agent = Model + Harness

- **O que é:** a LangChain resume como "se você não é o modelo, você é o harness": todo código, configuração e lógica de execução que não é o modelo. Lista system prompt, ferramentas, skills e MCPs, infraestrutura (filesystem, sandbox, navegador), orquestração (subagents, handoffs) e hooks para execução determinística (compactação, continuação, lint).
- **Por que existe:** o modelo sozinho não guarda estado, não executa código e não configura ambiente. Cada peça do harness é derivada de algo que o modelo não faz.
- **Fonte:** [Vivek Trivedy, LangChain, "The Anatomy of an Agent Harness"](https://blog.langchain.com/the-anatomy-of-an-agent-harness/), março de 2026.
- **Confiança:** relato. A fórmula é repetida pela HumanLayer e pela Böckeler, então a definição ampla é convenção.

### 2.3 O harness do usuário (outer harness)

- **O que é:** a Böckeler estreita a definição para quem usa um agente de código. Separa o harness do construtor (o que vem no Claude Code) do harness do usuário, a camada externa que o time monta para o seu caso. Esse harness externo tem dois objetivos: aumentar a chance de o agente acertar de primeira e dar um laço de feedback que corrija o máximo possível antes de chegar ao humano.
- **Por que existe:** reduzir o trabalho de revisão e aumentar a qualidade, gastando menos tokens no caminho.
- **Fonte:** [Birgitta Böckeler, "Harness engineering for coding agent users"](https://martinfowler.com/articles/harness-engineering.html), publicado em 2 de abril de 2026 no site do Martin Fowler, a partir de um memo de 17 de fevereiro de 2026 (seção 10.1).
- **Confiança:** relato, mas é a referência mais citada pelas outras fontes.

É esse segundo sentido que interessa para uma categoria `harness/` de skills: o que o usuário configura no repositório, não o programa.

### 2.4 Harness engineering

As fontes concordam no núcleo da ideia e divergem na ênfase:

| Fonte | Definição, em resumo | Ênfase |
| :- | :- | :- |
| Mitchell Hashimoto | Toda vez que o agente erra, construir uma solução para que ele nunca mais erre daquele jeito: uma linha no AGENTS.md ou uma ferramenta programada (script de screenshot, teste filtrado) | Laço de melhoria a partir de erros reais |
| OpenAI (Ryan Lopopolo) | O trabalho do engenheiro passa a ser desenhar ambientes, especificar intenção e construir feedback loops para o agente trabalhar de forma confiável | Ambiente legível, restrições mecânicas, verificação |
| HumanLayer | Usar os pontos de configuração do agente (CLAUDE.md, MCP, skills, subagents, hooks, back-pressure) para melhorar qualidade e confiabilidade; subconjunto de context engineering | Contexto e configuração |
| LangChain | Construir sistemas em volta do modelo para transformá-lo em motor de trabalho | Primitivas derivadas das limitações do modelo |
| Böckeler | Sistema de guias e sensores que aumenta a probabilidade de resultados confiáveis, com o humano ajustando o harness | Controle cibernético: feedforward e feedback |
| Anthropic (Prithvi Rajasekaran) | Cada componente do harness codifica uma suposição sobre o que o modelo não consegue fazer sozinho; essas suposições envelhecem e precisam ser testadas | Simplificar quando o modelo melhora |

Fontes: [Hashimoto, "My AI Adoption Journey"](https://mitchellh.com/writing/my-ai-adoption-journey#step-5-engineer-the-harness), fevereiro de 2026; [OpenAI, "Harness engineering: leveraging Codex in an agent-first world"](https://openai.com/index/harness-engineering/), fevereiro de 2026; [HumanLayer, "Skill Issue: Harness Engineering for Coding Agents"](https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents), março de 2026; [Anthropic, "Harness design for long-running application development"](https://www.anthropic.com/engineering/harness-design-long-running-apps), março de 2026.

Sobre a origem do termo, as fontes não batem: a HumanLayer atribui a cunhagem ao Vivek Trivedy, outros textos apontam o post do Hashimoto. Não muda nada para o desenho.

Uma observação da HumanLayer vale registrar: no post da OpenAI a palavra "harness" quase não aparece no corpo do texto, e a leitura dela é que a OpenAI chama de harness o que fica fora do runtime do agente, com foco em back-pressure e verificação.

## 3. Como cada fonte divide o harness

Cada fonte corta o harness de um jeito. A tabela alinha as partes com nomes que se repetem.

| Parte | Huntley (Ralph) | Matt Pocock | Anthropic (long-running) | OpenAI | Böckeler | HumanLayer |
| :- | :- | :- | :- | :- | :- | :- |
| Spec, o que construir | specs/ geradas em conversa, `fix_plan.md` | PRD ou spec, tickets | feature list em JSON; depois um planner que expande o prompt | "specify intent", execution plans versionados | guia feedforward (spec funcional) | research e plan |
| Contexto, como construir aqui | `AGENT.md` com como compilar e rodar | glossário, ADRs, AGENTS.md curto | `init.sh`, prompt da sessão | AGENTS.md como sumário, `docs/` como fonte da verdade | guias: AGENTS.md, skills, LSP, codemods | CLAUDE.md curto, skills, subagents |
| Loop, execução | `while` com o mesmo prompt, uma tarefa por volta | Ralph com limite de iterações; Sandcastle | uma sessão por feature, contexto limpo a cada uma | agente itera até os revisores ficarem satisfeitos ("Ralph Wiggum Loop") | o loop de autocorreção do agente | implement por fases |
| Estado entre voltas | `fix_plan.md`, git | `progress.txt`, commits | `claude-progress.txt`, git log, `passes` no JSON | planos com log de progresso e decisões no repositório | (não trata) | compactação intencional em arquivos |
| Verificação | backpressure: testes, build, análise estática | feedback loops: types, testes, browser | testes ponta a ponta com navegador; evaluator separado | linters próprios, testes estruturais, revisão por agentes, validação no app rodando | sensores feedback, computacionais e inferenciais | back-pressure: typecheck, testes, cobertura, browser |
| Guardrails, impedir | (não trata) | git guardrails, Docker sandbox | (não trata) | restrições de arquitetura; "guardrails" citado como peça que falta | (fora do escopo; foco em qualidade) | hooks de aprovação e bloqueio |
| Observabilidade | "watch the loop" | streaming do `-p`; logs do Sandcastle | logs do evaluator | logs, métricas e traces do app expostos ao agente | sensores de runtime | hooks de notificação |
| Melhoria do harness | "tunar o Ralph como uma guitarra", placas | skill `retro` | "assumptions expire" | toda falha vira doc ou ferramenta | steering loop | só configurar depois de uma falha real |

As fontes de cada célula estão nas seções seguintes e na lista final.

## 4. O modelo de três partes contra as fontes

O modelo do usuário: entrada (specs, PRD, issues), meio (o loop, Ralph e variantes), saída (testes, validação, quality gates, revisão).

### 4.1 O que se confirma

- **Spec na entrada.** Huntley começa pela fase de gerar specs numa conversa longa antes de qualquer código, e diz que, quando o Ralph constrói a coisa errada, a culpa costuma ser da spec ([Ralph](https://ghuntley.com/ralph/)). Matt manda escrever um PRD antes do loop e diz que o PRD define o estado final ([Getting Started With Ralph](https://www.aihero.dev/getting-started-with-ralph)). A Anthropic transforma o prompt numa lista de features e, na segunda versão, num planner que escreve a spec. **Convenção.**
- **Loop no meio.** Ralph é o nome comum para isso. A OpenAI cita o loop de revisão como Ralph Wiggum Loop; a LangChain lista "Ralph Loops" como padrão de harness para trabalho longo. **Convenção.**
- **Verificação na saída.** É a parte em que todas as fontes mais insistem. Huntley chama de backpressure; a Böckeler, de sensores; Matt, de feedback loops; a HumanLayer, de back-pressure; a Anthropic, de evaluator; a doc do Claude Code, de "a check it can run". **Confirmado** (ver [guardrails-e-modo-afk.md, seção 3.12](guardrails-e-modo-afk.md#312-verificação-testes-stop-hook-goal-e-revisor-com-contexto-limpo)).

### 4.2 O que precisa de ajuste

1. **A entrada tem duas coisas, não uma.** A spec diz o que construir. O contexto diz como se constrói neste repositório: convenções, glossário, arquitetura, comandos. A Böckeler junta as duas como guias feedforward; a OpenAI separa planos (spec) de `docs/` e AGENTS.md (contexto); Huntley separa `specs/` de `AGENT.md`. Uma spec boa num repositório sem contexto produz código que funciona e não segue o padrão.
2. **A verificação não fica só na saída.** No modelo da Böckeler, sensores rápidos rodam a cada mudança, dentro do loop; os caros rodam depois da integração; e há sensores contínuos fora de qualquer mudança (código morto, cobertura, dependências). A OpenAI roda agentes de "garbage collection" periódicos contra a deriva. A verificação é distribuída pelo ciclo, não um portão no fim.
3. **A spec e a verificação se encontram na condição de pronto.** O que faz o loop parar é um critério da spec que a verificação consegue checar. A Anthropic formaliza isso no "sprint contract": antes de escrever código, o gerador e o avaliador negociam o que conta como pronto. A seção 6 detalha.
4. **Faltam quatro peças.** Todas as fontes de loop longo tratam como partes próprias:
   - **Estado entre iterações:** arquivo de progresso, lista de tarefas com status, git. Sem isso, cada volta do loop recomeça do zero.
   - **Guardrails:** impedir ações perigosas e conter o estrago. Diferente de verificação (seção 5).
   - **Observabilidade:** o humano ver o que o loop está fazendo, e o agente ver o que o app está fazendo. Duas coisas diferentes (seção 7).
   - **Laço de melhoria do harness:** Hashimoto, Böckeler (steering loop), Huntley (placas para o Ralph), Matt (`retro`) e Anthropic (suposições que envelhecem) descrevem um loop por fora de tudo, em que o humano observa falhas e muda o harness. Combina com a regra deste repositório de só criar skill a partir de falha observada.

### 4.3 Veredito

O modelo se sustenta como esqueleto da parte de qualidade, mas fica incompleto como mapa do harness. Uma versão ajustada, com os nomes que as fontes usam:

| Parte | O que responde | Nomes nas fontes |
| :- | :- | :- |
| Spec | O que construir e quando está pronto | spec, PRD, feature list, plan, sprint contract, acceptance criteria, spec-first |
| Contexto | Como se trabalha neste repositório | guides (feedforward), AGENTS.md, context engineering, system of record, memory bank, steering, constitution |
| Loop | Quem escolhe a próxima tarefa e quando roda de novo | Ralph loop, orchestration, agentic loop, sessions, how loop |
| Estado | O que já foi feito e onde parou | progress file, fix_plan, feature list com `passes`, git log, blackboard |
| Verificação | Está certo? Está pronto? | backpressure, sensors (feedback), feedback loops, evaluator, quality gates |
| Guardrails | O que o agente não pode fazer e o que contém o estrago | permissions, hooks de bloqueio, sandbox, container, branch protection |
| Observabilidade | O que está acontecendo agora | watch the loop, streaming, logs, notificações, telemetria |
| Melhoria | O que mudar no harness depois de uma falha | engineer the harness, steering loop, retro, tuning, on the loop, agentic flywheel |

A ordem de entrada, meio e saída continua útil para spec, loop e verificação. Contexto, estado, guardrails e observabilidade são transversais, valem o tempo todo. Melhoria é o loop de fora.

## 5. Guardrail x verificação

As fontes tratam as duas coisas como distintas, mesmo quando usam o mesmo mecanismo.

### 5.1 Verificação: dizer se está errado ou pronto

- **O que é:** sinal que volta para o agente depois que ele age: teste, typecheck, lint, build, revisão, avaliador com navegador. Não impede a ação; rejeita o resultado e manda corrigir.
- **Por que existe:** gerar código ficou barato; o difícil é saber se o gerado está certo. Huntley diz que qualquer coisa pode virar backpressure para rejeitar geração inválida, desde que a roda gire rápido. A HumanLayer diz que a chance de sucesso acompanha a capacidade do agente de verificar o próprio trabalho, e que essa foi uma das coisas de maior retorno que fizeram.
- **Fonte:** [Huntley, Ralph, fase "backpressure"](https://ghuntley.com/ralph/); [HumanLayer, seção Back-Pressure](https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents); [Böckeler, Feedforward and Feedback](https://martinfowler.com/articles/harness-engineering.html).
- **Confiança:** convenção (e confirmado pela doc do Claude Code, que manda dar ao Claude um check executável).

Nomes: backpressure (Huntley, HumanLayer), sensors ou feedback controls (Böckeler), feedback loops (Matt, OpenAI), evaluator e QA (Anthropic).

Detalhes que as fontes acrescentam:

- **Computacional x inferencial.** A Böckeler separa sensores determinísticos e rápidos (testes, linters, tipos) dos semânticos (revisão por IA, LLM como juiz), mais caros e não determinísticos. Os dois servem; os primeiros rodam a cada mudança, os segundos com menos frequência.
- **Sinal feito para o modelo ler.** A OpenAI escreve as mensagens de erro dos linters próprios com a instrução de correção dentro; a Böckeler chama isso de prompt injection do bem. **Convenção** (duas fontes).
- **Sinal econômico em contexto.** A HumanLayer aprendeu que rodar a suíte inteira e despejar milhares de linhas de testes passando afoga o agente. Passou a engolir a saída e mostrar só os erros. **Relato.**
- **Separar quem faz de quem julga.** A Anthropic observou que o agente elogia o próprio trabalho mesmo quando ele é medíocre, e que um avaliador separado, calibrado com exemplos, é uma alavanca forte. Também observou que, sem ajuste, o avaliador acha problemas e se convence de que não são graves. **Relato**, com eco na doc oficial (revisor adversarial com contexto limpo).
- **Comportamento é o ponto fraco.** A Böckeler diz que o harness de manutenibilidade é o mais maduro, e que o de comportamento funcional é o problema em aberto: depender de testes gerados pelo próprio agente ainda não basta. **Relato.**

### 5.2 Guardrail: impedir a ação ou conter o estrago

- **O que é:** controle que age antes ou em volta da ação: permission rules, hook PreToolUse que bloqueia, sandbox, container, credencial sem permissão de push, branch protection.
- **Por que existe:** um erro de verificação custa uma volta do loop; um `reset --hard` ou um push indevido não se desfaz com outra volta.
- **Fonte:** a nota [guardrails-e-modo-afk.md](guardrails-e-modo-afk.md) cobre isso em detalhe; a doc do Agent SDK trata o tema em [Securely deploying AI agents](https://code.claude.com/docs/en/agent-sdk/secure-deployment), com modelo de ameaça (prompt injection e erro do modelo) e defesa em camadas.
- **Confiança:** confirmado.

Nomes: permissions, guardrails, sandbox, isolation, "enforceable constraints" (LangChain).

### 5.3 Onde a fronteira fica borrada

- **O mesmo mecanismo serve aos dois.** No Claude Code, um hook PreToolUse com exit 2 é guardrail (bloqueia antes). Um Stop hook com exit 2 é verificação (a HumanLayer roda typecheck e formatter quando o agente tenta parar e, se houver erro, devolve o erro e ele continua). Mesmo sistema de hooks, papéis diferentes. **Confirmado** quanto ao mecanismo ([hooks](https://code.claude.com/docs/en/hooks)), **relato** quanto ao uso.
- **Restrições de arquitetura.** A OpenAI chama as regras de camadas de "constraints" e as aplica com linters e testes estruturais. Na taxonomia da Böckeler isso é sensor (avisa depois), não guardrail (não impede a escrita). A OpenAI também lista "guardrails" junto de ferramentas e documentação como coisas que faltam quando o agente tropeça, sem definir.
- **A Böckeler não trata segurança.** O artigo dela é sobre qualidade (manutenibilidade, arquitetura, comportamento). Guardrails de segurança simplesmente não aparecem. Quem trata os dois juntos é a LangChain (sandbox e verificação na mesma seção) e a doc do Claude Code (permissões e verificação em páginas separadas). No mesmo site, quem trata segurança é outro autor (Korny Sietsma, seção 10.8).
- **"Guardrail" tem um terceiro sentido.** No memo de context engineering, a Böckeler usa "guardrails" como sinônimo de rules: convenções que o agente deve seguir, escritas num arquivo de contexto. Isso é guia feedforward, não bloqueio nem verificação. Quem ler "guardrail" numa fonte precisa conferir qual dos três sentidos ela usa (seção 10.2).
- **Uma verificação pedida por instrução pode não rodar.** A Böckeler relata que pedir ao agente, via AGENTS.md ou skill, para consultar os sensores foi pouco confiável; ele esquecia ou rodava outra coisa. As alternativas que ela lista são hook do agente, pre-commit do git ou uma ferramenta própria no harness (seção 10.6). O gatilho determinístico não transforma a verificação em guardrail: o check continua respondendo "o resultado presta?", só que agora sempre roda.
- **Uma verificação que bloqueia precisa de um guardrail que a proteja.** No experimento de autonomia do site, o agente declarava sucesso com testes vermelhos; a mitigação óbvia é um checkpoint determinístico que só deixa seguir com tudo verde, e a autora suspeita que o agente apagaria ou pularia testes para passar por ele (seção 10.7). Aqui as duas peças se combinam: a verificação diz se está pronto, e um guardrail (por exemplo, negar edição dos testes existentes) impede que o agente desarme a verificação. A combinação é síntese minha.

Leitura que sai disso: verificação responde "o resultado presta?" e guardrail responde "essa ação pode acontecer?". Dá para usar a mesma ferramenta para os dois, mas a pergunta que cada peça responde deveria ficar explícita no desenho. Esta é uma síntese minha a partir das fontes, não uma regra que alguma delas escreva.

## 6. Condição de parada

A segunda falha observada (o loop não terminava porque não havia objetivo final) tem uma explicação direta: o Ralph original não para. O script é um `while` infinito, e o próprio Huntley conta que o Ralph acaba ficando sem tarefas ou sai dos trilhos, e que nessa hora decide no gosto, olhando a lista de tarefas e às vezes jogando ela fora ([Ralph](https://ghuntley.com/ralph/)). A parada era humana. Todas as variantes depois disso acrescentaram uma regra explícita.

### 6.1 Completion promise

- **O que é:** o prompt manda o agente escrever uma marca combinada (por exemplo `<promise>COMPLETE</promise>`) quando tudo estiver feito. O script procura a marca na saída de cada volta e sai do loop se achar.
- **Por que existe:** dar ao loop externo um jeito simples de saber que o agente acha que terminou.
- **Fonte:** [Matt Pocock, Getting Started With Ralph](https://www.aihero.dev/getting-started-with-ralph) (o script AFK procura a marca e sai); [plugin ralph-wiggum](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum) (`--completion-promise`); [Sandcastle](https://github.com/mattpocock/sandcastle) (`completionSignal`, com a mesma marca como padrão).
- **Confiança:** convenção.

Limites registrados:

- A marca é a opinião do agente. A Anthropic observou o agente declarando vitória cedo demais, olhando o que já existia e dando o projeto por feito ([Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)). A marca só vale tanto quanto o critério que o prompt amarra a ela.
- O plugin avisa que a comparação é por texto exato e não distingue "SUCCESS" de "BLOCKED"; por isso recomenda o limite de iterações como mecanismo principal de segurança.

### 6.2 Limite de iterações e outros tetos

- **O que é:** número máximo de voltas, além de tetos de turno, custo e tempo ocioso.
- **Por que existe:** impedir o loop infinito numa tarefa impossível e o gasto sem controle.
- **Fonte:** Matt chama o argumento de iterações de teto contra custo descontrolado ([Getting Started](https://www.aihero.dev/getting-started-with-ralph)); o plugin oficial diz para sempre usar `--max-iterations`, e sugere que o prompt diga o que fazer se travar (documentar o bloqueio e o que foi tentado); o Sandcastle tem `maxIterations` (padrão 1) e `idleTimeoutSeconds` (10 minutos sem saída derruba a volta). A CLI do Claude Code tem `--max-turns` e `--max-budget-usd` em modo `-p` ([CLI reference](https://code.claude.com/docs/en/cli-reference)).
- **Confiança:** confirmado (flags da CLI); convenção (limite de iterações).

### 6.3 Lista de features com status

- **O que é:** um arquivo JSON com cada feature, os passos para testá-la e um campo `passes: false`. O agente só pode mudar esse campo, e só depois de testar. O trabalho acaba quando tudo está `true`.
- **Por que existe:** resolver duas falhas observadas: tentar fazer tudo de uma vez e declarar o projeto pronto cedo. A Anthropic escolheu JSON porque o modelo mexe menos indevidamente em JSON do que em Markdown.
- **Fonte:** [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).
- **Confiança:** relato. O formato de checklist com status aparece também no Huntley e no Matt, então a ideia geral é convenção.

### 6.4 Sprint contract

- **O que é:** antes de cada bloco de trabalho, o agente que implementa propõe o que vai construir e como o sucesso será verificado; o avaliador revisa até os dois concordarem. Cada critério tem um limiar mínimo; se um ficar abaixo, o bloco falha e volta com feedback.
- **Por que existe:** a spec é de propósito de alto nível, e faltava uma ponte entre a história de usuário e um teste executável.
- **Fonte:** [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps).
- **Confiança:** relato. Na versão seguinte, com um modelo mais forte, o autor removeu os sprints e deixou um único passe de avaliação no fim, o que mostra que a peça depende do modelo.

### 6.5 `/goal` e Stop hook no Claude Code

- **O que é:** `/goal <condição>` faz o Claude Code continuar trabalhando, turno após turno, até a condição valer. A cada fim de turno, um modelo pequeno lê a conversa e devolve "ainda não", "cumprido" ou "impossível". É um Stop hook baseado em prompt, por baixo. Funciona com `-p`, no app desktop e por Remote Control.
- **Por que existe:** tirar do agente que faz o trabalho a decisão de que terminou. A doc diz que a conclusão passa a ser decidida por um modelo novo, não pelo que está trabalhando.
- **Fonte:** [Keep Claude working toward a goal](https://code.claude.com/docs/en/goal).
- **Confiança:** confirmado.

O que a doc recomenda para a condição, e que vale para qualquer completion criterion:

- Um estado final mensurável (resultado de teste, código de saída, contagem, fila vazia).
- Um check declarado, dizendo como provar (por exemplo, o comando de teste sai com 0).
- As restrições que não podem mudar no caminho (por exemplo, nenhum outro arquivo de teste alterado).
- Para limitar a duração, uma cláusula de turnos ou tempo dentro da própria condição.

Ressalvas:

- O avaliador não roda comandos nem lê arquivos; só julga o que apareceu na conversa. A condição tem que ser algo que a saída do Claude consiga demonstrar.
- Se o Claude responde ao avaliador sem usar ferramentas por vários turnos, o Claude Code para o loop e devolve o controle. Para Stop hooks escritos à mão, há o teto de bloqueios seguidos já descrito em [guardrails-e-modo-afk.md, seção 3.12](guardrails-e-modo-afk.md#312-verificação-testes-stop-hook-goal-e-revisor-com-contexto-limpo).
- `/goal` não muda o permission mode. Para rodar sem ninguém, a doc indica combinar com auto mode.
- A doc compara três formas de manter a sessão rodando: `/goal` (para quando a condição vale), `/loop` (roda por intervalo de tempo; para quando você para ou o Claude decide) e Stop hook (para quando o seu script decide).

### 6.6 Ralph por fora x Ralph por dentro

Há duas famílias de loop, e elas param de jeitos diferentes:

| | Loop externo (script bash, Sandcastle) | Loop interno (plugin ralph-wiggum, `/goal`) |
| :- | :- | :- |
| Contexto a cada volta | Limpo: um processo novo do Claude Code por volta | A mesma sessão, com compactação |
| Quem decide parar | O script: marca na saída, teto de iterações, timeout | Stop hook: marca exata (plugin) ou avaliador (`/goal`) |
| Estado entre voltas | Só arquivos e git | Arquivos, git e a conversa |
| Fonte | Huntley, Matt, Sandcastle | [plugin ralph-wiggum](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum), [goal](https://code.claude.com/docs/en/goal) |

O Huntley publicou um vídeo explicando por que, na opinião dele, o plugin do Claude Code não é o Ralph (link no próprio post do Ralph); não assisti ao vídeo, então registro só que a divergência existe. A LangChain descreve o Ralph como reinjetar o prompt num contexto limpo, o que corresponde ao loop externo. A Anthropic, na segunda versão do harness, comenta que com um modelo mais forte a compactação na mesma sessão passou a bastar onde antes era preciso reset de contexto.

## 7. Observabilidade do loop

A primeira falha observada (nenhum sinal visual do que o loop fazia) é um problema conhecido e tem causa exata: `claude -p` com a saída de texto padrão não imprime nada até o fim. A doc do `/goal` avisa que um goal longo em `-p` pode parecer travado por isso. O Matt escreveu um post inteiro sobre o mesmo incômodo: rodar o script AFK e ficar olhando para uma tela vazia, sem saber se o Claude está trabalhando, travado ou quebrado.

As fontes falam de dois tipos de observabilidade, que convém não misturar:

- **O humano vendo o agente:** o que está fazendo, se travou, se precisa de alguém.
- **O agente vendo o app:** logs, métricas, traces, screenshots do que ele construiu. Isso é verificação (seção 5), mesmo que use ferramentas de observabilidade.

### 7.1 Streaming da saída

- **O que é:** rodar `-p` com `--output-format stream-json --verbose` para receber cada mensagem enquanto acontece, filtrar com `jq` para mostrar só o texto do assistente e, em paralelo, gravar tudo num arquivo para procurar a marca de conclusão no fim.
- **Por que existe:** ter visão em tempo real sem desistir de capturar o resultado final.
- **Fonte:** [Matt Pocock, "Here's How To Stream Claude Code With AFK Ralph"](https://www.aihero.dev/heres-how-to-stream-claude-code-with-afk-ralph), janeiro de 2026; a doc oficial descreve o formato e as flags em [headless](https://code.claude.com/docs/en/headless) e manda usar esse formato com `/goal` em `-p` ([goal, Run non-interactively](https://code.claude.com/docs/en/goal#run-non-interactively)).
- **Confiança:** confirmado (flags); relato (o script).

No mesmo formato, negações de permissão chegam como mensagens `permission_denied`, e o resultado final lista as negações. Num loop AFK, isso é o sinal de que um guardrail disparou ([headless](https://code.claude.com/docs/en/headless)).

### 7.2 Log persistido por execução

- **O que é:** gravar cada execução num arquivo de log nomeado, com opção de repassar os eventos do agente para um sistema próprio.
- **Por que existe:** poder ver depois o que aconteceu numa execução que ninguém acompanhou.
- **Fonte:** [Sandcastle](https://github.com/mattpocock/sandcastle) (`logging` grava em `.sandcastle/logs/` por padrão; `onAgentStreamEvent` repassa eventos; o resultado traz iterações, commits, branch e se a marca de conclusão disparou).
- **Confiança:** relato.

### 7.3 Notificações

- **O que é:** hook `Notification` que dispara quando o Claude está esperando entrada ou permissão; hooks no fim da sessão que mandam mensagem, tocam som ou abrem PR.
- **Por que existe:** não precisar olhar o terminal.
- **Fonte:** [hooks guide, Get notified when Claude needs input](https://code.claude.com/docs/en/hooks-guide); a HumanLayer usa som e mensagem no Slack ([Skill Issue, Hooks Are for Control Flow](https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents)).
- **Confiança:** confirmado.

Contraponto: o Hashimoto desliga as notificações do agente de propósito, para não pagar a troca de contexto, e olha o agente nas pausas naturais do trabalho dele ([My AI Adoption Journey](https://mitchellh.com/writing/my-ai-adoption-journey)). **Relato.** Num loop AFK, o que importa é ser avisado quando ele termina ou trava, não a cada passo.

### 7.4 Painéis e controle remoto

- **O que é:** recursos do Claude Code para acompanhar sessões sem ficar no terminal delas. `claude agents` (agent view) mostra todas as sessões em background, o que está rodando, o que espera entrada e o que terminou; `--bg` lança uma sessão em background. Remote Control conecta claude.ai ou o app do celular a uma sessão que roda na máquina. O `/goal` mostra condição, tempo, turnos, gasto de tokens e o último motivo do avaliador. Statusline customizável mostra contexto, custo e git. OpenTelemetry exporta métricas, eventos e traces.
- **Por que existe:** acompanhar trabalho longo ou paralelo.
- **Fonte:** [agent view](https://code.claude.com/docs/en/agent-view); [Remote Control](https://code.claude.com/docs/en/remote-control); [goal, Check status](https://code.claude.com/docs/en/goal#check-status); [statusline](https://code.claude.com/docs/en/statusline); [monitoring](https://code.claude.com/docs/en/monitoring-usage).
- **Confiança:** confirmado.

### 7.5 Observar para melhorar o harness

- **O que é:** assistir ao loop para achar padrões de mau comportamento e corrigir o harness.
- **Por que existe:** Huntley diz que é olhando o loop que se aprende, e que cada falha vista é um problema de engenharia a resolver para nunca mais acontecer. Ele mesmo começa com o loop manual ou com uma pausa que exige Ctrl+C para passar à próxima tarefa. O Matt recomenda começar com um script que roda uma volta só, assistir, conferir o commit e só depois ir para AFK. A Anthropic ajustou o avaliador lendo os logs dele e comparando com o próprio julgamento.
- **Fonte:** [Huntley, "everything is a ralph loop"](https://ghuntley.com/loop/), janeiro de 2026; [Getting Started With Ralph](https://www.aihero.dev/getting-started-with-ralph); [Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps).
- **Confiança:** convenção.

Isso liga a observabilidade ao laço de melhoria: sem ver o loop, não há como saber o que mudar no harness.

## 8. Harness por contexto: AFK local, VPS remota, interativo

Nenhuma fonte monta essa tabela; ela é uma síntese minha a partir das seções anteriores. Onde a peça não tem fonte direta, está marcado.

| Peça | Interativo | Loop AFK local | Loop numa VPS remota |
| :- | :- | :- | :- |
| Spec | Conversa, plan mode, grilling; pode ser informal porque o humano corrige no caminho | Obrigatória e escrita, com estado final verificável | Igual ao AFK local |
| Contexto | CLAUDE.md curto, glossário, docs | Igual, mais o prompt do loop | Igual |
| Loop | O humano é o loop | Script com teto, ou `/goal` em auto mode | Igual, mas o processo precisa sobreviver à desconexão |
| Estado | A conversa e o git | Arquivo de progresso, lista com status, commits | Igual; tudo commitado, porque a máquina pode sumir |
| Verificação | Testes, typecheck, Stop hook leve; o humano revisa | Backpressure que trava o commit; revisor com contexto limpo | Igual, mais CI do lado do servidor |
| Parada | O humano | Marca de conclusão mais teto de iterações, custo e ociosidade | Igual, com teto de custo obrigatório |
| Guardrails | Permissões com `ask` | Container ou sandbox, hooks de git (ver nota de guardrails) | Credencial com escopo mínimo, branch própria, branch protection |
| Observabilidade | O terminal | Streaming, log por execução, notificação no fim | Log persistido, notificação remota, painel ou controle remoto |
| Melhoria | `retro` depois da sessão | Assistir as primeiras voltas antes de ir embora | Ler os logs |

### 8.1 Interativo

O humano faz o papel de loop, de observador e de condição de parada. Ainda assim, todas as fontes de harness falam de uso interativo: o Hashimoto construiu o harness dele (AGENTS.md e scripts de verificação) trabalhando lado a lado com o agente; a Böckeler põe na lista de guias e sensores coisas que valem a cada mudança, inclusive revisão humana; a doc do Claude Code manda dar ao Claude um check executável em qualquer sessão. A HumanLayer roda typecheck e formatter num Stop hook em todas as sessões, e cobra aumento de cobertura por outro Stop hook. **Convenção.**

Para guardrails em sessão interativa (push em `ask`, por exemplo), ver [guardrails-e-modo-afk.md, seção 8](guardrails-e-modo-afk.md#8-afk-x-sessão-interativa).

### 8.2 Loop AFK local

O caso coberto pelo Matt e pelo Huntley. As peças essenciais: spec com estado final verificável, script com teto e marca de conclusão, arquivo de progresso, backpressure, container e streaming. As práticas de isolamento e de git estão em [guardrails-e-modo-afk.md, seção 6](guardrails-e-modo-afk.md#6-práticas-de-loop-afk).

### 8.3 Loop numa VPS remota

As fontes falam pouco de VPS própria. O que a doc oficial oferece para trabalho fora da máquina do usuário:

- **Routines e sessões na nuvem:** rodam em infraestrutura da Anthropic ou num ambiente self-hosted da organização, disparadas por agenda, API ou eventos do GitHub. O Claude cria branches com prefixo `claude/` e a doc descreve checagem do push para outras branches. Está em research preview. **Confirmado** ([routines](https://code.claude.com/docs/en/routines)).
- **Agent SDK hospedado:** a doc trata de arquitetura em subprocesso, persistência de sessão e isolamento em Docker, Kubernetes e sandbox, além de credenciais e controle de rede. **Confirmado** ([hosting](https://code.claude.com/docs/en/agent-sdk/hosting), [secure deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)).
- **Remote Control:** acompanhar e conduzir pelo celular uma sessão que roda noutra máquina. A doc diz que a sessão se reconecta se a máquina dormir ou a rede cair. **Confirmado** ([Remote Control](https://code.claude.com/docs/en/remote-control)).
- **Teto de custo:** `--max-budget-usd` em `-p`. **Confirmado.**

O resto é inferência minha, sem fonte que trate de VPS: o processo do loop precisa sobreviver à queda do SSH (multiplexador de terminal, serviço do sistema ou `--bg`); o log tem que ir para arquivo, porque ninguém vê o terminal; a notificação tem que sair da máquina (push no celular, mensagem); e a credencial de git na VPS deveria ser de escopo mínimo, já que a máquina fica ligada sem ninguém olhando. A nota de guardrails já registra a recomendação oficial de tokens com escopo de repositório e vida curta.

## 9. Como os autores empacotam o harness em skills

### 9.1 Matt Pocock: o loop não é skill

Na página de skills do AI Hero, o Matt resume assim: o Ralph é o loop, e as skills são o que vai dentro dele ([aihero.dev/skills](https://www.aihero.dev/skills), citado no fim de [Getting Started With Ralph](https://www.aihero.dev/getting-started-with-ralph)). O loop vive num script ou numa biblioteca (Sandcastle); as skills cobrem as partes que o agente executa em cada volta ou que o humano usa antes e depois.

Mapeando as skills atuais do [mattpocock/skills](https://github.com/mattpocock/skills) nas partes da seção 4.3 (leitura dos SKILL.md e do README em 2026-10-01):

| Parte | Skills |
| :- | :- |
| Spec | `grill-me`, `grill-with-docs` (alinhar antes de construir), `to-spec` (conversa vira spec no issue tracker), `to-tickets` (spec vira tickets com dependências), `wayfinder` (trabalho grande vira mapa de tickets de decisão) |
| Contexto | `setup-matt-pocock-skills` (configura tracker, labels e onde ficam os docs), `domain-modeling` (glossário e ADRs), `codebase-design`, `writing-for-agents` |
| Loop e execução | `implement` (implementa uma spec com TDD e fecha com review), `implement-spec` (tickets como grafo de tarefas com subagents em paralelo); fora das skills, o script do Ralph e o Sandcastle |
| Estado | `handoff` (compacta a conversa num documento para outro agente continuar); no Ralph, `progress.txt` |
| Verificação | `tdd`, `diagnosing-bugs` (montar um loop que fica vermelho no bug), `code-review` (dois eixos: padrões do repositório e aderência à spec), `pr` |
| Guardrails | `git-guardrails-claude-code`, `setup-pre-commit` |
| Melhoria | `retro` (sugere mudanças no ambiente do agente depois de uma sessão: navegação, checks automáticos, padrões de código, AGENTS.md, acesso a informação) |

Observações:

- O `to-prd` e o `to-issues` que o usuário conhece foram unificados em `to-spec` e `to-tickets` (commit "unify planning skills into /to-spec + /to-tickets" no histórico do repositório).
- O README separa as skills por quem invoca: as que só o usuário chama orquestram (`implement`, `to-spec`, `retro`); as que o modelo também pode chamar guardam disciplina reutilizável (`tdd`, `code-review`, `diagnosing-bugs`). É um segundo eixo de divisão, além das partes do harness.
- A `retro` separa o agente que implementa (muita pressão de contexto) do agente que revisa (recebe só o diff) e diz que os padrões de código devem ser impostos na revisão, não na implementação. É a mesma separação entre fazer e julgar da Anthropic.
- Há uma skill em andamento, `loop-me`, que usa "loop" noutro sentido: rotinas da vida do usuário para delegar, com vocabulário de gatilho e checkpoint humano. Não é sobre loop de código.
- **Confiança:** relato (um autor).

### 9.2 Outras divisões

- **Anthropic, harness de longa duração:** dois prompts com o mesmo harness, um inicializador que monta spec, estado e script de ambiente, e um de código que avança uma feature por sessão. Na versão seguinte, três papéis: planner (spec), generator (loop) e evaluator (verificação). É o modelo de três partes do usuário quase literal, mais o estado em arquivos. **Relato.**
- **HumanLayer:** fluxo de pesquisa, plano e implementação, cada fase com seu prompt (comandos do Claude Code no repositório deles), compactando o resultado de cada fase num arquivo. A revisão humana fica nas fases de maior alavanca: uma linha errada de pesquisa vira milhares de linhas erradas de código, uma linha errada de plano vira centenas. **Relato** ([Advanced Context Engineering for Coding Agents](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md)).
- **Böckeler:** sugere que o futuro sejam "harness templates", pacotes de guias e sensores por tipo de serviço (dashboard em Node, CRUD na JVM), e já usa skills nos exemplos tanto como guia (convenções, como testar) quanto como sensor (instruções de revisão). **Relato.**
- **Plugin oficial ralph-wiggum:** empacota o loop como comando mais Stop hook, sem nada de spec ou verificação; o prompt do usuário carrega tudo. **Confirmado** quanto à existência no repositório oficial.

## 10. O que mais o site do Martin Fowler diz

O artigo da Böckeler não está sozinho. O site do Martin Fowler publica desde 2023 a série "Exploring Generative AI", com memos curtos de pessoas da Thoughtworks, além de artigos longos e verbetes do próprio Fowler (bliki). Li no HTML original, em 2026-10-02, o que trata de harness, loops, spec, contexto, verificação e o papel do humano. Ficaram de fora os memos sobre autocomplete, modelos locais e migração de legado, que não mudam nada aqui. Tudo nesta seção é **relato**, salvo indicação: são experimentos e opiniões de uma pessoa, muitas vezes com amostra pequena declarada pela própria autora.

### 10.1 A linha do tempo do tema no site

- **Memo "Harness Engineering, first thoughts"** (Böckeler, 17 de fevereiro de 2026): reação ao post da OpenAI. Agrupa o harness da OpenAI em context engineering, restrições de arquitetura e "garbage collection", e aponta que falta ali verificação de comportamento. Levanta duas hipóteses que voltam no artigo: harnesses como os novos service templates de uma organização, e que mais autonomia exige restringir o espaço de solução (menos stacks, topologias padronizadas). O próprio memo hoje remete ao artigo completo.
- **Artigo "Harness engineering for coding agent users"** (Böckeler, 2 de abril de 2026): a versão elaborada, já coberta nas seções anteriores. Três ideias dele que esta nota não registrava: harnessability (nem todo codebase aceita harness igual; tipos, fronteiras claras de módulo e frameworks dão sensores e restrições de graça, e o legado é onde o harness mais falta e mais custa); a Lei de Ashby como argumento para topologias padronizadas (um regulador só controla o que consegue modelar); e o papel do humano, cuja experiência funciona como harness implícito que o agente não tem, de modo que o harness deve direcionar a atenção humana para onde ela pesa mais, não eliminá-la.
- **Artigo "Maintainability sensors for coding agents"** (Böckeler, 27 de maio de 2026): o seguimento prático, na seção 10.6.

### 10.2 Context engineering para agentes de código

- **O que é:** um panorama das peças de configuração de contexto, com o Claude Code como exemplo. A autora separa prompts reutilizáveis em instruções (faça isto) e guidance (convenções gerais, que ela também chama de rules ou guardrails); interfaces de contexto, que dizem ao modelo como buscar mais (tools, MCP, skills); e os arquivos do próprio repositório, que são o contexto mais básico. O eixo mais útil é quem decide carregar cada peça: o modelo (skills, com a incerteza de ele carregar ou não), o humano (slash commands, mais controle e menos automação) ou o software do agente em pontos fixos (hooks, determinísticos).
- **Por que existe:** as opções de configuração explodiram e precisavam de um mapa. A autora recomenda montar o contexto aos poucos, desconfiar de configurações copiadas de estranhos e lembra que não há teste unitário para context engineering. Fecha com o aviso de ilusão de controle: nenhuma dessas peças garante comportamento, porque a execução ainda depende de como o modelo interpreta o texto.
- **Fonte:** [Böckeler, "Context Engineering for Coding Agents"](https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html), 5 de fevereiro de 2026.
- **Confiança:** relato. O artigo de harness diz que o harness do usuário é uma forma específica de context engineering, o que bate com a HumanLayer (seção 2.4).

Para o desenho, o eixo "quem dispara" importa mais que a lista: uma peça que precisa rodar sempre não pode depender do modelo decidir carregá-la.

### 10.3 Spec-driven development: Kiro, spec-kit e Tessl

- **O que é:** uma tentativa de definir SDD olhando três ferramentas que usam o rótulo. A autora separa três níveis: spec-first (escreve a spec antes e usa na tarefa), spec-anchored (mantém a spec depois para evoluir a feature) e spec-as-source (só a spec é editada; o código é gerado). Também separa spec (vale para uma tarefa ou feature) de memory bank (contexto que vale para toda sessão: rules, descrição do produto e do codebase). As ferramentas, como ela as viu em setembro de 2025:
  - **Kiro:** fluxo de requisitos, design e tarefas, um Markdown para cada; requisitos como histórias de usuário com critérios no formato given, when, then. O memory bank se chama steering. Na prática, spec-first.
  - **spec-kit (GitHub):** CLI que monta arquivos e slash commands; o memory bank se chama constitution e é obrigatório; cada etapa (specify, plan, tasks) usa checklists como uma definição de pronto, interpretada pelo modelo. Fala em spec viva, mas cria uma branch por spec, o que ela lê como spec-first.
  - **Tessl:** em beta privado; o único que mira spec-anchored e experimenta spec-as-source, com uma spec por arquivo de código e o código marcado como gerado.
- **Por que existe:** SDD virou palavra da moda sem definição estável, e o termo "spec" já está sendo usado como sinônimo de prompt detalhado.
- **Fonte:** [Böckeler, "Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl"](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html), 15 de outubro de 2025. As ferramentas mudam rápido; o retrato é daquela data.
- **Confiança:** relato.

As críticas dela que importam para uma skill de spec:

- **Um fluxo para todos os tamanhos não serve.** O Kiro transformou um bug pequeno em quatro histórias com dezesseis critérios; o spec-kit, numa feature média, gerou tanto Markdown que ela acha que teria implementado mais rápido sem ele.
- **Revisar Markdown pode ser pior que revisar código.** Arquivos repetitivos entre si e com o código existente.
- **Falsa sensação de controle.** Mesmo com templates e checklists, o agente ignorava instruções (tratou a pesquisa sobre classes existentes como spec nova e duplicou tudo) ou seguia demais (aplicou um artigo da constitution com zelo excessivo).
- **Separar funcional de técnico é difícil**, e a profissão nunca foi boa nisso em histórias de usuário.
- **O paralelo certo para spec-as-source é model-driven development**, que nunca pegou em aplicações de negócio; o risco é juntar a rigidez do MDD com o não determinismo do LLM.

O valor que ela reconhece é o de spec-first. Isso reforça a separação entre spec e contexto da seção 4.2 com um par de nomes a mais (spec e memory bank).

### 10.4 Humanos fora, dentro e sobre o loop

- **O que é:** Kief Morris separa o why loop (transformar ideias em resultado, que é do humano) do how loop (construir o software), e mostra que o how loop tem vários níveis aninhados: o de fora especifica e entrega, os do meio quebram trabalho em tarefas e validam, o de dentro gera e testa código. Sobre essa estrutura, três posições:
  - **Fora do loop:** o humano fica só no why loop e deixa o how loop para o agente. É o vibe coding, e também algumas leituras de SDD.
  - **Dentro do loop:** o humano como porteiro do loop mais interno, inspecionando cada linha. Vira gargalo, porque o agente gera mais rápido do que se revisa.
  - **Sobre o loop (on the loop):** o humano constrói e mantém o harness (specs, checks de qualidade, orientação de fluxo) que controla os loops internos. O teste prático: quando o resultado não presta, quem está dentro do loop corrige o artefato; quem está sobre o loop corrige o harness que produziu o artefato.
  - O passo seguinte ele chama de agentic flywheel: o agente analisa os resultados de cada etapa e recomenda mudanças no harness; primeiro o humano aprova cada uma, depois elas vão para o backlog, e com confiança as de baixo risco podem ser aplicadas sozinhas.
- **Por que existe:** sair do falso dilema entre vibe coding e revisar tudo, aplicando ao agente o mesmo shift left que funcionou para humanos.
- **Fonte:** [Kief Morris, "Humans and Agents in Software Engineering Loops"](https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html), 4 de março de 2026. Ele cita a mesma ideia sob o nome middle loop, vinda dos workshops "The Future of Software Development" ([bliki, 2 de julho de 2026](https://martinfowler.com/bliki/FutureOfSoftwareDevelopment.html)). Numa nota, lembra que no Ralph original o operador tem papel ativo de conduzir o loop, ao contrário do uso coloquial de soltar agentes e esperar.
- **Confiança:** relato; a ideia de mudar o harness a partir de falhas é convenção (seção 4.2, item 4).

Isso dá um critério operacional para a parte Melhoria: toda correção feita à mão num artefato do loop é uma candidata a virar mudança no harness.

### 10.5 TDD dentro do loop do agente

- **O que é:** um experimento exploratório da Böckeler sobre o uso mais comum de TDD com agentes: mandar o próprio agente escrever o teste que falha, ver vermelho, implementar e ver verde, tudo dentro do loop dele. Ela comparou soluções com e sem instruções de TDD em tarefas pequenas, médias e grandes, com um modelo julgando a qualidade às cegas e mutation testing como medida de eficácia dos testes. Resultado, com as ressalvas dela (amostra muito pequena, tarefas greenfield de lógica de negócio): nenhuma vantagem clara do TDD; as soluções sem TDD ficaram à frente com mais frequência; e o TDD custou pelo menos três vezes mais tokens. A hipótese levantada é que, sem TDD, o agente desenha a solução inteira antes, e com TDD o desenho sai da soma de decisões locais tomadas a cada teste.
- **Por que existe:** saber se vale o esforço de fazer o agente seguir TDD. A análise objetivo por objetivo é o ponto central: o passo vermelho só prova algo se alguém olha por que ficou vermelho, e quando o agente escreve e confere o próprio teste isso não acontece; os agentes também pulavam ou fingiam o passo vermelho; e benefícios como YAGNI e confiança são humanos, não passam para o agente.
- **Fonte:** [Böckeler, "TDD inside the agent loop: theater or actual value?"](https://martinfowler.com/articles/exploring-gen-ai/tdd-in-the-agent-loop.html), 10 de agosto de 2026. Os dados estão no repositório citado no texto.
- **Confiança:** relato, com amostra pequena declarada.

O que ela propõe no lugar: parar de prescrever o processo e medir o resultado. Para qualidade de regressão, mutation testing; para refatoração, análise estática e revisões periódicas de estrutura; para confiança, approved scenarios (expectativas congeladas num runner próprio, que o humano reaprova quando mudam, abordagem que ela credita à Ivett Ördög). A conclusão geral dela é que ser muito específico sobre como o modelo deve trabalhar não se sustenta, e que o esforço deve ir para feedback automatizado sobre o resultado.

### 10.6 Sensores de manutenibilidade na prática

- **O que é:** a Böckeler montou, num app próprio, um conjunto de sensores e conta o que funcionou. Ela os distribui por quando rodam: durante a sessão (typecheck, lint, SAST, regras de dependência entre módulos, testes com cobertura, mutation testing incremental, scanner de segredos no pre-commit), no pipeline depois da integração (os mesmos, em infraestrutura limpa), de tempos em tempos (revisões inferenciais de segurança, de tratamento de dados, de dependências e de modularidade) e em produção.
- **Por que existe:** testar na prática o modelo de guias e sensores do artigo anterior. Ela deixou os guias de fora de propósito, para ver o efeito só dos sensores.
- **Fonte:** [Böckeler, "Maintainability sensors for coding agents"](https://martinfowler.com/articles/sensors-for-coding-agents.html), 27 de maio de 2026.
- **Confiança:** relato.

Achados que importam aqui:

- **Sensores computacionais funcionam bem no nível de arquivo e função**; os de acoplamento e modularidade entre arquivos são ruído sem um modelo para interpretar, ou seja, precisam de um sensor inferencial por cima.
- **Mutation testing vira essencial quando o agente escreve os testes**, porque cobertura alta com poucas asserções dá falsa segurança.
- **Instrução para rodar o sensor falha.** Pedir no AGENTS.md ou numa skill que o agente consulte os sensores foi a forma mais fácil e a menos confiável. Ela lista como alternativas hook do agente (depois de cada edição, com cuidado para não distrair), pre-commit do git e uma extensão própria no harness.
- **O resumo para o agente é diferente do resumo para o humano.** Ela escreveu uma CLI que roda os sensores continuamente e entrega ao agente um resumo curto, com limiares, tendência em relação a um snapshot e uma orientação global de correção. É o mesmo princípio da HumanLayer de mostrar só o que falhou (seção 5.1).
- **Medir o próprio sensor.** Sensor sempre verde é suspeito, sempre vermelho é sensível demais; ela passou a registrar o histórico de estados para ter dados. Também prevê conflitos entre sensores (regras de tamanho de função empurrando complexidade para outro lugar).

### 10.7 Até onde dá para empurrar a autonomia

- **O que é:** um fluxo de agentes que gerava uma aplicação Spring Boot de ponta a ponta sem intervenção humana, com prompts reutilizáveis, uma aplicação de referência servida por MCP como âncora de padrões, scripts determinísticos e análise estática. Funcionou para aplicações simples, com problemas que cresciam com a complexidade: features não pedidas, suposições que mudavam para tapar lacunas dos requisitos, correções na força bruta e, o mais relevante para a condição de parada, o agente declarando build e testes como sucesso quando não estavam, mesmo com a instrução explícita de que a tarefa não acaba com teste falhando.
- **Por que existe:** medir o limite da autonomia com os modelos da época. A conclusão é que um humano supervisionando continua essencial, e que o não determinismo deixa sempre uma probabilidade não desprezível de o agente fazer o que não se quer. Ela também registra o custo de desenvolver o próprio fluxo: cada ajuste de prompt levava de 10 a 20 minutos para mostrar efeito, e era difícil definir o que conta como sucesso de uma geração.
- **Fonte:** [Böckeler, "How far can we push AI autonomy in code generation?"](https://martinfowler.com/articles/pushing-ai-autonomy.html), 5 de agosto de 2025. A âncora em aplicação de referência tem memo próprio ([Anchoring AI to a reference application](https://martinfowler.com/articles/exploring-gen-ai/anchoring-to-reference.html), 25 de setembro de 2025).
- **Confiança:** relato. O agente que declara pronto cedo também aparece na Anthropic (seção 6.1) e numa nota do próprio Fowler (abaixo), então o fenômeno é convenção.

O Fowler, numa coletânea de notas de 28 de agosto de 2025, registra o mesmo incômodo (o modelo diz que os testes passam e eles falham) e duas ideias sobre não determinismo: alucinação é o que o modelo sempre faz, e às vezes ela é útil; por isso vale perguntar mais de uma vez e comparar, e não pedir ao modelo um cálculo que um programa faria de forma determinística, e sim o código que calcula ([Some thoughts on LLMs and Software Development](https://martinfowler.com/articles/202508-ai-thoughts.html)). Ele compara com outras engenharias, que sempre trabalharam com tolerâncias. **Relato.**

### 10.8 Segurança: a lethal trifecta

- **O que é:** Korny Sietsma parte de que o modelo não separa instrução de dado, então tudo o que ele lê pode virar instrução. O risco grave aparece quando o agente junta três coisas: acesso a dados sensíveis, contato com conteúdo não confiável e capacidade de se comunicar para fora. As mitigações que ele propõe: reduzir o acesso a cada um dos três; rodar o agente (e servidores MCP) em container, com sandbox como alternativa mais fraca; quebrar o trabalho em subtarefas que fiquem sem pelo menos um dos três; e dar passos pequenos que um humano revisa. Ele avisa que container não resolve tudo e critica o devcontainer que já vem com a flag de pular permissões.
- **Por que existe:** agentes com ferramentas mudam o modelo de ameaça de um LLM.
- **Fonte:** [Korny Sietsma, "Agentic AI and Security"](https://martinfowler.com/articles/agentic-ai-security.html), 28 de outubro de 2025. No mesmo site, Gautam Koul e Lucian Moss, em ["The VibeSec Reckoning"](https://martinfowler.com/articles/vibesec-reckoning.html) (27 de maio de 2026), defendem, para quem faz vibe coding, um harness seguro por padrão em vez de pedir segurança no prompt.
- **Confiança:** relato; container e sandbox como guardrail são **confirmados** pela doc oficial (seção 5.2).

Isso corrige a impressão da seção 5.3: o artigo de harness da Böckeler não trata segurança, mas o site trata, em outro autor. A trifecta é um critério útil para o perfil VPS da seção 8: a máquina remota com credencial de push e acesso a issues públicas tem as três pernas.

### 10.9 Quanto revisar: risco e os nomes do Fowler

- **O que é:** a Böckeler propõe decidir o nível de revisão do código gerado com os três fatores clássicos de risco: probabilidade de o agente errar (ferramenta, contexto disponível, quão favorável é o codebase), impacto se errar sem ninguém notar, e detectabilidade (testes, tipos, conhecimento do sistema). Baixa probabilidade, baixo impacto e alta detectabilidade permitem vibe coding; o oposto pede revisão pesada.
- **Por que existe:** sair do debate binário sobre revisar ou não código de IA.
- **Fonte:** [Böckeler, "To vibe or not to vibe"](https://martinfowler.com/articles/exploring-gen-ai/to-vibe-or-not-vibe.html), 23 de setembro de 2025.
- **Confiança:** relato.

O Fowler fixou dois termos no bliki em 21 de maio de 2026: [Vibe Coding](https://martinfowler.com/bliki/VibeCoding.html) (construir sem olhar o código, bom para software descartável e de público restrito) e [Agentic Programming](https://martinfowler.com/bliki/AgenticProgramming.html) (o humano dirige agentes e continua responsável pelo código, revisando código, testes e saída de outros sensores). Nesse verbete ele põe harness engineering, o trabalho com guias e sensores, como atividade central do programador. **Relato.**

Para a seção 8, os três fatores dão um jeito de escolher o perfil de harness por tarefa, não só por ambiente.

### 10.10 Estado compartilhado entre agentes

- **O que é:** num exercício com dez engenheiros e muitos agentes no mesmo monorepo, os agentes recebiam uma spec com seções numeradas, escreviam planos ligados a essas seções, guardados no repositório, e atualizavam o progresso neles. Com a regra de commitar e fazer rebase da main continuamente, cada agente passou a ver os planos dos outros e a usá-los para se coordenar: marcar uma linha como em andamento, esperar a dependência ficar pronta, ler as notas de como foi feita. O autor reconheceu ali o padrão blackboard (memória compartilhada que agentes autônomos leem e escrevem).
- **Por que existe:** foi um efeito acidental. O custo apareceu logo: commits frequentes sobrecarregaram o CI e eles recuaram, perdendo o fluxo de atualizações. A opinião do autor é que esse canal deveria existir fora do controle de versão, e ele começou uma ferramenta para isso.
- **Fonte:** [Giles Edwards-Alexander, "An Accidental Blackboard"](https://martinfowler.com/articles/exploring-gen-ai/an-accidental-blackboard.html), 2 de setembro de 2026.
- **Confiança:** relato.

Para este repositório, que roda um loop por vez, o ponto é menor: o arquivo de progresso da seção 4.3 é a versão de um agente só desse blackboard, e o problema de passá-lo pelo git só aparece com vários agentes em paralelo.

### 10.11 Outras peças menores

- **Interrogatory LLM** (Fowler, bliki, 14 de maio de 2026): em vez de o humano escrever o contexto de uma tarefa, pedir ao modelo que o entreviste, uma pergunta por vez, e escreva o documento para outra sessão executar; ou dar ao modelo uma spec pronta para ele validar com um especialista. Ele credita a técnica ao blog do Harper Reed. É o mesmo movimento das skills de grilling da seção 9.1. **Relato.** ([Interrogatory LLM](https://martinfowler.com/bliki/InterrogatoryLLM.html))
- **The Orchestrator's Tax** (Rahul Garg, 16 de julho de 2026): defende que o valor de um subagent é o que ele mantém fora do contexto do orquestrador, não a velocidade, e que o orquestrador precisa de regras explícitas de quando delegar. Li só o resumo e a estrutura; o próprio autor diz que é exploratório e baseado num incidente. **Relato.** ([The Orchestrator's Tax](https://martinfowler.com/articles/orchestrator-tax.html))
- **Qualidade interna com agente** (Erik Doernenburg, 27 de janeiro de 2026): exemplos de código que funcionava mas piorava o codebase (complexidade desnecessária, lógica duplicada, um cache sem motivo), pegos só por um desenvolvedor experiente. Reforça que a manutenibilidade precisa de sensor próprio. **Relato.** ([Assessing internal quality while coding with an agent](https://martinfowler.com/articles/exploring-gen-ai/ccmenu-quality.html))

### 10.12 O que isso muda no modelo

- **As três partes (spec, loop, verificação) continuam de pé, e o ajuste para oito partes da seção 4.3 também.** Nada no site pede uma parte nova. O material refina partes existentes: spec e contexto ganham o par spec e memory bank (10.3); o loop ganha a estrutura de loops aninhados e a posição do humano sobre o loop (10.4); o estado ganha a leitura de blackboard (10.10); a melhoria ganha o critério "corrigir o harness, não o artefato" e o flywheel (10.4).
- **A verificação se desloca de processo para resultado.** O memo de TDD e o de sensores apontam na mesma direção: instruir o agente sobre como trabalhar (TDD, rodar os checks) é frágil; medir o que ele produziu, com gatilho determinístico, é o que se sustenta. Isso também reforça que a verificação é distribuída (sessão, pipeline, agenda, produção), como já dizia a seção 4.2.
- **A distinção guardrail x verificação se mantém, com três ressalvas novas**, já anotadas na seção 5.3: o termo "guardrail" também aparece como sinônimo de convenção; um check obrigatório precisa de gatilho determinístico; e uma verificação que bloqueia precisa de um guardrail que impeça o agente de desarmá-la.

## 11. Onde as fontes concordam e divergem

**Concordam:**

- Harness é tudo em volta do modelo, e a maior parte do ganho vem dele, não de esperar um modelo melhor (HumanLayer, LangChain, OpenAI, Böckeler).
- A verificação é a peça de maior retorno, e precisa ser rápida, automática e legível pelo agente (todas).
- Uma tarefa por volta, estado em arquivos e git, contexto limpo ou compactado entre voltas (Huntley, Matt, Anthropic, LangChain).
- O harness se melhora a partir de falhas observadas, não de um desenho completo feito antes (Hashimoto, Huntley, HumanLayer, Böckeler, Anthropic).
- AGENTS.md curto, como mapa, com o detalhe em outros arquivos (OpenAI, HumanLayer).
- Instrução não garante comportamento: o agente declara pronto com teste falhando, pula passos pedidos ou ignora contexto, e o que segura isso é um check mecânico (Anthropic, Böckeler nos memos de context engineering, SDD, autonomia e sensores, Fowler).

**Divergem:**

- **Quem decide que acabou.** O Ralph original não decide: o humano para. O Matt e o Sandcastle usam a marca escrita pelo próprio agente. O `/goal` usa outro modelo lendo a conversa. A Anthropic usa um avaliador que testa o app de verdade, com limiar por critério.
- **Contexto novo ou mesma sessão.** O Ralph de script começa do zero a cada volta; o plugin oficial e o `/goal` mantêm a sessão. O Huntley critica o plugin; a Anthropic relata que, com modelo mais forte, a compactação passou a bastar.
- **Quanto do harness é segurança.** A Böckeler e a OpenAI quase não falam de isolamento; a LangChain e a doc do Claude Code põem sandbox no centro. No site do Fowler o tema existe, mas em artigo separado (Sietsma, seção 10.8), não dentro do modelo de harness.
- **TDD dentro do loop.** O Matt tem uma skill `tdd` entre as de verificação e o Huntley trata testes como backpressure; a Böckeler, num experimento pequeno, não viu ganho em mandar o agente seguir TDD, pagou várias vezes mais tokens e parou de pedir teste primeiro (seção 10.5). Não é bem uma contradição: todos querem testes como sinal; a divergência é sobre prescrever o processo ao agente.
- **Quanto de spec antes.** Huntley, Matt e Anthropic começam por uma spec escrita; a Böckeler valoriza spec-first, mas desconfia de muita spec antecipada e verbosa, e prefere passos pequenos (seção 10.3).
- **Portões de merge.** A OpenAI roda com poucos portões bloqueantes e resolve flake com nova execução, porque correção é barata e espera é cara; diz que isso seria irresponsável com pouco throughput. A Böckeler defende manter a qualidade à esquerda, com checks o mais cedo possível.
- **Notificações.** A HumanLayer e a doc oficial incentivam; o Hashimoto desliga.
- **Quanto o harness vai importar.** A Anthropic e a LangChain esperam que parte do harness seja absorvida pelo modelo; a Anthropic acrescenta que o espaço de combinações interessantes não encolhe, só se move.

## 12. Perguntas abertas para o desenho

Sem decisão aqui.

**Divisão do modelo**

1. A categoria `harness/` adota as oito partes da seção 4.3, ou um modelo menor (por exemplo spec, loop, verificação, guardrails, observabilidade)? Contexto e estado viram partes próprias ou ficam dentro de spec e loop?
2. O loop vira skill, ou segue o Matt e fica num script ou biblioteca, com as skills cobrindo só o que roda dentro dele?
3. Guardrail e verificação ficam em skills separadas mesmo quando usam o mesmo mecanismo (hooks)?

**Parada e observabilidade (as duas falhas observadas)**

4. Qual a condição de parada padrão: marca de conclusão, lista com `passes`, `/goal`, ou a combinação de uma delas com teto de iterações e custo?
5. Quem garante que a spec traga um estado final verificável antes de o loop começar? Uma checagem na skill de spec, uma pergunta obrigatória no grilling, ou o próprio script recusando rodar sem isso?
6. O script de loop sempre usa `stream-json`, ou isso vira opção? Onde fica o log de cada execução e quem limpa?
7. Qual o canal de aviso de fim ou travamento: hook de notificação local, push no celular, mensagem?

**Contextos**

8. Um harness só com perfis (interativo, AFK local, VPS) ou skills diferentes por contexto?
9. Para a VPS: Remote Control, routines na nuvem, ou um loop próprio num processo que sobrevive à desconexão? Que credencial de git a máquina recebe?
10. No modo interativo, quais peças valem a pena: Stop hook com typecheck, `retro` no fim da sessão, mais alguma?

**Empacotamento**

11. Reaproveitar skills do Matt (MIT) para spec, verificação e melhoria, adaptar, ou escrever do zero? Lembrando que uma skill não pode apontar para arquivos de outra (ADR 0002).
12. Um sensor inferencial (revisor com contexto limpo) entra no loop AFK como passo fixo ou só no fim?

**Material do site do Martin Fowler (seção 10)**

13. A skill `tdd` entra no loop AFK como instrução de processo, ou o loop mede só o resultado (testes verdes, mutation testing, approved scenarios) e deixa o TDD para o trabalho interativo?
14. Como o loop garante que os checks rodam: instrução na skill (pouco confiável, segundo a Böckeler), hook do agente, pre-commit do git ou o próprio script do loop?
15. Quem protege os testes de o agente apagá-los ou pulá-los para passar no checkpoint: um guardrail que nega edição em testes existentes, uma verificação do diff, ou o revisor com contexto limpo?
16. A spec padrão é só spec-first (vale para a tarefa e morre) ou spec-anchored (fica no repositório para evoluções)? E como a skill de spec escala o tamanho da spec ao tamanho do problema, para não repetir o caso do bug que virou dezesseis critérios?
17. Ficar sobre o loop vira regra: toda correção manual num artefato do loop gera uma proposta de mudança no harness? Quem registra (a `retro`, o próprio loop) e quem aprova?
18. O perfil de harness (seção 8) se escolhe também pelo risco da tarefa (probabilidade, impacto, detectabilidade), além do ambiente?

## 13. Fontes

Doc oficial do Claude Code (consultada em 2026-10-01):

- Glossary: https://code.claude.com/docs/en/glossary
- How Claude Code works: https://code.claude.com/docs/en/how-claude-code-works
- Keep Claude working toward a goal: https://code.claude.com/docs/en/goal
- Run prompts on a schedule (`/loop`): https://code.claude.com/docs/en/scheduled-tasks
- Hooks reference: https://code.claude.com/docs/en/hooks
- Hooks guide: https://code.claude.com/docs/en/hooks-guide
- Headless: https://code.claude.com/docs/en/headless
- CLI reference: https://code.claude.com/docs/en/cli-reference
- Agent view: https://code.claude.com/docs/en/agent-view
- Remote Control: https://code.claude.com/docs/en/remote-control
- Routines: https://code.claude.com/docs/en/routines
- Statusline: https://code.claude.com/docs/en/statusline
- Monitoring: https://code.claude.com/docs/en/monitoring-usage
- Best practices: https://code.claude.com/docs/en/best-practices
- Agent SDK, agent loop: https://code.claude.com/docs/en/agent-sdk/agent-loop
- Agent SDK, hosting: https://code.claude.com/docs/en/agent-sdk/hosting
- Agent SDK, secure deployment: https://code.claude.com/docs/en/agent-sdk/secure-deployment
- Plugin ralph-wiggum: https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum

Anthropic Engineering:

- Effective harnesses for long-running agents (Justin Young, novembro de 2025): https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Harness design for long-running application development (Prithvi Rajasekaran, março de 2026): https://www.anthropic.com/engineering/harness-design-long-running-apps

OpenAI:

- Harness engineering: leveraging Codex in an agent-first world (Ryan Lopopolo, fevereiro de 2026): https://openai.com/index/harness-engineering/

Matt Pocock:

- Repositório de skills: https://github.com/mattpocock/skills
- Getting Started With Ralph: https://www.aihero.dev/getting-started-with-ralph
- Here's How To Stream Claude Code With AFK Ralph: https://www.aihero.dev/heres-how-to-stream-claude-code-with-afk-ralph
- 11 Tips For AI Coding With Ralph Wiggum: https://www.aihero.dev/tips-for-ai-coding-with-ralph-wiggum
- Sandcastle: https://github.com/mattpocock/sandcastle

Geoffrey Huntley:

- Ralph Wiggum as a software engineer: https://ghuntley.com/ralph/
- everything is a ralph loop: https://ghuntley.com/loop/

Site do Martin Fowler (consultado em 2026-10-02):

- Índice da série Exploring Generative AI: https://martinfowler.com/articles/exploring-gen-ai.html
- Birgitta Böckeler, Harness engineering for coding agent users (2 de abril de 2026): https://martinfowler.com/articles/harness-engineering.html
- Birgitta Böckeler, Harness Engineering, first thoughts (17 de fevereiro de 2026): https://martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html
- Birgitta Böckeler, Maintainability sensors for coding agents (27 de maio de 2026): https://martinfowler.com/articles/sensors-for-coding-agents.html
- Birgitta Böckeler, Context Engineering for Coding Agents (5 de fevereiro de 2026): https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html
- Birgitta Böckeler, Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl (15 de outubro de 2025): https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
- Birgitta Böckeler, TDD inside the agent loop: theater or actual value? (10 de agosto de 2026): https://martinfowler.com/articles/exploring-gen-ai/tdd-in-the-agent-loop.html
- Birgitta Böckeler, How far can we push AI autonomy in code generation? (5 de agosto de 2025): https://martinfowler.com/articles/pushing-ai-autonomy.html
- Birgitta Böckeler, Anchoring AI to a reference application (25 de setembro de 2025): https://martinfowler.com/articles/exploring-gen-ai/anchoring-to-reference.html
- Birgitta Böckeler, To vibe or not to vibe (23 de setembro de 2025): https://martinfowler.com/articles/exploring-gen-ai/to-vibe-or-not-vibe.html
- Kief Morris, Humans and Agents in Software Engineering Loops (4 de março de 2026): https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html
- Giles Edwards-Alexander, An Accidental Blackboard (2 de setembro de 2026): https://martinfowler.com/articles/exploring-gen-ai/an-accidental-blackboard.html
- Erik Doernenburg, Assessing internal quality while coding with an agent (27 de janeiro de 2026): https://martinfowler.com/articles/exploring-gen-ai/ccmenu-quality.html
- Korny Sietsma, Agentic AI and Security (28 de outubro de 2025): https://martinfowler.com/articles/agentic-ai-security.html
- Gautam Koul e Lucian Moss, The VibeSec Reckoning (27 de maio de 2026): https://martinfowler.com/articles/vibesec-reckoning.html
- Rahul Garg, The Orchestrator's Tax (16 de julho de 2026): https://martinfowler.com/articles/orchestrator-tax.html
- Martin Fowler, Some thoughts on LLMs and Software Development (28 de agosto de 2025): https://martinfowler.com/articles/202508-ai-thoughts.html
- Martin Fowler, bliki Agentic Programming (21 de maio de 2026): https://martinfowler.com/bliki/AgenticProgramming.html
- Martin Fowler, bliki Vibe Coding (21 de maio de 2026): https://martinfowler.com/bliki/VibeCoding.html
- Martin Fowler, bliki Interrogatory LLM (14 de maio de 2026): https://martinfowler.com/bliki/InterrogatoryLLM.html
- Martin Fowler, bliki Future Of Software Development (2 de julho de 2026): https://martinfowler.com/bliki/FutureOfSoftwareDevelopment.html

Comunidade:

- Mitchell Hashimoto, My AI Adoption Journey: https://mitchellh.com/writing/my-ai-adoption-journey
- HumanLayer, Skill Issue: Harness Engineering for Coding Agents: https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents
- HumanLayer, Advanced Context Engineering for Coding Agents: https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md
- Vivek Trivedy (LangChain), The Anatomy of an Agent Harness: https://blog.langchain.com/the-anatomy-of-an-agent-harness/

Nota relacionada neste repositório:

- [guardrails-e-modo-afk.md](guardrails-e-modo-afk.md)
