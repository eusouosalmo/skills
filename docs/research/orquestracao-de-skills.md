# Orquestração de skills: pipeline com portões humanos e artefatos em arquivo

Resumo: nenhuma fonte oficial define um mecanismo de uma skill chamar outra, nem de declarar dependência entre skills. O que existe é o modelo invocando outra skill pelo nome (a Skill tool, no Claude Code), workflows com checklist e loops de validação dentro de uma skill, arquivos intermediários como estado verificável, e o aviso de que agentes podem parar para feedback humano em checkpoints. Para o pipeline do reel (cutting-raw-takes, animating-reel-scenes, finishing-reels), três fatos oficiais pesam mais: as sub-skills perguntam ao autor e o `AskUserQuestion` não existe em subagent, então tudo roda na conversa principal; depois de uma compactação o Claude Code guarda só o começo de cada skill invocada, num orçamento comum, então o estado precisa estar em arquivo; e nada instala as sub-skills junto com a orquestradora, então a orquestradora precisa conferir que elas existem. O resto (arquivo de estado, ledger, retomar de onde parou, não pedir aprovação duas vezes) é prática de comunidade.

Pesquisa feita em 2026-10-17, para o desenho da skill que recebe os brutos e o roteiro e entrega o reel pronto. Complementa [escrita-de-skills.md](escrita-de-skills.md) (seções 4.8, 4.9, 5.2, 5.6, 5.7 e 5.8 já cobrem checklist, plan-validate-execute, `disable-model-invocation`, ciclo de vida da skill no contexto, `context: fork` e a forma de chamar outra skill) e [harness-de-agentes.md](harness-de-agentes.md) (seções 6.3, 9.2, 10.4 e 10.10 já cobrem lista de status, o fluxo pesquisa, plano e implementação da HumanLayer, humanos sobre o loop e estado compartilhado). Aqui esses pontos aparecem só por referência.

## Sumário

1. [Fontes e método](#1-fontes-e-método)
2. [Uma skill invocar outra](#2-uma-skill-invocar-outra)
3. [Declarar dependências entre skills](#3-declarar-dependências-entre-skills)
4. [Quando a skill chamada não está instalada](#4-quando-a-skill-chamada-não-está-instalada)
5. [Workflow, checklist e loop de validação](#5-workflow-checklist-e-loop-de-validação)
6. [Portões de aprovação humana](#6-portões-de-aprovação-humana)
7. [Contexto numa sessão longa](#7-contexto-numa-sessão-longa)
8. [Estado entre etapas por arquivos](#8-estado-entre-etapas-por-arquivos)
9. [Padrões da comunidade](#9-padrões-da-comunidade)
10. [Onde as fontes concordam e divergem](#10-onde-as-fontes-concordam-e-divergem)
11. [O que isso sugere para a skill orquestradora](#11-o-que-isso-sugere-para-a-skill-orquestradora)
12. [Perguntas abertas](#12-perguntas-abertas)
13. [Fontes](#13-fontes)

## 1. Fontes e método

| Sigla | Fonte | Tipo |
| - | - | - |
| SPEC | [Agent Skills specification](https://agentskills.io/specification) | especificação aberta |
| AS | Guias de agentskills.io: [best practices](https://agentskills.io/skill-creation/best-practices) e [adding skills support](https://agentskills.io/client-implementation/adding-skills-support) | doc oficial do padrão |
| BP | [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) e [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) | doc oficial Anthropic |
| CC | [Extend Claude with skills](https://code.claude.com/docs/en/skills), [Create custom subagents](https://code.claude.com/docs/en/sub-agents), [Dynamic workflows](https://code.claude.com/docs/en/workflows), [Plugins reference](https://code.claude.com/docs/en/plugins-reference) | doc oficial Claude Code |
| VL | [README do vercel-labs/skills](https://github.com/vercel-labs/skills) | doc oficial do instalador |
| BEA | [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) (Erik Schluntz e Barry Zhang, 19 de dezembro de 2024) | blog de engenharia Anthropic |
| ENG | [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) (Barry Zhang, Keith Lazuka e Mahesh Murag, 16 de outubro de 2025) | blog de engenharia Anthropic |
| SP | [obra/superpowers](https://github.com/obra/superpowers): `brainstorming`, `writing-plans`, `executing-plans`, `using-superpowers` | comunidade |
| MP | [mattpocock/skills](https://github.com/mattpocock/skills): `implement`, `implement-spec`, `handoff`, `claude-handoff`, `.agents/invocation.md` | comunidade |
| PK | [pskoett/pskoett-ai-skills](https://github.com/pskoett/pskoett-ai-skills), skill `skill-pipeline` e `references/handoff-matrix.md` | comunidade |
| MS | [How to Build a Skill System in Claude Code](https://mindstudio.ai/blog/claude-code-skill-system-chaining-pipelines) (MindStudio, 16 de junho de 2026) | comunidade (blog de empresa) |

Os documentos de SPEC, AS, BP, CC e VL foram baixados em Markdown em 2026-10-17 e lidos por busca nos trechos relevantes. As skills de SP, MP e PK foram lidas pelo `gh api`. Os níveis de confiança seguem os das outras notas:

- **confirmado:** está em doc oficial (SPEC, AS, BP, CC, VL).
- **convenção:** vários autores independentes fazem igual.
- **relato:** um autor afirma. Posts de engenharia (BEA, ENG) contam como relato quando descrevem experimento, e como confirmado quando descrevem o produto.

## 2. Uma skill invocar outra

### 2.1 Não há mecanismo próprio; o modelo invoca pelo nome

- **O que é:** a SPEC não tem campo nem sintaxe para uma skill chamar outra. O corpo do SKILL.md não tem "format restrictions". O que torna a chamada possível é o cliente: no Claude Code, o modelo carrega skills pela Skill tool, e "Claude can invoke any skill that doesn't have `disable-model-invocation: true` set" (CC, Restrict Claude's skill access). Uma instrução no corpo da orquestradora ("use a skill `cutting-raw-takes`") é só texto que leva o modelo a fazer essa chamada.
- **O que as fontes oficiais dizem sobre compor:** a BP lista como benefício "Combine Skills for complex, multistep tasks" (overview), sem dizer como. O ENG chama skills de "composable resources" e não trata de uma skill invocando outra. A AS compara o escopo de uma skill ao de uma função, "a coherent unit of work that composes well with other skills", e avisa que skills estreitas demais "force multiple skills to load for a single task, risking overhead and conflicting instructions".
- **Confiança:** confirmado que não existe mecanismo na SPEC e que a chamada é do modelo; a forma exata da frase que chama (nome da tool, uma chamada por skill) está em [escrita-de-skills.md, 5.8](escrita-de-skills.md#58-como-uma-skill-chama-outra) e é convenção.

### 2.2 A orquestradora pode ser só do usuário; as chamadas, não

- **O que é:** uma skill com `disable-model-invocation: true` não pode ser invocada pelo modelo, e "If Claude tries anyway, Claude Code blocks the call and instructs it not to reproduce the deploy steps another way" (CC). Portanto a orquestradora pode ser user-invoked, mas as três sub-skills precisam continuar model-invoked para ela alcançá-las. O MP formaliza isso: "A user-invoked skill may invoke model-invoked skills, but it can never reach another user-invoked skill" (invocation.md), e o `implement` dele é exatamente uma orquestradora user-invoked que chama `tdd` e `code-review`.
- **Estado no repositório:** as três sub-skills não declaram `disable-model-invocation`, então podem ser chamadas.
- **Confiança:** confirmado (CC); o exemplo é relato (MP). Detalhe da troca de custo em [escrita-de-skills.md, 5.2](escrita-de-skills.md#52-disable-model-invocation-true).

### 2.3 Invocar de novo não duplica

- **O que é:** se o modelo invoca uma skill cujo conteúdo renderizado é igual ao que já está no contexto, o Claude Code põe só um aviso de que ela já está carregada; se mudou (outros argumentos, contexto dinâmico), anexa o conteúdo inteiro de novo (CC, Skill content lifecycle). A AS recomenda o mesmo a quem implementa um cliente ("Deduplicate activations").
- **Por que importa:** a orquestradora pode mandar reinvocar uma sub-skill ao voltar a ela (ver 7.1) sem custo extra quando nada mudou.
- **Confiança:** confirmado.

## 3. Declarar dependências entre skills

### 3.1 A SPEC não tem campo de dependência

- **O que é:** os campos da SPEC são `name`, `description`, `license`, `compatibility`, `metadata` e `allowed-tools`. Nenhum lista outras skills. O `compatibility` é texto livre de até 500 caracteres para "environment requirements (intended product, system packages, network access, etc.)", e a própria SPEC diz que a maioria das skills não precisa dele. Em `scripts/`, pede que o código seja "self-contained or clearly document dependencies".
- **Leitura:** citar as skills necessárias no `compatibility` ("Needs the cutting-raw-takes, animating-reel-scenes and finishing-reels skills installed") cabe no texto livre, mas nenhum exemplo oficial usa o campo assim e nenhum cliente o lê como dependência. É inferência desta nota.
- **Confiança:** confirmado quanto à ausência; o uso do `compatibility` para isso é inferência.

### 3.2 O instalador não resolve dependências

- **O que é:** o `npx skills add` instala o que for pedido, por `--skill <nome>`, `--skill '*'` ou `--all`; o README não menciona dependência entre skills. Skills com `metadata.internal: true` ficam ocultas, "shown and installed" só com `INSTALL_INTERNAL_SKILLS=1` (VL, Environment Variables).
- **Consequência:** quem instalar só a orquestradora fica sem as sub-skills. E enquanto `finishing-reels` for `draft` (com `internal: true`), um `npx skills add eusouosalmo/skills --all` comum não a instala.
- **Confiança:** confirmado.

### 3.3 Plugin do Claude Code: dependência entre plugins, não entre skills

- **O que é:** o `plugin.json` tem `dependencies`, "Plugins that must be enabled for this one to work" (CC, Plugins reference). Não há equivalente por skill. Dentro de um mesmo plugin, todas as skills listadas são instaladas juntas.
- **Consequência para este repositório:** o plugin só leva skills `beta` e `stable` (ADR 0005). Hoje `cutting-raw-takes` e `animating-reel-scenes` estão lá e `finishing-reels`, `draft`, não. Uma orquestradora `beta` no plugin chamaria uma sub-skill ausente do plugin.
- **Confiança:** confirmado (CC); o estado do plugin vem do `.claude-plugin/plugin.json` em 2026-10-17.

### 3.4 O princípio vizinho: não supor o que está instalado

- **O que é:** a BP tem uma seção "Avoid assuming tools are installed": não escrever "use a biblioteca de pdf", e sim dizer como instalar antes de usar. O texto fala de pacotes, não de skills, mas é a regra oficial mais próxima.
- **Confiança:** confirmado para pacotes; a extensão para skills é analogia.

## 4. Quando a skill chamada não está instalada

- **O que as fontes oficiais dizem:** pouco, e de forma indireta.
  - A AS manda o cliente restringir o nome na ferramenta de ativação ao conjunto de skills válidas, "as an enum in the tool schema", porque isso "prevents the model from hallucinating nonexistent skill names". Ou seja, num cliente bem feito a chamada a uma skill ausente nem é possível.
  - O CC registra um caso: uma rotina que invoca uma skill que só existe em `~/.claude/skills/` de outra máquina recebe que a skill "was not found".
  - O CC diz que a lista de skills "always contains every skill name", mas que, se o orçamento estoura, descrições são cortadas a partir das menos usadas. Uma sub-skill instalada continua com o nome visível mesmo sem descrição.
- **O que nenhuma fonte diz:** o que o modelo faz depois. O risco óbvio é improvisar a etapa sem a skill. O único bloqueio documentado contra improviso é o de `disable-model-invocation` (2.2), que vale para skill bloqueada, não ausente.
- **Prática possível:** conferir no início, antes de qualquer trabalho, que as três skills aparecem entre as disponíveis, e parar com a instrução de instalação se faltar alguma. Nenhuma fonte oficial descreve isso; o PK faz algo parecido para ferramentas ("A missing history source or no useful matches must not block implementation"), mas no sentido oposto, de seguir sem a peça.
- **Confiança:** confirmado para os três fatos acima; o comportamento depois da falha é lacuna.

## 5. Workflow, checklist e loop de validação

A base já está em [escrita-de-skills.md, 4.8 e 4.9](escrita-de-skills.md#48-critérios-de-conclusão). O que importa a mais para um pipeline:

- **Checklist copiável:** a BP manda, em workflows complexos, dar "a checklist that Claude can copy into its response and check off as it progresses", e diz que passos claros "prevent Claude from skipping critical validation". A AS diz que o checklist ajuda "especially when steps have dependencies or validation gates". Num pipeline, cada etapa é uma linha, e o portão entre etapas vira um item. Confirmado.
- **Loop de validação:** "Run validator, fix errors, repeat" (BP); o validador pode ser um script, um checklist de referência ou uma autoavaliação (AS), e o passo seguinte só começa "when validation passes". Entre etapas do reel, o validador natural é conferir que os artefatos que a próxima skill espera existem e estão coerentes. Confirmado.
- **Workflow condicional:** a BP mostra um passo inicial que decide o ramo ("Creating new content? Editing existing content?"). Num pipeline que pode começar no meio (corte já feito, cenas já feitas), esse é o padrão para escolher a etapa de partida. Confirmado.
- **Workflow grande vai para arquivo:** "If workflows become large or complicated with many steps, consider pushing them into separate files" (BP). Confirmado.

## 6. Portões de aprovação humana

### 6.1 O que a Anthropic chama de gate

- **O que é:** no BEA, prompt chaining é decompor a tarefa numa sequência em que "each LLM call processes the output of the previous one", com "programmatic checks (see "gate" in the diagram below) on any intermediate steps". Serve quando a tarefa "can be easily and cleanly decomposed into fixed subtasks", trocando latência por acerto. Um dos exemplos é escrever um roteiro de documento, conferir se ele atende a critérios e só então escrever o documento.
- **Humano no meio:** o mesmo post diz que agentes "can pause for human feedback at checkpoints or when encountering blockers", que precisam de "ground truth" do ambiente a cada passo, e pede transparência: "explicitly showing the agent's planning steps". Recomenda também condições de parada, como número máximo de iterações, e começar simples.
- **Leitura:** no BEA, o gate é uma checagem programática; o checkpoint humano é outra coisa. Um pipeline de skills pode ter os dois: a checagem de artefatos (5) e a pergunta ao autor.
- **Confiança:** relato (post de engenharia descrevendo padrões, não produto). É a fonte mais citada para o termo.

### 6.2 Onde um portão humano pode rodar no Claude Code

- **Só na conversa principal:** o filtro que vale para todo subagent remove `AskUserQuestion`, entre outras ferramentas (CC, Available tools). Um subagent não pergunta ao usuário; só devolve um resultado. As três sub-skills usam a ferramenta de pergunta (está no `compatibility` de cada uma), então não podem rodar em subagent sem perder os portões delas.
- **Permissão não é portão:** um subagent em segundo plano mostra pedidos de permissão de ferramenta na sessão principal (CC, Run subagents in foreground or background). Isso aprova chamadas de ferramenta, não o conteúdo de uma etapa.
- **Controle de momento:** `disable-model-invocation: true` existe para "workflows with side effects or that you want to control timing" (CC). É um portão na entrada (só o humano começa), não entre etapas.
- **Confiança:** confirmado.

### 6.3 Cada sub-skill já tem seus portões

- **Estado no repositório:** `cutting-raw-takes` pergunta a forma de saída e aprova a tabela de tomadas "before anything is rendered"; `finishing-reels` pergunta a forma de saída antes de qualquer render; `animating-reel-scenes` decide com o autor quais trechos viram cena. Um portão da orquestradora entre etapas se soma a esses.
- **O que a comunidade faz com isso:**
  - O PK manda reaproveitar a aprovação já dada: depois que o usuário aprova o plano, seguir "directly into the execution stage, no separate "should I proceed?" prompt", e só perguntar se surgir decisão material nova. Relato.
  - O SP, em `executing-plans`, proíbe pausas de "posso continuar?" entre tarefas e lista quatro únicas paradas (operação destrutiva, ação sensível de segurança, efeito fora do worktree como push ou publicação, plano quebrado). Em `brainstorming`, um HARD-GATE impede construir antes da aprovação, com a ressalva "Approval covers what you showed them". Relato.
  - A HumanLayer põe a revisão humana nas fases de maior alavanca ([harness-de-agentes.md, 9.2](harness-de-agentes.md#92-outras-divisões)). Relato.
- **Convergência:** três autores independentes tratam pergunta de rotina entre etapas como custo e guardam o portão para o que é caro de desfazer ou para o que o humano ainda não viu. Convenção.

## 7. Contexto numa sessão longa

### 7.1 Várias SKILL.md na mesma sessão

- **O que é:** a skill invocada entra uma vez como mensagem e fica; o Claude Code não relê o arquivo. Na compactação, ele religa a invocação mais recente de cada skill guardando "the first 5,000 tokens of each", num orçamento conjunto de 25.000 tokens preenchido a partir da skill invocada por último, de modo que "older skills can be dropped entirely after compaction if you have invoked many in one session" (CC, Skill content lifecycle). O remédio oficial: "invoke the skill again to restore its full content", e pôr o mais importante no topo.
- **Números do pipeline (estimativa grosseira, cerca de 4 caracteres por token):** `cutting-raw-takes` tem 9,2 mil caracteres (uns 2,3 mil tokens), `animating-reel-scenes` 32,8 mil (uns 8 mil) e `finishing-reels` 13,5 mil (uns 3,4 mil). A `animating-reel-scenes` passa dos 5 mil e volta cortada depois de uma compactação. Somadas à orquestradora, cabem nos 25 mil, mas a sessão de um reel inteiro (transcrição, renders, revisões) tem boa chance de compactar no meio.
- **Confiança:** confirmado (regras do CC); os tamanhos foram medidos em 2026-10-17.

### 7.2 context: fork e subagentes não servem às sub-skills

- **context: fork:** roda a skill num subagent que "doesn't see your conversation history" (CC). Além do que já está em [escrita-de-skills.md, 5.7](escrita-de-skills.md#57-context-fork): o fork roda em segundo plano por padrão, com o conjunto menor de ferramentas dos subagents em segundo plano; suas edições ficam fora dos checkpoints do `/rewind`; e o campo só funciona no Claude Code (VL, tabela de compatibilidade: `context: fork` é "Yes" só na coluna do Claude Code).
- **Subagent com skills pré-carregadas:** o campo `skills` de um subagent injeta o conteúdo inteiro no início, mas não aceita skills com `disable-model-invocation: true` (CC). Continua sendo subagent, sem `AskUserQuestion`.
- **Quando a doc manda ficar na conversa principal:** "The task needs frequent back-and-forth or iterative refinement" e "Multiple phases share significant context" (CC, Choose between subagents and main conversation). As duas descrevem o pipeline do reel.
- **Encadear subagentes:** o CC documenta "Chain subagents", em que cada um devolve o resultado e o Claude passa o contexto relevante ao seguinte. Serve para etapas sem perguntas.
- **Confiança:** confirmado.

### 7.3 Dynamic workflows

- **O que é:** o CC compara quem guarda o plano. Em skills, quem decide o próximo passo é "Claude, following the prompt", os resultados intermediários ficam na janela de contexto e uma interrupção "Restarts the turn"; num workflow, um script decide, os resultados ficam em variáveis do script e a execução é retomável na mesma sessão (CC, Dynamic workflows).
- **Por que não encaixa aqui:** o workflow orquestra subagents (sem `AskUserQuestion`), é recurso só do Claude Code e mira dezenas de agentes. Mas a tabela deixa explícito por que, numa skill, o estado tem de ir para arquivo.
- **Confiança:** confirmado.

## 8. Estado entre etapas por arquivos

### 8.1 O que a doc oficial sustenta

- **Saídas intermediárias verificáveis:** BP e AS recomendam o plan-validate-execute com um arquivo no meio (`fields.json`, `changes.json`) validado antes de executar. A BP lista o porquê: erros aparecem cedo, a checagem é objetiva, "Reversible planning" (iterar no plano sem tocar nos originais) e mensagens de erro apontam o problema. Confirmado.
- **O contexto não guarda o estado com segurança:** a skill não é relida e pode ser cortada na compactação (7.1); em skills, "intermediate results live" na janela de contexto (7.3). Confirmado. A conclusão de que o estado do pipeline deve morar em disco é inferência direta disso.
- **Arquivo de progresso em harness de longa duração:** já coberto em [harness-de-agentes.md, 6.3](harness-de-agentes.md#63-lista-de-features-com-status). Relato.

### 8.2 Duas formas de saber em que etapa se está

- **Estado derivado dos artefatos:** a etapa atual é deduzida do que já existe na pasta. As skills do repositório já descrevem esse contrato: `finishing-reels` espera "a reel folder with the cut, `legenda.srt`, `words.json`, `timeline.md` and `exports/`". Sem arquivo extra, mas ambíguo quando um artefato existe e não foi aprovado.
- **Arquivo de estado explícito:** um arquivo que lista as etapas concluídas. O MS sugere `pipeline_state.json` com `completed_steps` e `current_step`, gravado após cada etapa, lido no início para pular o que já foi feito, o que só é seguro com etapas idempotentes. O SP usa um ledger em Markdown (`progress.md`), com a identidade do plano na primeira linha, uma linha "complete" por tarefa, retomada na primeira tarefa sem essa linha e a regra de, depois de compactação, confiar no ledger e no `git log` mais que na própria memória. Relato em cada caso.
- **Confiança:** as duas formas são relato; a necessidade de alguma delas decorre de 7.1 e 7.3.

### 8.3 Contrato de artefatos entre etapas

- O PK mantém uma "handoff matrix": tabela de skill produtora, artefato e skill consumidora. Relato.
- O MP passa contexto por "context pointers" (caminhos para spec, tickets, notas) em vez de copiar o conteúdo, e o `handoff` dele manda não duplicar o que já está em artefatos e listar as skills que o próximo agente deve chamar. Relato.
- Convergência: os dois referenciam artefatos por caminho e declaram quem produz e quem consome. Convenção.

## 9. Padrões da comunidade

Tudo nesta seção é relato ou convenção.

| Padrão | Quem | Como |
| - | - | - |
| Cadeia por marcador | SP | "REQUIRED SUB-SKILL: Use superpowers:x" no fim de cada skill; `brainstorming` termina mandando invocar `writing-plans` "and no other skill"; `writing-plans` termina pedindo revisão do plano e a escolha do executor. Cada skill aponta a próxima; não há orquestradora central. |
| Orquestradora user-invoked | MP | `implement` e `implement-spec` são `disable-model-invocation: true` e chamam skills model-invoked com "Call the Skill tool with". |
| Maestro sem artefato próprio | PK | `skill-pipeline` classifica a tarefa, escolhe a variante e "produces no artifacts of its own", só decisões de roteamento. Mantém a regra de não pedir segunda confirmação depois de um plano aprovado. |
| Handoff para outra sessão | MP | `handoff` grava um documento fora do repositório; `claude-handoff` grava e já abre um agente em segundo plano com ele (`claude --bg`). |
| Ledger e retomada | SP | `progress.md` por plano num diretório ignorado pelo git, compartilhado entre os dois executores para trocar de executor no meio. |
| Pasta da execução e estado em JSON | MS | Pasta por execução, saídas numeradas por etapa, `pipeline_state.json`, retomar pulando etapas concluídas. |

Observações:

- O SP referencia arquivos de skills vizinhas (`../subagent-driven-development/scripts/sdd-workspace`, `../requesting-code-review/code-reviewer.md`). Funciona porque o plugin instala tudo junto, e é exatamente o que o ADR 0002 deste repositório proíbe.
- A busca também achou skills em registros de terceiros (por exemplo uma `pipeline-advance` que avança uma etapa ou um portão por vez com um comando `/pipeline-approve` separado). Não foram verificadas no repositório de origem; ficam só como indício de que o padrão "uma etapa ou um portão por chamada" circula.

## 10. Onde as fontes concordam e divergem

### Concordam

- Uma skill chama outra pelo nome, por meio do modelo; não existe import nem caminho entre skills (SPEC por omissão, CC, MP, SP, ADR 0002).
- Passos em sequência com validação antes de seguir (BEA, BP, AS).
- O estado de um trabalho longo vai para arquivo, porque o contexto se perde (CC por consequência, SP, MS, PK, harness de longa duração da Anthropic).
- Portão humano onde o erro é caro ou onde há algo novo para ver, não em toda transição (SP, PK, HumanLayer).

### Divergem

- **Centralizar ou encadear:** MP e PK têm uma skill que chama as outras; o SP espalha a cadeia, cada skill nomeando a próxima.
- **Estado explícito ou derivado:** SP e MS gravam um arquivo de progresso; PK e MP confiam nos artefatos e em ponteiros para eles.
- **Quanto parar:** o SP, no modo inline, proíbe check-ins entre tarefas; o BEA fala em pausar em checkpoints sem dizer quantos; o modo subagent do SP põe revisão a cada tarefa.

## 11. O que isso sugere para a skill orquestradora

Não são decisões, são consequências das fontes acima para o desenho.

1. **Rodar tudo na conversa principal.** As sub-skills perguntam ao autor e subagent não tem `AskUserQuestion` (6.2, 7.2). Nada de `context: fork` na orquestradora nem nas sub-skills.
2. **Chamar cada sub-skill pelo nome, uma chamada por vez**, e manter as três model-invoked. A orquestradora pode ser user-invoked (2.2).
3. **Conferir as dependências no início.** Nem o instalador nem a SPEC garantem que as três existam (3, 4). Hoje `finishing-reels` é `draft` e fica fora do plugin e do `--all` comum: a orquestradora só pode ir para `beta` no plugin junto com ela, ou precisa dizer como instalá-la.
4. **Estado em disco, na pasta do reel.** Depois de uma compactação, a `animating-reel-scenes` volta cortada e a skill mais antiga pode sumir (7.1). O que já foi feito e aprovado precisa estar escrito para retomar sem refazer, e a orquestradora deve mandar reinvocar a sub-skill da etapa corrente ao retomar.
5. **Um contrato de artefatos por etapa**, no estilo da handoff matrix: o que cada etapa entrega e o que a seguinte exige (o corte; o SRT que o autor gera no CapCut; as cenas em `exports/`). A checagem desses arquivos é o gate programático do BEA entre etapas (5, 6.1, 8.3).
6. **Não pedir aprovação duas vezes.** As sub-skills já têm portões; o da orquestradora entre etapas só se justifica onde há algo novo para o autor ver (o corte pronto antes das cenas, as cenas antes do acabamento) ou trabalho caro a seguir (6.3).
7. **Prever passos que só o autor faz.** Entre o corte e as cenas, o autor legenda no CapCut e exporta o SRT. O portão ali não é aprovação, é espera por um arquivo; o checkpoint por "blocker" do BEA (6.1).

## 12. Perguntas abertas

- O estado fica derivado dos artefatos ou num arquivo explícito na pasta do reel? Se explícito, o `timeline.md` que as skills já usam serve, ou é preciso um arquivo novo?
- Que portões da orquestradora sobram depois de contar os das sub-skills? Precisa de eval com e sem portão para ver se algum é só fricção.
- Como a orquestradora confere, de forma portátil, que as sub-skills estão instaladas? Olhar a lista de skills disponíveis no contexto é o único jeito que vale para qualquer agente, e nenhuma fonte diz o quanto o modelo acerta nisso.
- A pergunta de forma de saída aparece em `cutting-raw-takes` e em `finishing-reels`. A orquestradora pergunta uma vez e passa a resposta adiante, ou deixa cada sub-skill perguntar? Passar adiante exige que as sub-skills aceitem a escolha já feita.
- A sessão de um reel inteiro cabe numa conversa, ou o desenho deve prever um handoff para outra sessão no meio (padrão `handoff` do MP)?

## 13. Fontes

Oficiais (consultadas em 2026-10-17):

- Agent Skills specification: https://agentskills.io/specification
- Agent Skills, best practices for skill creators: https://agentskills.io/skill-creation/best-practices
- Agent Skills, how to add skills support to your agent: https://agentskills.io/client-implementation/adding-skills-support
- Skill authoring best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Agent Skills overview: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Claude Code, Extend Claude with skills: https://code.claude.com/docs/en/skills
- Claude Code, Create custom subagents: https://code.claude.com/docs/en/sub-agents
- Claude Code, Orchestrate subagents at scale with dynamic workflows: https://code.claude.com/docs/en/workflows
- Claude Code, Plugins reference: https://code.claude.com/docs/en/plugins-reference
- vercel-labs/skills README: https://github.com/vercel-labs/skills

Anthropic Engineering:

- Building effective agents (19 de dezembro de 2024): https://www.anthropic.com/engineering/building-effective-agents
- Equipping agents for the real world with Agent Skills (16 de outubro de 2025): https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

Comunidade:

- obra/superpowers: https://github.com/obra/superpowers (skills `brainstorming`, `writing-plans`, `executing-plans`, `using-superpowers`)
- mattpocock/skills: https://github.com/mattpocock/skills (skills `implement`, `implement-spec`, `handoff`, `claude-handoff`; `.agents/invocation.md`)
- pskoett/pskoett-ai-skills, `skill-pipeline`: https://github.com/pskoett/pskoett-ai-skills/tree/main/agent-plugin/skills/skill-pipeline
- MindStudio, How to Build a Skill System in Claude Code (16 de junho de 2026): https://mindstudio.ai/blog/claude-code-skill-system-chaining-pipelines

Notas relacionadas neste repositório:

- [escrita-de-skills.md](escrita-de-skills.md)
- [harness-de-agentes.md](harness-de-agentes.md)
- [docs/adr/0002-skills-reference-each-other-by-name.md](../adr/0002-skills-reference-each-other-by-name.md)
- [docs/adr/0005-versioned-claude-code-plugin.md](../adr/0005-versioned-claude-code-plugin.md)
