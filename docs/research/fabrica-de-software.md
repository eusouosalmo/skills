# Fábrica de software com agentes: gatilhos, anatomia e custo

Resumo: uma fábrica de software é o passo seguinte ao loop AFK. Em vez de uma pessoa abrir a sessão, um gatilho (label numa issue, alerta de produção, relógio) inicia uma run de agente numa máquina descartável, e o resultado volta como PR para um humano decidir. As conclusões que as fontes sustentam:

1. **A peça difícil não é o agente, são os freios.** Todas as fontes com método (Matt Pocock, Anthropic, Tech Leads Club, Warp) dizem o mesmo com nomes diferentes: todo gatilho acelera, e sem checks automáticos, revisão automática, revisão humana, teto de tentativas e throttle a fábrica vira produtora de slop. O Matt manda ligar um gatilho por vez.
2. **O padrão se repete em todas as ferramentas** (convenção): fila de issues com label, label como estado, uma run por issue, um worktree ou sandbox por run, PR draft, merge humano.
3. **O caminho mais curto para um dev solo já é oficial**: `claude-code-action` disparado por label, o runner do GitHub (ou um runner próprio na VPS) e a skill `code-review` como segundo par de olhos. A VPS entra como executor, não como pré-requisito.
4. **Controle na fábrica, não no agente.** O caso mais rígido apresentado (máquina de estados, contrato com schema, token de uso único) nasceu de um experimento em que bots com regras só em prosa aprovaram PRs que se revertiam uns aos outros. Instrução em linguagem natural pede; código garante.
5. **Multiagente custa caro e rende pouco em código.** A Anthropic mede cerca de 15 vezes os tokens de um chat em sistemas multiagente e diz que a maioria das tarefas de código não se beneficia. O Akita chega ao mesmo lugar por benchmark próprio. Paralelismo vale para tickets independentes e para revisão e pesquisa.
6. **Custo e termos são o ponto mais instável.** Hoje a assinatura cobre GitHub Action com OAuth token, routines e `claude -p`, mas os limites pressupõem uso "ordinary, individual", e uma mudança de cobrança anunciada para junho de 2026 foi pausada, não cancelada.

Pesquisa feita em 2026-11-06, só leitura, sem ticket próprio. Complementa [harness-de-agentes.md](harness-de-agentes.md) e [guardrails-e-modo-afk.md](guardrails-e-modo-afk.md), que já cobrem harness, condição de parada, Ralph loop, Sandcastle como loop local, `stream-json`, sandbox, container, worktrees, permission modes e a lethal trifecta. Esses pontos aparecem aqui só por referência. A doc do Claude Code muda toda semana; confira a página antes de decidir.

## Sumário

1. [Método e níveis de confiança](#1-método-e-níveis-de-confiança)
2. [O que é uma fábrica](#2-o-que-é-uma-fábrica)
3. [Anatomia](#3-anatomia)
4. [O que o Matt Pocock publicou](#4-o-que-o-matt-pocock-publicou)
5. [O que o Akita mostra](#5-o-que-o-akita-mostra)
6. [O que os links e vídeos acrescentam](#6-o-que-os-links-e-vídeos-acrescentam)
7. [Custo e termos de uso](#7-custo-e-termos-de-uso)
8. [Segurança](#8-segurança)
9. [Arquiteturas em degraus, de 0 a 5](#9-arquiteturas-em-degraus-de-0-a-5)
10. [Onde as fontes concordam e divergem](#10-onde-as-fontes-concordam-e-divergem)
11. [Perguntas abertas](#11-perguntas-abertas)
12. [Fontes](#12-fontes)

## 1. Método e níveis de confiança

Fontes primárias: a doc oficial do Claude Code e da plataforma da Anthropic (preços, termos, routines, GitHub Actions, Code Review, OpenTelemetry), dois artigos de engenharia da Anthropic, os repositórios `mattpocock/skills` (commit `4ae2317`, 2026-10-31) e `mattpocock/sandcastle` (commit `ed8e716`, 2026-11-05), as páginas do AI Hero, os posts e repositórios do Fábio Akita, a skill the-judge, as páginas de produto de Warp, Unblocked, Cognee e Hermes Agent, e dois vídeos: a live da Tech Leads Club sobre fábrica agêntica e a palestra do CEO da Warp. Os vídeos foram lidos pela legenda automática e por quadros extraídos; nomes próprios na legenda vêm deformados e foram corrigidos pelo quadro quando possível.

Os mesmos níveis das notas anteriores:

- **confirmado**: doc oficial de produto ou arquivo do repositório, aberto nesta pesquisa.
- **convenção**: vários autores independentes fazem.
- **relato**: um autor afirma, ou um fornecedor fala de si, ou um número sem método. Números de página de produto sem metodologia aparecem marcados como marketing.

Artigos de engenharia da Anthropic contam como relato com dados internos: descrevem a experiência de uma equipe, não comportamento de produto. Tudo o que vem marcado como inferência é leitura minha a partir das fontes, não afirmação delas.

## 2. O que é uma fábrica

- **Definição.** No dicionário do AI Hero, software factory é um sistema em que gatilhos, e não pessoas, iniciam sessões de agente, para que mais trabalho rode AFK e o tempo com humano no loop fique para o que precisa dele. O mesmo dicionário chama de dark factory a parte do código que a fábrica escreve e nenhum humano revisa ([software-factory](https://www.aihero.dev/ai-coding-dictionary/software-factory), [dark-factory](https://www.aihero.dev/ai-coding-dictionary/dark-factory)). **Confirmado** como definição do autor.
- **A diferença para o loop AFK.** O loop das notas anteriores ainda é aberto por alguém. Na fábrica, quem abre é um evento, e cada run termina sem esperar resposta: a ação humana seguinte dispara outra run. **Confirmado** (skill `software-factory`, seção 4.1).
- **Os três tipos de gatilho** que aparecem em todas as fontes (convenção):
  - **Label ou evento no tracker.** Issue recebe `ready-for-agent` ou `agent:implement`, PR recebe review, CI falha. É o gatilho do Sandcastle, do `claude-code-action`, do OpenHands resolver e das automações da Warp.
  - **Alerta de produção.** Erro no Sentry, evento no PostHog, alarme de nuvem. Entra pelo mesmo funil de triagem que um pedido humano. A doc de routines usa literalmente um alerta do Sentry como exemplo do `/fire` ([routines](https://code.claude.com/docs/en/routines)).
  - **Relógio.** Uma tarefa por dia ou por semana: tirar um arquivo da lista de exceções do lint, varrer a arquitetura e abrir ticket, limpar feature flag parada, gerar resumo de uso.
- **Todo sinal passa pela mesma triagem.** A live da Tech Leads Club e a Warp insistem nisso: trabalho que nasce de alerta ou de relógio passa pelo mesmo fluxo que o pedido de uma pessoa, com o mesmo registro e os mesmos portões. **Convenção.**

## 3. Anatomia

As fontes dividem a fábrica em peças parecidas. O vocabulário mais enxuto é o da skill do Matt; o mais detalhado, o diagrama de camadas da live da Tech Leads Club; o mais orientado a produto, a "factory stack" da Warp. Juntando os três:

| Peça | O que faz | Como aparece nas fontes |
| :- | :- | :- |
| Gatilho | Decide que uma run deve começar | label, alerta, cron, outra run (Matt); intake com guardas (TLC); automations (Warp) |
| Fila e estado | Guarda o que está pendente, em andamento e feito | o tracker é a interface humana e o system of record; labels como máquina de estados |
| Orquestrador | Recebe gatilhos, inicia runs, impede duplicação | o workflow do GitHub Actions, um daemon próprio, Step Functions, o foreman da Warp |
| Runner | A máquina onde a run acontece, descartável | runner do Actions, microVM, plataforma gerenciada, VPS com container novo por run |
| Agente | Lê a tarefa, edita, devolve resultado | Claude Code, Codex, Cursor; sempre com as mesmas skills do time |
| Verificação | Diz se o trabalho está certo | checks automáticos, verificador dentro da implementação, QA sem permissão de editar |
| Revisão | Lê o diff a frio antes do merge | outra run, outro modelo, conta própria no GitHub; humano por risco |
| Observabilidade | Mostra o que rodou, quanto custou, onde falhou | página da run no Actions, OpenTelemetry, Langfuse, custo por PR |

Duas peças transversais aparecem só nas fontes de time: o **brain** (conhecimento da empresa acessível a pessoas e agentes, seção 6.5) e a **fundação** (repositório pronto para agente: build determinístico, testes rápidos, lint, instruções). A fundação é o que as notas de harness já chamam de harness; sem ela nada acima funciona, e o Akita diz o mesmo com "base antes de velocidade" (seção 5).

Cinco perguntas que a skill do Matt manda responder para cada tipo de tarefa, antes de construir (**confirmado**, `software-factory`): o que dispara, o que faz e em que serviços lê e escreve, o que dispara depois, onde o humano volta a entrar e o que impede duas runs de fazerem o mesmo trabalho. Para cada fonte de tickets, a pergunta equivalente é o que impede ticket duplicado.

## 4. O que o Matt Pocock publicou

### 4.1 A skill `software-factory`

- **O que é:** skill nova em 2026-10-31, no bucket `in-progress`, com `disable-model-invocation: true`. Não executa nada: é um glossário para desenhar uma fábrica numa sessão de grilling, mais um catálogo de tarefas de exemplo e um levantamento de produtos por função. **Confirmado** ([repo](https://github.com/mattpocock/skills/tree/main/skills/in-progress/software-factory)).
- **Vocabulário:** task (o tipo de trabalho, definido uma vez), trigger, run (uma execução que nunca espera humano), runner (máquina descartável, nada sobrevive à run), ticket tracker, git host, orchestrator e uma plataforma de observabilidade opcional.
- **Comece devagar.** Os três freios que ele lista são checks automáticos, revisão automática por outra run e revisão humana antes do merge. Ligar um gatilho por vez, com throttle (um bug a cada dez, relógio uma vez por dia), e limitar todo laço a poucas tentativas antes de devolver ao humano.
- **Tarefas de exemplo**, descritas com minhas palavras: explorar e triar issues; implementar ticket marcado como pronto e abrir PR draft; revisar automaticamente; retrabalhar só o que a revisão apontou, com label de espera por humano depois de N falhas; decompor uma spec em tickets com dependências; o "ratchet" de lint, um arquivo por dia; transformar falha da própria fábrica em ticket, sem deixar correções encadearem; varredura noturna de arquitetura que só abre ticket; e uma retro a cada dez PRs mergeados que propõe mudanças nas instruções da fábrica.
- **Runners**, levantamento de outubro de 2026: runner de CI (o workflow é o orquestrador e a página da run é a observabilidade), API de microVM (E2B, Daytona, Modal, Vercel Sandbox), plataforma de agente empacotada (Claude Code na web, Managed Agents, Codex cloud, Copilot coding agent), worker próprio de plataforma e VPS ou containers próprios. A VPS é recomendada quando as runs são longas ou pesadas, quando o custo por hora domina ou quando já existe um servidor. O runner pode mudar por tarefa.
- **O design mínimo** que a skill descreve é "tudo no GitHub": Issues como tracker, Actions como orquestrador e runner, sem observabilidade extra.

### 4.2 `chief-of-staff`, `loop-me` e o que ficou privado

- **chief-of-staff** (in-progress): sessão longa que coordena subagentes em background, guarda memória num wiki com cada afirmação datada e ligada a um commit, roda uma retro a cada cerca de cinco sessões de subagente e usa `to-spec`, `to-tickets` e `implement-spec` para trabalho grande. É a camada que decide o que vai para a fila. **Confirmado.**
- Um PR que ensinava essa skill a despachar para a fábrica e coletar o resultado pelo id da run foi fechado em 2026-11-05: a regra foi para uma skill privada. O texto do PR diz que a fábrica dele tinha rodado só duas vezes até então. **Confirmado** pelo texto do PR ([#1387](https://github.com/mattpocock/skills/pull/1387)); a fábrica em si não é pública.
- **loop-me** (in-progress): grilling cujo único produto é a spec de um workflow, com gatilho, checkpoint humano, a regra de empurrar esse checkpoint o mais para o fim possível e um resumo para o humano decidir rápido. Serve para especificar cada tarefa antes de construir. **Confirmado.**
- **Lacunas que o próprio repo registra** na doc de triagem: um ticket especificado mas bloqueado por outro também aparece como `ready-for-agent`, e falta um estado terminal "implementado, aguardando verificação"; sem ele, um runner AFK pode enfileirar de novo o que já terminou. A versão atual do `setup-matt-pocock-skills` traz o comando que conta bloqueadores abertos pelas dependências nativas do GitHub (zero significa que pode começar). **Confirmado.**
- O repo também registra que o limite de recursão de subagentes é responsabilidade do harness, não da skill. Numa VPS sem supervisão, o teto fica no orquestrador. **Confirmado.**

### 4.3 Os workflows do Sandcastle

O Sandcastle (biblioteca TypeScript, MIT, versão 0.14.0 de 2026-11-02) já aparece em [guardrails 6.3](guardrails-e-modo-afk.md#63-sandcastle) como loop local. O que esta pesquisa acrescenta é como o próprio repositório dele usa issues para disparar agentes, em três formas. **Confirmado** pelos arquivos no commit `ed8e716`.

1. **Laço local planner, implementers, reviewer e merger.** A cada iteração, até dez, um agente planejador lê as issues com `ready-for-agent`, monta um grafo de dependências (depende de código de outra, mexe nos mesmos arquivos, depende de decisão de API) e devolve só as desbloqueadas, cada uma com uma branch de nome determinístico para poder replanejar sem perder progresso. Até quatro implementers rodam em paralelo, cada um no seu container; se houve commit, um revisor roda no mesmo container; no fim, as branches à frente são mergeadas. Issue com cara de PRD e filhas não é trabalhada.
2. **Fábrica no GitHub Actions disparada por label**, com vocabulário próprio de prefixo `agent:`. `agent:explore` tria em lote e transforma o veredito em label (fácil vai para implementar, precisa de humano vai para `ready-for-human`, bloqueado vai para `agent:blocked`). `agent:implement` recusa sub-issue, issue em formato de PRD e issue que já tem PR; troca a label para `agent:in-progress`, roda o Claude Code, abre PR draft, pede revisão automática, marca bloqueio em falha e sempre remove o "em andamento". Um grupo de `concurrency` por número da issue impede duas runs na mesma issue, com timeout de 60 minutos. Há ainda labels para revisar, retrabalhar a partir de comentários e resolver conflito de branch.
3. **Daemon externo.** Um script no repo é chamado uma vez por tarefa com branch, base e número da issue em variáveis de ambiente; cria worktree e container, roda implementer e revisor, e o daemon empurra os commits e abre o PR. O daemon é privado; só o contrato do lado do repositório é visível. Serve de modelo para quem escrever o próprio orquestrador.

Os comentários dos workflows trazem os cuidados de segurança da seção 8: título e corpo de issue não entram em shell nem em expressão do workflow, vão para um arquivo lido por script; PR de fork usa `pull_request`, não `pull_request_target`, para não receber segredos; o token do Claude fica em secret.

### 4.4 Outras publicações

| Data | O quê | Confiança |
| :- | :- | :- |
| 2026-04-30 | Vídeo apresentando o Sandcastle como fábrica AFK de código aberto | confirmado pela descrição; vídeo não assistido |
| 2026-01-08 (atualizado) | Guia do Ralph: mesmo prompt em laço, uma tarefa por iteração, começar com humano e só depois AFK, teto de iterações, Docker | confirmado (já em guardrails 6.2) |
| 2026-11-09 a 2026-11-20 | Cohort pago sobre fábricas, com construção de uma fábrica em GitHub Actions na segunda semana | confirmado pela página de venda; conteúdo não acessado |
| palestra no AI Engineer | Divisão em turno do dia (humano planeja) e turno da noite (agentes implementam) | relato de agregadores; palestra não aberta |

## 5. O que o Akita mostra

O Fábio Akita escreve em pt-BR e publica o próprio processo. Ele não monta uma fábrica com gatilhos automáticos: roda as skills a mão, uma linha por dia em cada projeto. O que ele mostra serve como contraponto e como fonte de freios. Posts e repositórios abertos nesta pesquisa; os números são dele, sem auditoria externa (**relato**).

- **Separar julgamento de execução.** No repositório [my-skills](https://github.com/akitaonrails/my-skills), uma skill audita issues e outra audita PRs, decidindo o que é verdade e o que entra; uma terceira só executa o que a auditoria aprovou, um ticket por vez, com teste de regressão antes do fix, sem rediscutir a auditoria. Lote com mais de três tickets exige uma auditoria do estado combinado antes do push, porque revisão de um diff só não vê a interação entre mudanças. **Confirmado** pelos arquivos.
- **Texto de issue e PR é evidência não confiável, nunca instrução.** A skill de auditoria não roda comando copiado de issue: reconstrói uma reprodução sintética. **Confirmado.**
- **Base antes de velocidade.** O post sobre fazer mais deploy defende que corrigir depois ficou barato, mas só em cima de testes de cenário, CI em toda mudança, revisão adversarial automática, feature flags, staging e rollback rápido; ele mesmo lista as exceções (dinheiro, migrations destrutivas, bibliotecas públicas) e admite que a evidência é de projetos em que é dono único ([post](https://akitaonrails.com/2026/09/22/parem-de-inventar-desculpas-e-facam-mais-deploy-a-premissa-mudou/)). Ele estima que as skills de revisão resolvem cerca de 99% e que o furo é duplicação entre PRs. **Relato.**
- **Contra multiagente.** No post sobre harness e loop engineering ele argumenta que falha se compõe (90% por passo em dez passos dá cerca de 35%) e relata que um modelo caiu de 91 para 24 pontos sob um orquestrador no benchmark dele; noutro benchmark, nenhuma combinação planner mais executor foi melhor e mais barata que o modelo forte sozinho num harness maduro. Orquestração só se justifica para trabalho paralelo independente e para frota sem supervisão ([hot take](https://akitaonrails.com/2026/08/18/hot-take-harness-loop-engineering-graph-engineering-sao-bullshit/), [planner e executor](https://akitaonrails.com/2026/04/25/llm-benchmarks-vale-a-pena-misturar-2-modelos/)). **Relato com benchmark próprio.**
- **Oráculo.** O agente rende onde há algo verificável (testes, docs, saída esperada); sem isso o loop gira no vácuo ([post](https://akitaonrails.com/2026/10/12/llms-agentes-competente-o-suficiente/)). **Relato**, e coincide com o que a nota de harness chama de verificação.
- **Sandbox e backup em vez de prompt de permissão.** Roda agentes em modo sem confirmação dentro do [ai-jail](https://github.com/akitaonrails/ai-jail) (só o projeto gravável), com snapshots do sistema de arquivos e backup externo. O README do ai-jail diz que ele não protege contra código hostil, só contra acidente de um agente confiável; para hostil, VM descartável. Agente nunca tem acesso a produção; mudança de infra vira código promovido por humano via PR ([post](https://akitaonrails.com/2026/07/11/como-me-precaver-pros-meus-agentes-nao-apagarem-minhas-coisas/)). **Confirmado** (README) e relato (prática).
- **Cota e handoff.** Usa planos Max de dois fornecedores e alterna de harness quando bate o limite, com um widget que mostra o uso de cada um; a memória de handoff mora num serviço próprio ([ai-memory](https://github.com/akitaonrails/ai-memory)). **Relato.**
- **Cada regra é uma cicatriz.** Toda regra de skill nasce de um erro real, skill sem uso é dívida, e copiar skill de outro é assinar contrato sem ler ([post](https://akitaonrails.com/2026/09/17/falando-um-pouco-sobre-minhas-skills-de-ia/)). Converge com a regra deste repositório de só criar skill a partir de falha observada.

Ressalva dele mesmo: o volume que relata (centenas de PRs, jornadas longas) é de um dev sênior com audiência que gera contribuidores, e várias conclusões ele marca como especulação ou benchmark pequeno.

## 6. O que os links e vídeos acrescentam

### 6.1 Revisão em camadas

- **O artigo da Anthropic** sobre revisão de código no time do Claude Code ([claude.dev](https://claude.dev), 2026-10-15) troca a pergunta "um humano leu?" por "o que pode dar errado e que verificação pega isso?". Em vez de um portão único, camadas: o agente roda testes, build e lint e mostra a saída antes do PR; um subagente com contexto limpo revisa o diff; revisão por IA em todo PR, com vários caçadores e um grupo de verificadores que só deixa passar achado com concordância; security review que bloqueia; CI obrigatório; aprovação humana escalada por risco da mudança (não do autor), em que aprovação de agente nunca conta como humana e vale só para um commit específico; merge queue, flags, release gradual e rollback. **Relato com dados internos.**
- **Convergência da revisão.** O mesmo artigo conta um PR que passou por mais de cinquenta rodadas de revisão e correção durante a noite até o autor parar; daí o teto de três rodadas, a re-revisão só do diff novo e a regra de nunca repetir achado já postado. Incidentes viram casos de eval do revisor, rodados todo dia. **Relato.**
- **Números que eles publicam**, todos internos: merges no Claude Code mais que dobraram de junho a setembro enquanto a fração revertida caiu mais de 40%; PRs com comentário substantivo de revisão foram de 16% para 54%. **Relato.**
- **O que é produto e o que não é.** O Code Review gerenciado é Team e Enterprise, cobrado por tokens, lê `REVIEW.md` do branch base e "never approves or blocks"; o check não falha. Para um dev solo, a doc lista alternativas: `/code-review` local, Ultrareview, a action no próprio CI ou um revisor próprio como skill ([code-review](https://code.claude.com/docs/en/code-review)). **Confirmado.**
- **the-judge** ([tech-leads-club/agent-skills](https://github.com/tech-leads-club/agent-skills), Felipe Rodrigues, CC-BY-4.0) é uma skill de revisão que chega às mesmas ideias por outro caminho: poucos comentários, todos com prova (arquivo e linha conferidos, ou URL oficial buscada na hora); teto de nits; nada que lint ou testes já pegam; roda os checks do CI e um scanner de gambiarras no diff antes de ler; tenta reproduzir bloqueadores e descarta o achado se a reprodução falha; passa o texto por um portão determinístico antes de postar; tudo visível na primeira rodada sai na primeira rodada, com teto de três. Não publica dado de eficácia. Detalhe que importa para quem é autor único: o GitHub recusa aprovar ou pedir mudança no próprio PR, então o veredito vira comentário. **Confirmado** pelo SKILL.md e scripts; método descrito com minhas palavras.
- **A régua comum** (convenção entre Anthropic, the-judge e Warp): vários achadores mais um passo de verificação que filtra, evidência obrigatória, teto de nits, pré-existente separado, teto de rodadas, humano gasto por risco, e incidentes ou tarefas antigas viram eval.

### 6.2 Controle na fábrica: a live da Tech Leads Club

Live em pt-BR de 2026-11-03, publicada em 2026-11-04 ([vídeo](https://www.youtube.com/watch?v=5UwvjCVPigM)), com Waldemar Neto, Felipe Rodrigues e William Fernandes. **Relato** em tudo: são experiências dos apresentadores, e o repositório do caso mais rígido não é público.

- **O loop V2.** Todo sinal entra pela triagem; o humano fica com a intenção (pesquisa, PRD, design doc) e com os portões; implementação e verificação correm com mínimo de humano, paralelizadas em worktrees ou cloud agents; a revisão humana valida o que o agente não conseguiu e a direção. Eles citam um caso público em que mais da metade dos PRs de uma empresa passou a ser aprovada sem humano, com a ressalva de que não se sabe a profundidade desses PRs.
- **Assistente pessoal x teammate.** O teammate trabalha para o time, tem identidade própria em cada ferramenta (conta no GitHub, app no tracker, bot no chat), deixa o trabalho numa issue visível, tem permissões mínimas (cria, edita, comenta, não apaga) e é medido por custo e tempo por issue. Pedir no chat ou criar a issue tem o mesmo efeito: tudo entra pelo mesmo funil.
- **Execução no agente, controle na fábrica.** O caso do Felipe nasceu de um experimento com bots acordados por webhook em que, num dia, saíram oito PRs aprovados, quatro deles revertendo os outros quatro, e o bot líder passou a fazer tudo sozinho: nada o impedia de ignorar as regras escritas. A versão seguinte põe o agente na quinta de oito etapas. A fábrica (uma máquina de estados com histórico) recebe o evento, filtra com guardas das mais baratas para as mais caras (inclusive um teto de eventos por hora antes de chamar qualquer modelo), escolhe o executor pela cota livre com disjuntor, entrega ao agente uma tarefa com campos de resultado fixos e um token de uso único, e valida o retorno contra um schema campo a campo. O agente devolve JSON; não segura chave, não publica, não decide. Só a fábrica escreve o resultado de deploy, CI e testes, porque o agente nunca pode afirmar o que já aconteceu. O veredito do revisor só vale para o `head_sha` revisado; até três rodadas de retrabalho, depois falha ou espera humano. Depois do merge, a fábrica espera uma janela, mede contra limiares e, se falhar, primeiro recua a produção e depois prova o revert. Sem retry automático nas etapas de agente: estourou o tempo, falha, porque retry cego em agente queima dinheiro.
- **Quando isso é demais.** O próprio Waldemar chama de exemplo avançado e diz que para tarefa pequena é overengineering; a rigidez se justifica num incidente de madrugada sem plantão. Endurecer só o trecho que precisa.
- **Por onde começar**, na ordem deles: padronizar o fluxo em skills que humanos e agente usam, criar um agente que usa essas skills, dar a ele um brain e só então integrar ferramentas e pensar em fábrica como código.
- **Escolha de modelo por impacto.** A triagem classifica a issue em impacto baixo, médio ou alto (reversibilidade, superfícies tocadas, auth, pagamento, dados pessoais) e o nível poderia escolher o modelo. Hoje eles usam o modelo mais forte em tudo, porque corrigir bot sai mais caro.

### 6.3 Medição e melhoria: Warp

Palestra de Zach Lloyd, CEO da Warp, em 2026-10-19 ([vídeo](https://www.youtube.com/watch?v=x-PK3yx_MJg)), e a página do produto ([Warp Factories](https://www.warp.dev/factories)). **Relato de fornecedor**; os números de painel não têm metodologia (marketing).

- **Fábrica como código.** Agentes, automações, runners e MCPs declarados em arquivos versionados num repositório; a interface mostra a configuração como somente leitura porque ela mora no GitHub. Isso permite testar e reverter versões da fábrica.
- **Um foreman** recebe tudo e despacha etapas com portão para agentes de triagem, spec, implementação e revisão. Humanos revisam spec, código e produto.
- **Medição.** Painel com interações humanas por PR, tempo de ciclo por trecho e custo por PR fatiado por fonte, usuário, agente e modelo. Scorers com LLM como juiz avaliam runs inteiras com amostragem, porque rodar em todas custa. Tarefas reais viram benchmark e podem ser reexecutadas com outra combinação de modelo e harness.
- **Auto-melhoria.** Agentes observadores leem runs reprovadas, acham o problema repetido e abrem PR contra a definição da fábrica; no painel mostrado, um quarto dessas propostas foi aprovado. O exemplo aberto é um agente de triagem que recebia a instrução de delegar pesquisa mas não tinha permissão de criar subagentes.
- **Resultado declarado:** custo por PR de cerca de US$ 55 para cerca de US$ 15 em seis semanas. Marketing, sem método.
- **Para quem não compra o produto**, o vocabulário serve de mapa: gatilho, triagem, spec, implementação, verificação, revisão, merge humano, monitoramento, custo por PR, issues fechadas como benchmark. Inferência minha.

### 6.4 Multiagente e custo de tokens

- O artigo da Anthropic sobre o sistema de pesquisa multiagente ([engineering](https://www.anthropic.com/engineering/multi-agent-research-system)) mede que agentes gastam cerca de 4 vezes os tokens de um chat e sistemas multiagente cerca de 15 vezes. O ganho aparece em tarefas valiosas, muito paralelizáveis, com informação maior que uma janela de contexto; e o artigo diz que a maioria das tarefas de código tem menos partes paralelizáveis que pesquisa. **Relato com dados internos.**
- Lições do mesmo artigo que valem para a fábrica: delegar com objetivo, formato de saída, ferramentas e limites explícitos, senão subagentes duplicam trabalho; começar a avaliação com uns vinte casos, porque efeitos grandes aparecem cedo; para agentes que mudam estado, avaliar o estado final; retomar de checkpoint em vez de recomeçar; subagentes gravam a saída em arquivo e passam só a referência.
- Agent teams do Claude Code, experimentais, usam cerca de 7 vezes mais tokens em plan mode, recomendam começar com 3 a 5 colegas e não rodam em `-p` nem no Agent SDK ([agent-teams](https://code.claude.com/docs/en/agent-teams), [costs](https://code.claude.com/docs/en/costs)). **Confirmado.**
- Junto com o benchmark do Akita (seção 5), a leitura comum é: multiagente para ler (pesquisa, revisão com várias passadas, triagem), um agente sequencial para implementar cada issue, paralelismo só entre issues independentes. **Convenção.**
- Para o dev solo, o teto real de paralelismo é o rate limit da conta e a capacidade de revisar PR: se a fila de revisão cresce, paralelizar mais só aumenta estoque. Inferência minha.

### 6.5 Memória e contexto

- **Oficial:** `CLAUDE.md` curto, lido em toda execução; fluxo específico vai para skill; CLI como `gh` gasta menos contexto que MCP; issue template reduz turnos ([costs](https://code.claude.com/docs/en/costs#reduce-token-usage)). **Confirmado.**
- **Bases externas** vendem memória ou contexto para agentes: [Unblocked](https://getunblocked.com) liga código, chat, issues e docs num grafo e ranqueia fontes por recência e autoridade (SaaS, sem self-host fora do plano Enterprise); [Cognee](https://www.cognee.ai) é memória em grafo com núcleo de código aberto (Apache-2.0) e servidor MCP. Os números das páginas (menos tokens, mais rápido) vêm de uma tarefa rodada duas vezes ou de depoimentos. **Marketing.** Na live da Tech Leads Club, o brain do teammate é o Unblocked, usado para saber qual de duas regras conflitantes é a mais nova.
- **Leitura para dev solo**, inferência minha que as fontes de time também fazem: o problema que essas bases resolvem é conhecimento espalhado entre muitas pessoas e ferramentas. Num repositório de uma pessoa, `CLAUDE.md`, `CONTEXT.md`, ADRs, issues bem escritas e a memória do próprio harness cobrem quase tudo, são auditáveis em git e não exigem banco. A ideia aproveitável é minerar comentários de revisão aceitos e rejeitados para virar regra, o que a the-judge faz ao sugerir promover achados determinísticos a lint.

### 6.6 Agente residente: Hermes

O [Hermes Agent](https://github.com/NousResearch/hermes-agent) (Nous Research, MIT) é um agente de longa duração para rodar no próprio servidor, com cron em linguagem natural, gateway para apps de mensagem, memória entre sessões e skills no formato do agentskills.io. É o que o teammate da live usa, por cima do Claude Code numa VPS. **Confirmado** como existência pelo repositório; o site hermesagents.net é de fã, não oficial, e traz contagens contraditórias.

Dois atritos com este repositório, inferência minha: o Hermes cria e altera as próprias skills com a experiência, o que conflita com a regra de só mudar skill com eval contra baseline; e ele tem um modo que expõe a sessão de uma assinatura como endpoint compatível com a OpenAI, o que tende a esbarrar nos termos de uso da assinatura (seção 7.3). A alternativa conservadora é `claude -p` disparado por cron ou pelo GitHub Actions.

## 7. Custo e termos de uso

Preços e termos conferidos em 2026-11-06. É a parte que mais muda: reconfira antes de decidir.

### 7.1 Preço de API

Por milhão de tokens ([pricing](https://platform.claude.com/docs/en/about-claude/pricing)). **Confirmado.**

| Modelo | Input | Cache write 5 min | Cache hit | Output |
| :- | -: | -: | -: | -: |
| Fable 5.1 | US$ 10 | 12,50 | 0,25 | 50 |
| Opus 5.5 | 4 | 5 | 0,20 | 20 |
| Sonnet 5.5 | 2 | 2,50 | 0,10 | 10 |
| Haiku 5.5 (até 100k de prompt) | 0,10 | 0,125 | 0,01 | 0,50 |

Batch tem 50% de desconto, mas não serve para sessão agêntica. Managed Agents somam US$ 0,08 por hora de sessão em execução.

### 7.2 Assinatura

| Plano | Preço por mês | Crédito de API incluso |
| :- | -: | -: |
| Pro | US$ 20 | não |
| Max | US$ 100 | US$ 100 |
| Ultra | US$ 200 | US$ 200 |

O crédito vai para uma org do Console vinculada e cobre Claude API, Managed Agents, Agent SDK e `claude -p` rodado com a API key dessa org; não cobre o Claude Code logado na assinatura nem as runs da GitHub Action, e não acumula ([claude.com/pricing](https://claude.com/pricing), [API credits](https://platform.claude.com/docs/en/about-claude/api-credits-for-subscribers)). **Confirmado.**

### 7.3 O que os termos permitem

- Os limites de Pro, Max e Ultra "assume ordinary, individual usage of Claude Code and the Agent SDK". O OAuth da assinatura serve ao uso comum do Claude Code e dos apps nativos; quem constrói produto ou serviço deve usar API key; rotear requisições de terceiros pela credencial da assinatura é proibido, e a Anthropic se reserva o direito de agir sem aviso ([legal](https://code.claude.com/docs/en/legal-and-compliance)). **Confirmado.**
- Ao mesmo tempo, a doc **documenta** a assinatura na GitHub Action (`CLAUDE_CODE_OAUTH_TOKEN` gerado com `claude setup-token`) e nas routines ([github-actions](https://code.claude.com/docs/en/github-actions), [routines](https://code.claude.com/docs/en/routines)). **Confirmado.** Leitura minha: rodar a própria fábrica nos próprios repositórios com a própria assinatura é uso previsto; servir terceiros ou revender não é; rodar 24 horas por dia é onde "ordinary, individual" deixa de valer.
- **A mudança de junho de 2026.** Anunciada em maio, tiraria Agent SDK, `claude -p`, GitHub Actions e apps de terceiros dos limites da assinatura para um crédito mensal separado. Foi pausada; hoje tudo isso ainda conta contra a assinatura ([artigo de suporte](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan)). **Confirmado** o status em 2026-11-06; o risco de voltar é real.
- Em time ou organização, a fábrica cai nos Commercial Terms (Team, Enterprise ou API) e não pode rodar na assinatura pessoal de ninguém; a doc indica API key ou workload identity em vez de segredo estático, e Zero Data Retention desliga cloud sessions, routines, Code Review e Managed Agents ([legal](https://code.claude.com/docs/en/legal-and-compliance)). **Confirmado.**

### 7.4 Custo por tarefa

- Média oficial em empresas: cerca de US$ 13 por dev por dia ativo e US$ 150 a 250 por mês ([costs](https://code.claude.com/docs/en/costs)). **Confirmado.**
- Estimativa de terceiros: PR de bug entre US$ 1,50 e 3, de feature entre 3 e 6, no Sonnet; tarefa autônoma gasta 5 a 10 vezes os tokens de uma sessão focada. **Anedótico**, modelos de estimativa sem medição.
- **Cenário meu**, premissas explícitas: 3 milhões de tokens de input por tarefa com 90% de cache, 300 mil de cache write, 60 mil de output, revisão automática custando um terço disso. Dá cerca de US$ 2 por tarefa com Sonnet 5.5 e cerca de US$ 4 com Opus 5.5, antes de retrabalho. Vinte tarefas por mês cabem no crédito de API do Max; cem por mês, espalhadas, provavelmente cabem na assinatura; quatrocentas saem do uso individual e pedem API key com teto de gasto. Os limites da assinatura não são publicados em tokens, então "cabe" é palpite: medir com `/usage` e OpenTelemetry no piloto.
- **Medir custo por issue** é possível com o OpenTelemetry nativo: `OTEL_RESOURCE_ATTRIBUTES` marca todas as métricas de uma execução (por exemplo com o número da issue), e a métrica de custo já vem com modelo, skill e agente ([monitoring-usage](https://code.claude.com/docs/en/monitoring-usage)). **Confirmado** o mecanismo; o uso para custo por issue é inferência.

## 8. Segurança

A base está em [guardrails 3.9, 3.10 e 7](guardrails-e-modo-afk.md) e em [harness 10.8](harness-de-agentes.md#108-segurança-a-lethal-trifecta). O que a fábrica acrescenta é que a entrada deixa de vir de você.

- **Runner efêmero.** Nada sobrevive à run: container novo por run, runner do Actions em modo efêmero, memória só no tracker, no git e no orquestrador (Matt, `software-factory`). Na VPS, isso é responsabilidade sua: usuário não root, sem `~/.ssh` montado, rede de saída restrita. **Confirmado** como recomendação das fontes.
- **Permissões mínimas por tarefa.** Token de vida curta por repositório, de preferência um GitHub App com Contents, Issues e Pull requests; nunca PAT estático num fluxo com entrada externa, porque ele pode ser recuperado por prompt injection ([github-actions](https://code.claude.com/docs/en/github-actions)). Tarefa de triagem só lê. Identidade própria do agente, permissões de criar, editar e comentar, sem apagar (live da TLC). Na nuvem da Anthropic, as credenciais de git ficam fora da VM e um proxy as injeta; na VPS, imitar isso com um proxy de saída é inferência minha. **Confirmado** e inferência, como marcado.
- **Commits do `GITHUB_TOKEN` padrão não disparam CI**: deixe o action autenticar como GitHub App. Workflow agendado só roda do branch padrão e, em repo público, é desligado após 60 dias sem atividade. **Confirmado** ([github-actions](https://code.claude.com/docs/en/github-actions)).
- **Entrada não confiável.**
  - Título, corpo e comentários de issue nunca entram em shell nem em expressão do workflow; vão para arquivo lido por script (workflows do Sandcastle). **Confirmado** pelo arquivo.
  - O action só aceita gatilho de quem tem write access e barra bots por padrão; liberar usuários sem write "bypasses the primary security mechanism". Ele remove comentários HTML, caracteres invisíveis e texto oculto, mas avisa que técnicas novas de bypass podem surgir ([security.md](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md)). **Confirmado.**
  - Em PR, o action restaura `.claude/`, `.mcp.json` e `CLAUDE.md` do branch base, e o Code Review lê `REVIEW.md` do base: PR não reescreve as regras do revisor. Mas `package.json`, lockfile e `Makefile` ficam no head, então hook que roda script de pacote executa código do PR. **Confirmado.**
  - O `/fire` das routines rotula o payload como não confiável e exige que o prompt salvo diga explicitamente para agir sobre ele. **Confirmado.**
  - Alerta de produção carrega texto controlado pelo usuário final (mensagem de erro, URL, user agent). Tratar como issue de um estranho: nenhum segredo no ambiente do agente que lê alerta, saída de rede restrita e PR como única saída. Na demo da TLC, a issue gerada a partir de erro marca o bloco como dado externo a não seguir. Inferência minha mais relato.
- **Humano no fim por desenho.** O action não abre PR sozinho, commita numa branch e dá o link; routines empurram só para branches `claude/`; e uma branch protection que a credencial do agente consegue contornar não bloqueia nada. **Confirmado** ([security.md](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md), [routines](https://code.claude.com/docs/en/routines)).
- **Uma run por issue e teto de tentativas**: grupo de `concurrency` ou lock, e um estado de bloqueio depois de N falhas. Retry automático em etapa de agente é dinheiro queimado (TLC). **Convenção.**

## 9. Arquiteturas em degraus, de 0 a 5

Síntese minha, ordenada pelo que cada degrau acrescenta. Cada um só faz sentido quando o anterior roda sem surpresa, que é o "comece devagar" do Matt e o "por onde começar" da TLC. Os nomes das peças vêm das fontes; a escada não está em nenhuma delas.

| Degrau | O que é | Gatilho | Runner | Freios novos |
| :- | :- | :- | :- | :- |
| 0 | Interativo com skills e fila de issues bem escrita | você | sua máquina | o harness das notas anteriores |
| 1 | "Tudo no GitHub": label `ready-for-agent` dispara `claude-code-action` com uma skill | label | runner do GitHub | write access, `concurrency` por issue, `--max-turns`, timeout, merge humano |
| 2 | Máquina de estados por label e revisão automática | label, review, CI vermelho | runner do GitHub | labels de em andamento, bloqueado e aguardando verificação; revisor com contexto limpo; teto de três rodadas; contagem de bloqueadores |
| 3 | Executor na VPS | label ou cron | runner self-hosted efêmero, ou cron com `claude -p` em container, ou o planner paralelo do Sandcastle | container novo por run, token mínimo, sem segredo no ambiente, log por run, aviso de fim |
| 4 | Alertas e relógio | `/fire` com Sentry ou PostHog, cron diário | nuvem da Anthropic ou VPS | guardas antes de chamar modelo, teto de eventos por hora, payload não confiável, custo por issue no OpenTelemetry |
| 5 | Orquestrador próprio com contrato e medição | qualquer | qualquer | schema de resultado, token de uso único, veredito amarrado ao SHA, medição pós-deploy, scorers, fábrica como código |

Notas sobre a escada:

- O degrau 1 é o que a doc oficial já sustenta, com uma inferência pequena: a doc descreve o modo de automação com `prompt` em qualquer evento, inclusive `issues: labeled`, e aceita uma skill como prompt, mas não traz o exemplo exato com a label `ready-for-agent`.
- O degrau 2 resolve as duas lacunas que o próprio repositório do Matt registra (ticket bloqueado com cara de pronto e falta de estado terminal).
- O degrau 3 não precisa vir antes do 4: routines com `/fire` rodam na nuvem da Anthropic sem VPS nenhuma. A VPS só é necessária para runs longas, acesso a serviço interno ou custo por hora. Self-hosted environments, a forma oficial de usar a própria máquina como executor de routines, são Team e Enterprise em beta ([self-hosted-environments](https://code.claude.com/docs/en/self-hosted-environments)). O runner self-hosted do GitHub Actions é recurso do GitHub e não foi conferido nesta pesquisa.
- O degrau 5 é o caso da TLC e da Warp, e as próprias fontes dizem que ele é exagero para tarefa pequena. Só se paga onde o erro custa caro e ninguém está olhando.

## 10. Onde as fontes concordam e divergem

**Concordam:**

- O ticket no centro, com o tracker como system of record e todo sinal entrando pela triagem.
- Quem faz não avalia: revisor em outra run, outro modelo ou outra conta; QA sem permissão de editar.
- Teto de rodadas e de tentativas, depois humano.
- Merge humano no fim, escalado por risco.
- Texto de issue, PR e alerta é dado, nunca instrução.
- Começar pequeno e endurecer só o trecho que precisa.

**Divergem:**

- **Confiabilidade por determinismo ou por medição.** A TLC fecha o agente num contrato validado por código; a Warp deixa o agente mais solto e corrige a fábrica medindo runs e benchmarks. O Matt fica no meio: freios simples e uma retro periódica.
- **Orquestração.** Warp e TLC montam vários agentes especializados; o Akita mostra por benchmark que um modelo forte sozinho num harness maduro ganha, e a Anthropic diz que código raramente paga o multiagente.
- **Quanto automatizar o merge.** A Anthropic dispensa humano em mudança de baixo risco; a TLC deixa auto-merge desligado salvo mudança reversível; o action oficial nem abre o PR.
- **Nomes.** O Akita chama loop e harness engineering de taxonomia vendida como curso, mas o próprio repositório dele tem uma skill pequena de loop com critério de sucesso tipado e teto de tentativas. A divergência é mais sobre o rótulo que sobre a prática.

## 11. Perguntas abertas

Sem decisão aqui.

**Escopo**

1. A fábrica vira skill, script, ou só um ADR com o desenho? A skill do Matt é só de desenho e o loop dele mora numa biblioteca, como já discutido em [harness 9.1](harness-de-agentes.md#91-matt-pocock-o-loop-não-é-skill).
2. Qual o primeiro gatilho a ligar, e em qual repositório? Pela regra do repo, só depois de rodar a tarefa a mão algumas vezes e registrar onde dói.

**Fila e estado**

3. Adotar as labels `agent:*` do Sandcastle ou estender o vocabulário de triagem atual (`ready-for-agent`, `ready-for-human`) com em andamento, bloqueado e aguardando verificação?
4. Quem impede duas runs na mesma issue: `concurrency` do Actions, lock na VPS, ou os dois?

**Runner e custo**

5. Degrau 1 no runner do GitHub primeiro, ou direto para a VPS? O que justifica a VPS além de runs longas?
6. Assinatura ou API key com teto de workspace? Em que volume trocar, e como medir antes de saber o limite real da assinatura?
7. O que fazer se a mudança de cobrança pausada voltar?

**Revisão**

8. A revisão automática usa a `code-review` instalada (padrões e spec contra a issue), a the-judge, ou as duas? Como o veredito vira status obrigatório, se nenhuma ferramenta bloqueia sozinha?
9. Num repo de autor único, o GitHub não deixa o mesmo usuário aprovar o próprio PR: o agente precisa de identidade própria para a revisão contar?

**Segurança**

10. Que token cada tarefa recebe? Triagem só lê; implementação escreve em branch; ninguém além do humano faz merge?
11. Alertas entram na mesma fila que issues, ou numa fila separada com menos permissões?

**Melhoria**

12. A retro a cada N PRs propõe mudança nas skills da fábrica; isso passa pelo fluxo de eval contra baseline deste repositório, como qualquer mudança de skill?

## 12. Fontes

Todas acessadas em 2026-11-06.

Doc oficial da Anthropic:

- Claude Code GitHub Actions: https://code.claude.com/docs/en/github-actions
- Segurança do claude-code-action: https://github.com/anthropics/claude-code-action/blob/main/docs/security.md
- Code Review: https://code.claude.com/docs/en/code-review
- Custos do Code Review: https://code.claude.com/docs/en/code-review-costs
- Claude Code na web e auto-fix de PR: https://code.claude.com/docs/en/claude-code-on-the-web
- Routines (scheduled tasks): https://code.claude.com/docs/en/routines
- Self-hosted environments: https://code.claude.com/docs/en/self-hosted-environments
- Agent teams: https://code.claude.com/docs/en/agent-teams
- Custos e redução de tokens: https://code.claude.com/docs/en/costs
- Monitoramento com OpenTelemetry: https://code.claude.com/docs/en/monitoring-usage
- Legal e compliance: https://code.claude.com/docs/en/legal-and-compliance
- GitLab CI/CD: https://code.claude.com/docs/en/gitlab-ci-cd
- Preços de API: https://platform.claude.com/docs/en/about-claude/pricing
- Crédito de API para assinantes: https://platform.claude.com/docs/en/about-claude/api-credits-for-subscribers
- Managed Agents: https://platform.claude.com/docs/en/managed-agents/overview
- Planos: https://claude.com/pricing
- Agent SDK com o plano (status da mudança de cobrança): https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan

Artigos de engenharia da Anthropic:

- Solving code review at Anthropic (2026-10-15): https://claude.dev
- How we built our multi-agent research system: https://www.anthropic.com/engineering/multi-agent-research-system

Matt Pocock:

- Repositório de skills: https://github.com/mattpocock/skills
- Skill software-factory: https://github.com/mattpocock/skills/tree/main/skills/in-progress/software-factory
- PR #1387 (despacho para a fábrica): https://github.com/mattpocock/skills/pull/1387
- Sandcastle: https://github.com/mattpocock/sandcastle
- Docs do Sandcastle: https://www.aihero.dev/sandcastle
- AI Coding Dictionary: https://www.aihero.dev/ai-coding-dictionary/software-factory , https://www.aihero.dev/ai-coding-dictionary/dark-factory , https://www.aihero.dev/ai-coding-dictionary/afk
- Getting Started With Ralph: https://www.aihero.dev/getting-started-with-ralph
- Vídeo da fábrica AFK (2026-04-30): https://www.youtube.com/watch?v=E5-QK3CDVQM
- Cohort Software Factories for Real Engineers: https://www.aihero.dev/cohorts/software-factories-for-real-engineers

Fábio Akita:

- Hot take sobre harness, loop e graph engineering: https://akitaonrails.com/2026/08/18/hot-take-harness-loop-engineering-graph-engineering-sao-bullshit/
- Parem de inventar desculpas e façam mais deploy: https://akitaonrails.com/2026/09/22/parem-de-inventar-desculpas-e-facam-mais-deploy-a-premissa-mudou/
- Falando um pouco sobre minhas skills de IA: https://akitaonrails.com/2026/09/17/falando-um-pouco-sobre-minhas-skills-de-ia/
- LLMs + agentes = competente o suficiente: https://akitaonrails.com/2026/10/12/llms-agentes-competente-o-suficiente/
- Como me precaver pros meus agentes não apagarem minhas coisas: https://akitaonrails.com/2026/07/11/como-me-precaver-pros-meus-agentes-nao-apagarem-minhas-coisas/
- Vale a pena misturar 2 modelos: https://akitaonrails.com/2026/04/25/llm-benchmarks-vale-a-pena-misturar-2-modelos/
- Dicas e toolkit de IA: https://akitaonrails.com/2026/05/24/dicas-e-toolkit-de-ia-do-akita-ai-jail-ai-memory-ai-usagebar/
- LLM Benchmark v4 (self-host x assinatura): https://akitaonrails.com/2026/10/22/llm-benchmark-v4-can-my-team-fit-in-a-4x-b300-h200/
- my-skills: https://github.com/akitaonrails/my-skills
- ai-jail: https://github.com/akitaonrails/ai-jail
- ai-memory: https://github.com/akitaonrails/ai-memory

Revisão, memória e produtos:

- the-judge (Tech Leads Club, CC-BY-4.0): https://github.com/tech-leads-club/agent-skills
- Warp Factories: https://www.warp.dev/factories
- The Factory Stack (Warp): https://www.warp.dev/blog/the-factory-stack
- Unblocked: https://getunblocked.com
- Cognee: https://www.cognee.ai e https://github.com/topoteretes/cognee
- Hermes Agent: https://github.com/NousResearch/hermes-agent

Vídeos:

- Tech Leads Club, Como Construir uma Fábrica de Software Agêntica na Prática (2026-11-04): https://www.youtube.com/watch?v=5UwvjCVPigM
- Warp, What it takes to build a software factory (2026-10-19): https://www.youtube.com/watch?v=x-PK3yx_MJg

Anedóticas (comparativos e estimativas de terceiros, citadas só como relato):

- Custo por PR do Code Review: https://blog.codacy.com/ai-code-review-cost-per-pull-request-what-engineering-teams-actually-pay-in-2026
- Comparativo de background agents: https://techsy.io/en/blog/background-coding-agents-compared
- Cobertura da mudança de cobrança de junho: https://startdebugging.net/2026/06/claude-agent-sdk-separate-credit-pool-june-15/
