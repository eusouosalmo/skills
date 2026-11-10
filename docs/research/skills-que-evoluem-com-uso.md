# Skills que evoluem com o uso: eval antes ou criar cedo e endurecer

Resumo: a skill-forge deve deixar de ser eval-first estrito e passar a um meio-termo por fases, amarrado ao `metadata.status`. Um draft nasce de 1 ou 2 execuções reais (ou de um log de correções feitas à mão) de uma tarefa que se repete, com um teste de fumaça lado a lado (com e sem a skill) e um teste de disparo. Em uso, cada correção do usuário entra num log da skill e, quando pode voltar, vira cenário de regressão; a skill muda por delta, nunca por reescrita inteira. Promover a beta ou stable exige baseline completa sobre os cenários acumulados, com troca de ordem quando o juiz for um LLM e veredito humano nos casos decisivos. A manutenção consolida lições em lote e poda. Os dois gates baratos continuam: sem tarefa real, sem skill; regra mecânica vai para hook ou script.

Por que essa resposta: nenhuma fonte oficial exige três evals escritos antes do primeiro rascunho; os critérios de avaliação em boa parte só aparecem depois de ver saídas; três cenários não têm poder estatístico para provar nada; e, no próprio repo, nenhuma das 45 mudanças de comportamento depois da criação veio de um eval que achou algo novo. Ao mesmo tempo, skill escrita sem contato com execução real não ajuda (SkillsBench), iterar sem sinal externo degrada (Huang et al.), e a OpenAI e a Anthropic alertam contra adiar evals até depois de publicar. Daí o meio-termo: pouco eval na entrada, eval que cresce com o uso, eval completo no portão de promoção.

Pesquisa feita em 2026-11-10. Complementa [escrita-de-skills.md](escrita-de-skills.md), que cobre formato e redação, e responde a uma pergunta que aquela nota deixou de lado: em que momento do ciclo de vida o eval entra.

## Sumário

1. [A pergunta](#1-a-pergunta)
2. [Método e níveis de confiança](#2-método-e-níveis-de-confiança)
3. [Evidência acadêmica](#3-evidência-acadêmica)
4. [Empresas e praticantes](#4-empresas-e-praticantes)
5. [Comunidade](#5-comunidade)
6. [Dados medidos do próprio repo](#6-dados-medidos-do-próprio-repo)
7. [Onde as fontes divergem](#7-onde-as-fontes-divergem)
8. [O desenho que sai disso](#8-o-desenho-que-sai-disso)
9. [Métricas de uso](#9-métricas-de-uso)
10. [Limitações e perguntas abertas](#10-limitações-e-perguntas-abertas)
11. [Fontes](#11-fontes)

## 1. A pergunta

Hoje a skill-forge segue seis passos na ordem: achar a falha observada, escrever três cenários de eval, rodar a baseline, escrever o SKILL.md mínimo, rodar com a skill e comparar, iterar até todo `human_feedback` ficar vazio. O AGENTS.md do repo apoia esse caminho citando a seção "Build evaluations first" da best practices da Anthropic.

A alternativa é criar a skill cedo, usar, e endurecer com as correções que o uso traz. A pergunta é qual dos dois o conjunto das fontes sustenta, e com quais travas.

## 2. Método e níveis de confiança

Três frentes, cada uma com sua legenda, unificadas aqui assim:

- **confirmado:** abri a fonte original (abstract ou corpo do paper, página oficial, arquivo do repositório) e li o trecho citado.
- **parcial:** li o abstract ou parte da página, mas um detalhe citado veio de resumo de terceiro ou de trecho não lido.
- **não verificado:** só vi a fonte citada por outra, ou só o snippet de busca.

Para trabalhos acadêmicos, outra distinção pesa tanto quanto essa: **preprint** (arXiv, sem revisão por pares) ou **revisado por pares** (conferência ou periódico). Quase todo o material de 2026 sobre SKILL.md é preprint. Os trabalhos de 2023 a 2025 sobre reflexão, memória de agente, otimização de prompt e LLM como juiz são, na maioria, de conferências (NeurIPS, ICLR, AAAI, EMNLP, ACL), e os estudos de TDD saíram na IEEE TSE.

Para empresas e comunidade, o critério é outro: a fonte traz dado próprio (experimento com número) ou é guia e opinião? A maioria é guia. Os poucos números medidos vêm da Vercel, da LangChain, da Deephaven e dos benchmarks acadêmicos.

Os dados do repo saem do `git log` (114 commits, de 2026-10-01 a 2026-11-06), dos `evals/evals.json` de cada skill e dos workspaces de eval locais (fora do git). Na seção 6, fato medido e inferência ficam separados.

## 3. Evidência acadêmica

### 3.1 Skill escrita sem execução não ajuda

**SkillsBench** (Li et al., arXiv 2602.12670, preprint, confirmado) mediu 84 a 86 tarefas de CLI em 11 domínios, 7 combinações de agente e modelo, 7.308 trajetórias, em três condições: sem skill, skill curada por humano e skill gerada pelo modelo. Sem skill, 24,3% de acerto; com skill curada, 40,6% (+16,2 pp, variando de +4,5 pp em engenharia de software a +51,9 pp em saúde). A skill autogerada ficou em -1,3 pp na média.

O detalhe que importa para esta decisão: a skill autogerada foi escrita antes de resolver a tarefa, sem rodar nada e sem feedback. Os autores apontam procedimentos vagos e a ausência das particularidades que o verificador exige. Ou seja, o resultado condena escrever a skill no vazio, não criar cedo a partir de execução real.

Outros números do mesmo trabalho que voltam mais adiante: 16 das 84 tarefas pioraram com a skill curada (pior caso, -39,3 pp); skills detalhadas e compactas ganharam bem (+18,8 e +17,1 pp), skills abrangentes perderam (-2,9 pp); de 2 a 3 skills por tarefa rendeu +18,6 pp, 4 ou mais só +5,9 pp. O paper tem pequenas inconsistências internas (84 ou 86 tarefas; uma legenda com +12,66 pp). Esses números são da v1 (2026-02-13). A v4 (2026-06-14, 87 tarefas, 18 configurações) dá skill curada de 33,9% para 50,5% (+16,6 pp); por número de skills, 1 rende +18,0 pp, 2 a 3 rendem +19,0 pp e 4 ou mais +10,1 pp; por tamanho, a abrangente fica em +0,7 pp, com só 5 tarefas. A direção é a mesma e o efeito encolheu.

### 3.2 Rascunho testado mais uma rodada de uso supera a skill curada

**SkillEvolver** (Zhang et al., arXiv 2605.10500, preprint, confirmado) usa uma meta-skill que guia um agente a escrever, testar e revisar uma skill de domínio, com o sinal vindo das falhas de outro agente usando a skill. Um auditor de contexto limpo faz nove checagens de overfitting, vazamento e de skill que parece válida mas nunca é invocada. No SkillsBench (83 tarefas): sem skill 29,9%, curada por humano 43,6%, rascunho inicial já testado contra execuções 48,2%, depois de uma rodada de refinamento pelo uso 56,9%. Cerca de dois terços do ganho sobre a curada vêm do refinamento. Custo: 13 execuções e cerca de US$ 3,92 por tarefa.

Leitura: o rascunho cedo funciona porque não nasce no vazio (o agente explora a tarefa antes), e o grosso do ganho vem de uma rodada com falhas reais.

### 3.3 Iterar funciona com portão de validação

- **SkillAxe** (Gautam, Radhakrishna, Gulwani, arXiv 2606.10546, preprint, confirmado no abstract): refina skills escritas por LLM comparando a saída com e sem a skill em quatro dimensões, entre elas a precisão de disparo. +28% relativo no SkillsBench, fechando de 47% a 67% da distância para as skills humanas. A comparação com e sem a skill é o motor da melhora, mesmo sem gabarito.
- **SkillOpt** (Yang et al., arXiv 2605.23904, preprint, confirmado no abstract): uma edição na skill só é aceita se melhorar um score de validação separado; edições rejeitadas viram feedback negativo. Melhor ou empatado em 52 de 52 combinações de benchmark, modelo e harness, incluindo o Claude Code.
- **EvoSkill** (Alzubi et al., arXiv 2603.02766, preprint, confirmado no abstract): cria e refina skills a partir de falhas de execução e só mantém as que melhoram uma validação separada. OfficeQA de 60,6% para 67,9%, SealQA de 26,6% para 38,7%.

Os três apoiam o mesmo desenho: a skill muda com o uso, mas cada mudança passa por uma checagem de regressão.

### 3.4 Consolidar em lote, editar por delta, podar

- **Trace2Skill** (Ni et al., arXiv 2603.25158, preprint, confirmado no abstract): destila lições de muitas trajetórias juntas num diretório de skill, partindo de uma skill humana ou de um rascunho fraco, e supera a edição sequencial, caso a caso. Um rascunho fraco é ponto de partida válido se as lições forem consolidadas de várias execuções, não de uma por vez.
- **ACE, Agentic Context Engineering** (Zhang et al., arXiv 2510.04618, ICLR 2026, revisado por pares, confirmado no corpo): playbooks que evoluem por geração, reflexão e curadoria, com atualizações incrementais. Documenta o colapso de contexto: no AppWorld, um contexto de 18.282 tokens com 66,7% de acerto foi reescrito numa versão de 122 tokens e caiu para 57,1%, abaixo da baseline sem adaptação (63,7%). Os autores declaram que, sem feedback confiável, o método pode degradar.
- **From Registry to Repository** (Gao et al., arXiv 2607.00911, preprint, confirmado por resumo): em cerca de 41 mil skills, 53% das reutilizadas nunca mudam depois de adotadas e 60,8% das escritas localmente mudam; as adições superam as remoções em 6,1 para 1. Na prática, a skill cresce por acréscimo, o mesmo inchaço que o SkillsBench penaliza.

Disso saem duas regras: mudar por delta localizado, nunca reescrever a skill inteira de uma vez; e ter um passo explícito de poda, porque o uso sozinho só acrescenta.

### 3.5 Sinal externo é obrigatório

- **Reflexion** (Shinn et al., NeurIPS 2023, revisado por pares, confirmado): reflexão verbal sobre feedback externo levou a 91% pass@1 no HumanEval contra 80% do GPT-4.
- **Large Language Models Cannot Self-Correct Reasoning Yet** (Huang et al., ICLR 2024, revisado por pares, confirmado): sem feedback externo, o modelo não autocorrige o raciocínio e às vezes piora.

Juntos: iterar pelo uso só melhora a skill se o uso produzir sinal registrado (um teste, um verificador, uma correção do usuário anotada). Impressão vaga de que "ficou melhor" não conta.

### 3.6 Induzir rotinas do uso funciona

Trabalhos anteriores ao formato SKILL.md mostram o mesmo padrão: **Voyager** (Wang et al., 2023, preprint, parcial) monta uma biblioteca de habilidades com feedback do ambiente e autoverificação; **ExpeL** (Zhao et al., AAAI 2024, confirmado) melhora conforme acumula experiência; **Agent Workflow Memory** (Wang et al., 2024, confirmado no abstract) induz rotinas durante o uso, com +24,6% relativo no Mind2Web e +51,1% no WebArena, e a versão online generaliza melhor; **AutoManual** (Chen et al., NeurIPS 2024, confirmado no abstract) parte de uma única demonstração e chega a 97,4% no ALFWorld; **SkillWeaver** (Zheng et al., 2025, preprint, confirmado no abstract) pratica as skills antes de consolidá-las; **Dynamic Cheatsheet** (Suzgun et al., 2025, preprint, confirmado no abstract) evolui uma memória em tempo de teste, sem rótulo.

### 3.7 Os critérios nascem de ver saídas

**Who Validates the Validators?** (Shankar et al., arXiv 2404.12272, apresentado na UIST 2024 segundo citações, confirmado no abstract) descreve o criteria drift: é preciso ter critérios para avaliar saídas, mas é avaliando saídas que se definem os critérios. No estudo, com 9 praticantes, 5 quiseram acrescentar critérios ao ver saídas ruins e reinterpretaram os que já tinham. É o achado mais direto contra fixar três cenários com expectativas completas antes de a skill rodar.

### 3.8 Três cenários não medem, só farejam

**Adding Error Bars to Evals** (Miller, arXiv 2411.00640, preprint, confirmado no corpo): detectar uma diferença de 3 pontos com 80% de poder pede cerca de 969 perguntas; com 198 perguntas, repetir cada uma 10 vezes baixa a menor diferença detectável de 13,2% para 7,5%; comparar par a par, pergunta por pergunta, corta cerca de um terço da variância.

Para a skill-forge: três cenários só detectam diferenças enormes (a skill acerta onde a baseline sempre erra). Servem como teste de fumaça e registro qualitativo, não como prova. Repetir um cenário 2 a 4 vezes e comparar par a par rende mais do que escrever mais cenários antes.

### 3.9 LLM como juiz tem viés de posição

- **Judging LLM-as-a-Judge** (Zheng et al., NeurIPS 2023 Datasets and Benchmarks, confirmado): o GPT-4 como juiz passa de 80% de concordância com humanos, no nível da concordância entre humanos, com vieses de posição, verbosidade e autopromoção.
- **Large Language Models are not Fair Evaluators** (Wang et al., 2023, publicado na ACL 2024 segundo citações, confirmado no abstract): trocar a ordem das respostas inverte o ranking; num teste, um modelo menor "vence" o juiz em 66 de 80 perguntas só pela posição. Correções propostas: balancear a posição e pôr humano no loop.
- **Judging the Judges** (Thakur et al., workshop GEM2 da ACL 2025, confirmado no abstract): só os juízes maiores se alinham razoavelmente com humanos, e alta porcentagem de concordância pode esconder notas bem diferentes.

Daí a regra do portão de promoção: com juiz LLM, rodar com a ordem trocada; no caso decisivo, veredito humano.

### 3.10 Em TDD, o que conta é o passo curto

- **Rafique e Mišić 2013** (IEEE TSE, revisado por pares, parcial): meta-análise de 27 estudos; efeito pequeno e positivo em qualidade, pouco ou nenhum em produtividade, com queda de produtividade maior na indústria.
- **Fucci et al. 2017** (IEEE TSE, revisado por pares, confirmado no abstract): com 82 registros de processo de 39 profissionais, testar antes ou depois não teve influência importante; qualidade e produtividade se associam a passos pequenos e ritmo constante.
- **EDDOps** (Xia et al., arXiv 2411.13768, preprint, parcial): proposta sem experimento de unir avaliação offline e online num ciclo fechado para agentes LLM.

Transposto: o valor do eval-first está em cada mudança ser pequena e checada logo, não em ter três cenários prontos antes da primeira linha. Não achei estudo que meça diretamente o custo de escrever evals antes contra iterar em uso para prompts ou skills.

### 3.11 Otimização de prompt

APE (Zhou et al., ICLR 2023), OPRO (Yang et al., ICLR 2024), MIPRO (Opsahl-Ong et al., EMNLP 2024), TextGrad (Yuksekgonul et al., 2024) e GEPA (Agrawal et al., ICLR 2026) melhoram instruções com feedback, todos confirmados no abstract. Nenhum dispensa um score. O GEPA (confirmado em parte do corpo) mostra que reflexão em linguagem natural sobre poucas execuções rende muito, que a maior parte do orçamento vai para validação, e que instruções curtas generalizam melhor que exemplos colados. O que segura o overfitting é validação separada, não escrever mais casos antes.

### 3.12 Recorrência

**Do Personalized Skills Help Coding Agents?** (Huang, Du, Lan, arXiv 2608.10319, preprint, confirmado no abstract, sem números): skills específicas da tarefa são as mais eficazes; skills de preferência pessoal só se pagam quando a preferência se repete com frequência. Sustenta exigir uma tarefa que se repete antes de criar, mesmo sem exigir eval formal.

## 4. Empresas e praticantes

### 4.1 Anthropic

- **Skill authoring best practices** (confirmado): a seção "Build evaluations first" pede evals antes de "extensive documentation" (rodar sem skill, três cenários, baseline, instruções mínimas). A seção seguinte, sobre desenvolver com Claude A e Claude B, descreve outro caminho: fazer a tarefa sem skill, notar o contexto que se repete, pedir a skill, testar em tarefas parecidas; para uma skill existente, testar com tarefas reais, não cenários, e repetir conforme o uso. A página também diz que não há forma embutida de rodar esses evals. O checklist final pede ao menos três evals e teste com uso real. Leitura: o eval-first da doc oficial mira documentação longa no escuro, não proíbe rascunho.
- **Equipping agents for the real world with Agent Skills** (Zhang, Lazuka, Murag, 2025-10-16, confirmado): começar rodando tarefas representativas para achar lacunas, construir aos poucos, e acompanhar o uso real para iterar.
- **skill-creator** (confirmado): escreve o rascunho primeiro e só depois os 2 ou 3 prompts de teste; as assertions são redigidas enquanto as execuções rodam; skills de saída subjetiva muitas vezes dispensam testes, e o usuário pode pedir para pular os evals.
- **Demystifying evals for AI agents** (Grace et al., 2026-01-09, confirmado): começar cedo e pequeno, com 20 a 50 tarefas tiradas de falhas reais; em produção, transformar falhas relatadas em casos; ler as transcrições. Também diz que evals ficam mais difíceis de montar quanto mais se espera.
- **Effective context engineering for AI agents** (2025-09-29, confirmado): começar com um prompt mínimo no melhor modelo e acrescentar instruções a partir das falhas do teste inicial.
- **Skills no Claude Code** (confirmado): medir separadamente se a skill dispara e se a saída presta, com alguns prompts realistas em sessão nova, com a skill ligada e desligada. O `/skill-doctor` aponta skills nunca invocadas e o custo de contexto.
- **Monitoring usage** (confirmado): com telemetria OpenTelemetry ligada, os eventos da ferramenta Skill e as métricas de custo e tokens trazem o nome da skill; uma skill do próprio usuário só aparece com o nome real com `OTEL_LOG_TOOL_DETAILS=1`, sem isso vira `custom_skill`. Isso torna o uso mensurável sem suíte (seção 9).

### 4.2 agentskills.io

- **Evaluating skill output quality** (confirmado): parte de uma skill já escrita e testada num prompt, recomenda começar com 2 ou 3 casos sem investir demais antes da primeira rodada, e acrescentar assertions depois de ver as saídas, porque muitas vezes não se sabe como é o bom resultado antes de rodar. É o meio-termo dito com todas as letras.
- **Optimizing skill descriptions** (confirmado): cerca de 20 queries (metade deve disparar, metade são near-misses), 3 execuções cada, divisão treino e validação. O disparo é a parte mais barata de automatizar e pode vir depois da criação.

### 4.3 OpenAI

- **Evaluation best practices** (confirmado): testes com escopo em cada etapa, registrar tudo para minerar casos de eval nos logs, avaliar a cada mudança, calibrar o juiz com humanos. Chama de antipadrão os evals por impressão e esperar até publicar para implementar qualquer eval.
- **Testing Agent Skills Systematically with Evals** (confirmado; data e autores só por espelho): definir uma lista pequena de critérios obrigatórios, escrever a skill, disparar à mão, tratar cada correção manual como candidata a eval, manter de 10 a 20 prompts e deixar as falhas reais ditarem a cobertura.
- **Build skills, Codex** (confirmado): criação imediata, inclusive gravando uma demonstração; a única checagem pedida é testar o disparo pela description.

### 4.4 Dados medidos de empresas

- **Vercel** (Gao, 2026-01-27, confirmado): baseline sem docs 53%; skill padrão também 53%; skill com instrução explícita para usá-la 79%; índice no AGENTS.md 100%. Em 56% dos casos a skill nunca foi invocada. O primeiro risco de uma skill é não disparar, e isso só aparece medindo.
- **LangChain** (Xu, 2026-03-05, confirmado): tarefas concluídas em 82% com skills contra 9% sem; numa tarefa a skill nunca foi invocada, e mandar invocá-la levou a cerca de 70%; com cerca de 20 skills parecidas o agente às vezes escolheu a errada, com 12 acertou sempre; em skills de 300 a 500 linhas, mudar formatação teve efeito limitado.
- **Deephaven** (McKenzie, 2026-05-29, confirmado): na maioria dos evals, com e sem skill passaram perto de 100%, e a skill só ajudou num conjunto pequeno; cortaram cerca de um quarto da skill sem mudança medida; um loop de melhoria totalmente automático falhou porque as recomendações só acrescentavam conteúdo; a revisão humana dos logs achou um problema de configuração.
- **Google Codelabs** (confirmado): avalia skills que já existem, com três perguntas e juiz por modelo, ampliando com o tempo. Microsoft: não achei guia oficial.

### 4.5 Praticantes

- **Hamel Husain e Shreya Shankar, AI Evals FAQ** (confirmado em cerca de dois terços da página): começar pela análise de erros, não pela infraestrutura; revisar de 20 a 50 saídas a cada mudança relevante. Dizem que eval-driven development cria mais problemas do que resolve e pedem avaliadores para erros descobertos, não imaginados, com exceção de restrições cujo sucesso já se conhece. Os próprios autores chamam as opiniões de afiadas; é relato de experiência, não estudo.
- **Hamel Husain, Your AI Product Needs Evals** (2024, confirmado): o sucesso depende da velocidade de iterar; as assertions nascem e são atualizadas a partir de falhas vistas nos dados.
- **Eugene Yan** (2025, confirmado): defende eval antes da mudança, no estilo TDD, mas só depois de olhar os dados reais. Meio-termo.
- **Simon Willison** (2025-10-16, confirmado): skills são simples e fáceis de iterar; um validador dentro da skill (um script) deixa o modelo tentar de novo.
- **Minko Gechev** (2026-02-26, confirmado): skills como código, 5 ou mais tentativas por caso, CI nos PRs que mexem em skill. Eval como regressão de skill que já existe, em escala de time.
- **Jason Liu** (não verificado, só resumos): minerar conversas por sinais de frustração e repetição.

## 5. Comunidade

### 5.1 obra/superpowers, writing-skills

O polo mais rígido (confirmado no arquivo). Aplica TDD à documentação: rodar um cenário de pressão com subagente sem a skill e registrar as racionalizações literais, escrever a skill mínima para elas, procurar nova brecha e fechar. A regra central proíbe skill sem teste que falhe antes e manda apagar a skill escrita antes do teste; a tabela de racionalizações rejeita testar só se aparecerem problemas.

Duas nuances: os testes mudam por tipo de skill, e o rigor de cenário de pressão é para skills de disciplina (as que o agente tende a pular sob pressão); e a seção de micro-testes de redação pede sempre um controle sem a orientação, 5 repetições ou mais por variante, e diz que, se o controle não exibe a falha, não há o que corrigir. Esse atalho corta trabalho em vez de acrescentar. O mesmo autor manda automatizar o que regex ou validação conseguem checar.

### 5.2 mattpocock/skills

Confirmado nos arquivos do repositório. A antiga write-a-skill foi substituída por writing-for-agents, que é de redação e não prescreve evals; o teste que ela propõe é rodar o documento para ver se muda o comportamento. O processo de Pocock é publicar cedo: a pasta `in-progress/` é pública de propósito, convida a testar e reportar o que quebra, e fica fora do plugin até a skill graduar. Uma mudança em skill existente só entra com falha observada em sessão real (o que rodou, o que a skill fez, o que se esperava); melhoria hipotética não passa. Toda skill é tratada como superfície permanente de manutenção, e o que dá para compor com skills existentes não ganha skill nova. A skill `retro` lê o log de uma sessão difícil e propõe candidatos, sem mudar nada até o usuário escolher; ela mesma admite que não poda regras antigas.

### 5.3 Ferramentas de skills que se melhoram

Claudeception, claude-reflect, continuous-learning-v2 (everything-claude-code), self-learning-skills e outras (confirmado nos READMEs) capturam correções ou soluções da sessão e gravam numa skill. Nenhuma publica medição de que a skill melhora. As que duram põem um humano no meio: o claude-reflect guarda correções numa fila e só grava depois de revisar, com roteamento para a skill que estava em uso; a continuous-learning trocou a geração de skill inteira por unidades pequenas com grau de confiança. Com o SkillsBench (autogerada sem curadoria não ajuda), o recado é capturar no uso com curadoria humana, não deixar o modelo reescrever a skill sozinho.

### 5.4 Discussões

Relato, baixa a média confiança. No Hacker News, usuários contam skills que pioraram a experiência, dizem que ler o log da conversa é a única forma de saber por que a skill erra, lembram que o custo em tokens tem que entrar na comparação (skills que melhoram mas custam de 35% a 40% mais tokens) e alertam que exigir muitos exemplos aumenta o atrito para capturar qualquer coisa. Há também ceticismo sobre a falta de validação rigorosa no discurso sobre skills. Duas issues no repositório do Claude Code pediram um loop de feedback de skills e foram fechadas por inatividade.

## 6. Dados medidos do próprio repo

### 6.1 Fato medido

| Skill | Criada | feat depois | fix depois | 1a correção | Cenários |
| - | - | - | - | - | - |
| reel-motion | 2026-10-07 | 13 | 7 | no mesmo dia, após o 1o uso real | 29 |
| reel-script | 2026-10-05 | 9 | 2 | no mesmo dia | 18 |
| reel-finish | 2026-10-17 | 7 | 2 | no mesmo dia | 13 |
| eusouosalmo-voice | 2026-10-03 | 2 | 0 | 1 dia | 5 |
| reel-cut | 2026-10-15 | 1 | 0 | 1 dia, no 1o reel real | 4 |
| skill-forge | 2026-10-02 | 1 | 0 | 4 dias | 5 |
| git-guardrails | 2026-10-02 | 0 | 0 | nenhuma | 3 |
| post-caption | 2026-10-06 | 0 | 0 | nenhuma | 3 |
| reel-edit | 2026-10-19 | 0 | 0 | nenhuma | 2 |
| setup-eusouosalmo-skills | 2026-10-19 | 1 | 0 | nenhuma | 2 |

A contagem exclui promoções de status, a renomeação de 2026-10-27 e docs, e traduz os nomes antigos para os atuais (sem isso o `git log` por pasta subconta).

- 10 skills, todas `beta`, promovidas em bloco em 2026-11-02 com a justificativa de terem sido testadas pelo autor.
- 84 cenários de eval, nenhum com `human_feedback` preenchido. Pela convenção da própria skill-forge, vazio significa saída boa, então o campo não distingue aprovado de nunca revisado.
- Nos workspaces locais: 61 iterações e 209 gradings; só a reel-script tem 25 iterações e 137 gradings. Nenhum arquivo de feedback salvo.
- Evals declarados e não rodados: os cenários 1 a 3 da reel-cut não rodaram de novo depois do commit 3c79224; os cenários da reel-script ligados à issue #57 nunca rodaram, e a regressão completa foi cortada duas vezes pelo limite de uso. Uma rodada da reel-cut custou cerca de 100 mil tokens e 16 minutos.
- Origem das 45 mudanças de comportamento, pelo corpo do commit: cerca de 12 citam um caso de uso real (um limite de renders simultâneos depois de o excesso derrubar a máquina, margens seguras vistas num reel publicado, a posição da legenda que caiu sobre um desenho, o primeiro reel real cortado); cerca de 8 vêm de lacuna de referência (reels de alto desempenho analisados no mapa #17, mais uma pesquisa em skills da comunidade); o resto não registra origem. Nenhum commit atribui uma mudança a um eval que achou algo novo. Os evals aparecem nos commits como verificação (por exemplo, baseline 4/7 contra 7/7 com a skill).
- A reel-script nasceu das correções a dois roteiros feitos à mão. O log local de correções tem 41 entradas numeradas (15 de estrutura, 12 de voz, 12 de conteúdo, 2 de legenda): as 30 primeiras antes de existir qualquer skill de conteúdo, as de 31 a 39 sobre saídas da skill, e as duas últimas deram origem à post-caption. 34 linhas do log marcam a correção como candidata a cenário ou apontam a skill que deve mudar.

### 6.2 Inferência

- As skills melhoraram pelas correções em uso real e pelas lacunas de referência. Os evals funcionaram como trava de regressão e prova para promover, não como fonte de melhoria: os cenários são transcrições de correções que já existiam.
- O volume de mudança acompanha o uso, não o número de evals. As três skills usadas em todo reel (motion, script, finish) concentram 40 das 45 mudanças; as quatro sem correção são as menos usadas ou ainda sem projeto real (a git-guardrails espera o projeto novo).
- O primeiro uso real acha, em 0 ou 1 dia, o que os três cenários não acharam.
- O custo dos evals já empurra o processo para fora do método: rodadas adiadas, regressões não feitas, feedback nunca preenchido, promoção em bloco. O fluxo real já é criar, usar, corrigir, com os evals vindo atrás.
- O ganho real dos evals aparece quando muitas regras interagem: as 25 iterações da reel-script para estabilizar 18 cenários sugerem regressões que um uso isolado não pegaria. Não está medido como bug evitado.

## 7. Onde as fontes divergem

1. **Rascunho antes ou depois dos evals.** A best practices da Anthropic põe "evaluations BEFORE" no título da seção, mas qualifica com documentação extensa e oferece, na seção seguinte, o caminho pelo uso. O skill-creator, o agentskills.io, a OpenAI e o Codex escrevem a skill primeiro. O superpowers proíbe.
2. **O contrapeso: não esperar demais.** A OpenAI chama de antipadrão esperar até publicar para ter qualquer eval; a Anthropic diz que evals ficam mais difíceis quanto mais se adia. Isso derruba a versão extrema do criar cedo (nunca medir) e sustenta o teste de fumaça já no draft e o eval completo antes de promover.
3. **Rigor por tipo de skill.** O superpowers é eval-first estrito, mas para skills de disciplina, as que o agente racionaliza para pular. Para skills de conteúdo subjetivo, o skill-creator diz que muitas vezes os testes são dispensáveis e o agentskills.io troca assertions por revisão humana. No repo, a skill-forge é de disciplina; as de reel são de conteúdo.
4. **Quem escreve a lição.** As ferramentas de autoaprendizado deixam o modelo gravar; Pocock, o claude-reflect e o SkillsBench apontam para curadoria humana.
5. **Eval escrito antes da mudança.** Eugene Yan defende escrever o eval antes da mudança; Hamel Husain diz que eval-driven development cria mais problemas do que resolve. Os dois concordam em olhar os dados reais primeiro, e é aí que a divergência se resolve: o eval vem antes da mudança, mas depois da falha vista.
6. **Se skills ajudam.** SkillsBench (+16,2 pp com skill curada) e LangChain (82% contra 9%) mostram ganho; Vercel (53% igual à baseline) e Deephaven (perto de 100% com e sem) mostram que muitas vezes não muda nada; o estudo de skills recuperadas de um acervo grande vê o ganho ir a quase zero. Por isso a comparação com baseline continua no portão de promoção.

## 8. O desenho que sai disso

| Fase | `metadata.status` | Entrada | O que roda | Saída |
| - | - | - | - | - |
| Nascer | draft (com `internal: true`) | 1 ou 2 execuções reais de uma tarefa que se repete, ou um log de correções feitas à mão | um teste de fumaça lado a lado, com e sem a skill, em contexto limpo; um teste de disparo (alguns prompts que devem disparar e near-misses) | SKILL.md mínimo, só com o que a fumaça mostrou faltar; log de correções da skill aberto |
| Usar | draft ou beta | cada correção do usuário numa sessão real | registrar a correção no log (prompt, o que fez, o que devia fazer); se pode voltar, virar cenário de regressão; mudar a skill por delta, com o fundamento da regra (passo 6 atual) | skill corrigida; cenários acumulados a partir do uso |
| Promover | beta ou stable | cenários acumulados (os de uso mais os de lacuna de referência) | baseline completa: todos os cenários com e sem a skill (ou contra a versão anterior), 2 a 4 repetições quando o resultado for incerto, ordem trocada se o juiz for LLM, veredito humano registrado nos casos decisivos | `human_feedback` preenchido (não vazio por omissão); status novo nos READMEs e no plugin |
| Manter | beta ou stable | lote de entradas no log, de várias sessões | consolidar as lições em lote; podar o que o controle mostra não fazer diferença; regressão completa depois de mudança grande | skill mais curta ou do mesmo tamanho |

Gates que continuam em todas as fases:

- **Sem tarefa real, sem skill.** O draft precisa de execução real ou de correções reais; material inventado para a ocasião segue valendo como falha imaginada. É o que sustenta o SkillsBench (autogerada no vazio, -1,3 pp) e a exigência de recorrência (Huang, Du e Lan).
- **Regra mecânica vai para hook ou script.** Já está na skill-forge e no superpowers.
- **Se o controle não falha, não escreva.** O atalho do superpowers vale para cada regra nova, em qualquer fase.

Por fase, o que cada fonte sustenta:

- Nascer de 1 ou 2 execuções: SkillEvolver (rascunho testado já supera a curada), AutoManual (uma demonstração basta com feedback do ambiente), best practices na trilha de Claude A e Claude B, skill-creator, Pocock (`in-progress/`), e o próprio repo (a reel-script nasceu de dois roteiros corrigidos à mão).
- Fumaça em vez de três cenários com assertions: Miller (três casos não medem), Shankar (criteria drift), agentskills.io (assertions depois da primeira rodada).
- Teste de disparo já no draft: Vercel e LangChain (o primeiro risco é a skill não ser invocada).
- Correção vira cenário: OpenAI (cada correção manual é candidata), Anthropic (falhas de produção viram casos), Hamel (erros descobertos), e o log de 41 correções do repo.
- Edição por delta e poda: ACE (colapso na reescrita), Gao et al. (6,1 adições por remoção), SkillsBench (skill abrangente perde), Deephaven (cortar um quarto sem perda).
- Baseline completa no portão: SkillOpt, EvoSkill e GEPA (validação separada segura o overfitting), OpenAI e Anthropic (não adiar evals para sempre), e a reel-script (25 iterações pegando regressão).
- Ordem trocada e humano no decisivo: Wang et al. e Zheng et al. (viés de posição), Thakur et al.
- Consolidar em lote: Trace2Skill.

O que muda na skill-forge em relação aos seis passos atuais: os passos 3 a 5 deixam de ser pré-requisito para escrever e passam a ser o portão de promoção; o passo 2 aceita execução real ou log de correções como entrada; o passo 6 (fundamento por regra) fica como está e vira o passo da fase de uso.

## 9. Métricas de uso

| Métrica | Como coletar | Confiança |
| - | - | - |
| Taxa de disparo e skills nunca usadas | `/skill-doctor`; telemetria OpenTelemetry com detalhes de ferramenta ligados, contando eventos da ferramenta Skill por `skill_name` | confirmado (docs do Claude Code) |
| Custo por skill (tokens e dólares) | eventos de custo e tokens da telemetria, agrupados pelo nome da skill | confirmado (docs do Claude Code) |
| Correções por sessão | sem métrica nativa; contar as entradas do log de correções da skill por sessão, ou ler as transcrições | inferência, a partir da análise de erros de Hamel Husain |
| Rejeição de edições | evento de decisão das ferramentas de edição (aceita ou rejeita), como indício de correção | confirmado como evento; uso como indício é inferência |
| Feedback vazio como parada | só vale se o feedback foi de fato pedido e registrado | confirmado (agentskills.io); o repo mostra o risco de vazio por omissão |

Uma queda na taxa de correções por sessão é o sinal de que a skill está madura para promover; uma skill que nunca dispara é candidata a corte ou a nova description antes de qualquer eval de qualidade.

## 10. Limitações e perguntas abertas

Limitações:

- Quase toda a evidência sobre SKILL.md é preprint de 2026, sem revisão por pares, e mede tarefas de CLI com verificador automático. Skills de conteúdo subjetivo, como as de reel, não têm benchmark; a transposição é inferência.
- Os números de empresas (Vercel, LangChain, Deephaven) são de um experimento cada, com tarefas próprias.
- Os dados do repo são de um autor só, em cinco semanas, com a origem de parte dos commits não registrada.
- Alguns detalhes ficaram só no abstract ou em resumo de terceiro (marcados como parcial ou não verificado).
- Não existe estudo que compare diretamente eval antes contra iterar em uso para skills.

Perguntas abertas:

- Onde fica o log de correções de cada skill: dentro da pasta da skill (vai junto na instalação e é público) ou fora (perde a ligação com a skill)? O repo é público, então o log não pode carregar conteúdo de sessões privadas.
- Quantas correções sem regressão bastam para promover de draft a beta? As fontes não dão número.
- O que fazer com as 10 skills já em beta com `human_feedback` vazio: tratá-las como promovidas sem o portão e rodar a baseline completa quando mudarem, ou rebaixar as menos usadas a draft?
- A skill-forge, sendo de disciplina, deve manter para si mesma o rigor do superpowers (cenários de pressão)?
- Como ligar a telemetria sem coletar o texto dos prompts, e se a contagem de correções por sessão pode ser feita só pelo log da skill.
- Para skills de conteúdo, qual o juiz no portão de promoção: só o autor, ou um LLM com ordem trocada e o autor nos casos em que os dois discordam?

## 11. Fontes

Acadêmicas (consultadas em 2026-11-10):

- SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks (Li et al., 2026, preprint): https://arxiv.org/abs/2602.12670
- SkillEvolver: Skill Learning as a Meta-Skill (Zhang et al., 2026, preprint): https://arxiv.org/abs/2605.10500
- SkillAxe: Sharpening LLM-Authored Agent Skills Through Evaluation-Guided Self-Refinement (Gautam, Radhakrishna, Gulwani, 2026, preprint): https://arxiv.org/abs/2606.10546
- SkillOpt: Executive Strategy for Self-Evolving Agent Skills (Yang et al., 2026, preprint): https://arxiv.org/abs/2605.23904
- EvoSkill: Automated Skill Discovery for Multi-Agent Systems (Alzubi et al., 2026, preprint): https://arxiv.org/abs/2603.02766
- Trace2Skill: Distill Trajectory-Local Lessons into Transferable Agent Skills (Ni et al., 2026, preprint): https://arxiv.org/abs/2603.25158
- How Well Do Agentic Skills Work in the Wild (Liu et al., 2026, preprint): https://arxiv.org/abs/2604.04323
- Do Personalized Skills Help Coding Agents? (Huang, Du, Lan, 2026, preprint): https://arxiv.org/abs/2608.10319
- From Registry to Repository (Gao et al., 2026, preprint): https://arxiv.org/abs/2607.00911
- Agentic Context Engineering (Zhang et al., ICLR 2026): https://arxiv.org/abs/2510.04618
- Voyager (Wang et al., 2023, preprint): https://arxiv.org/abs/2305.16291
- Reflexion (Shinn et al., NeurIPS 2023): https://arxiv.org/abs/2303.11366
- Large Language Models Cannot Self-Correct Reasoning Yet (Huang et al., ICLR 2024): https://arxiv.org/abs/2310.01798
- ExpeL (Zhao et al., AAAI 2024): https://arxiv.org/abs/2308.10144
- Agent Workflow Memory (Wang et al., 2024): https://arxiv.org/abs/2409.07429
- AutoManual (Chen et al., NeurIPS 2024): https://arxiv.org/abs/2405.16247
- SkillWeaver (Zheng et al., 2025, preprint): https://arxiv.org/abs/2504.07079
- Dynamic Cheatsheet (Suzgun et al., 2025, preprint): https://arxiv.org/abs/2504.07952
- Large Language Models Are Human-Level Prompt Engineers, APE (Zhou et al., 2022): https://arxiv.org/abs/2211.01910
- Large Language Models as Optimizers, OPRO (Yang et al., ICLR 2024): https://arxiv.org/abs/2309.03409
- Optimizing Instructions and Demonstrations for Multi-Stage Language Model Programs, MIPRO (Opsahl-Ong et al., EMNLP 2024): https://arxiv.org/abs/2406.11695
- TextGrad (Yuksekgonul et al., 2024): https://arxiv.org/abs/2406.07496
- GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning (Agrawal et al., ICLR 2026): https://arxiv.org/abs/2507.19457
- Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (Zheng et al., NeurIPS 2023): https://arxiv.org/abs/2306.05685
- Large Language Models are not Fair Evaluators (Wang et al., 2023): https://arxiv.org/abs/2305.17926
- Judging the Judges (Thakur et al., GEM2 2025): https://arxiv.org/abs/2406.12624
- Who Validates the Validators? (Shankar et al., 2024): https://arxiv.org/abs/2404.12272
- Adding Error Bars to Evals (Miller, 2024, preprint): https://arxiv.org/abs/2411.00640
- The Effects of Test-Driven Development on External Quality and Productivity: A Meta-Analysis (Rafique, Mišić, IEEE TSE 2013): https://doi.org/10.1109/TSE.2012.28
- A Dissection of the Test-Driven Development Process (Fucci et al., IEEE TSE 2017): https://arxiv.org/abs/1611.05994
- Evaluation-Driven Development and Operations of LLM Agents, EDDOps (Xia et al., 2024, preprint): https://arxiv.org/abs/2411.13768

Anthropic e Claude Code:

- Skill authoring best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Equipping agents for the real world with Agent Skills (Zhang, Lazuka, Murag, 2025-10-16): https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- Demystifying evals for AI agents (Grace et al., 2026-01-09): https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- Effective context engineering for AI agents (2025-09-29): https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- skill-creator: https://github.com/anthropics/skills/tree/main/skills/skill-creator
- Improving skill-creator: test, measure and refine agent skills (2026-03-03): https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills
- Extend Claude with skills (Claude Code): https://code.claude.com/docs/en/skills
- Monitoring usage (Claude Code): https://code.claude.com/docs/en/monitoring-usage

Padrão aberto:

- Evaluating skill output quality: https://agentskills.io/skill-creation/evaluating-skills
- Optimizing skill descriptions: https://agentskills.io/skill-creation/optimizing-descriptions

OpenAI:

- Evaluation best practices: https://developers.openai.com/api/docs/guides/evaluation-best-practices
- Testing Agent Skills Systematically with Evals: https://developers.openai.com/blog/eval-skills
- Build skills (Codex): https://learn.chatgpt.com/docs/build-skills

Outras empresas:

- AGENTS.md outperforms skills in our agent evals (Vercel, Jude Gao, 2026-01-27): https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals
- Evaluating skills (LangChain, Robert Xu, 2026-03-05): https://www.langchain.com/blog/evaluating-skills
- Skill evals for measurable agent self-improvement (Deephaven, Don McKenzie, 2026-05-29): https://deephaven.io/blog/2026/05/29/agent-skills-evals/
- Evaluate agent skills using open source frameworks (Google Codelabs): https://codelabs.developers.google.com/codelabs/evaluate-agent-skills-using-open-source-frameworks

Praticantes:

- AI Evals FAQ (Hamel Husain e Shreya Shankar): https://hamel.dev/blog/posts/evals-faq/
- Your AI Product Needs Evals (Hamel Husain, 2024): https://hamel.dev/blog/posts/evals/
- An LLM-as-Judge Won't Save The Product, Fixing Your Process Will (Eugene Yan, 2025): https://eugeneyan.com/writing/eval-process/
- Claude Skills are awesome, maybe a bigger deal than MCP (Simon Willison, 2025-10-16): https://simonwillison.net/2025/Oct/16/claude-skills/
- Unit Tests for AI Agent Skills (Minko Gechev, 2026-02-26): https://blog.mgechev.com/2026/02/26/skill-eval/

Comunidade:

- obra/superpowers, writing-skills: https://github.com/obra/superpowers/tree/main/skills/writing-skills
- Skills for Claude (Jesse Vincent, 2025-10-16): https://blog.fsck.com/2025/10/16/skills-for-claude
- mattpocock/skills (pastas `in-progress/`, `skills/engineering/retro`, SCOPE.md): https://github.com/mattpocock/skills
- claude-reflect: https://github.com/BayramAnnakov/claude-reflect
- Claudeception: https://github.com/blader/Claudeception
- everything-claude-code (continuous-learning-v2): https://github.com/affaan-m/everything-claude-code
- Show HN: Agent-skills-eval: https://news.ycombinator.com/item?id=48046023
- Skills are quietly becoming the unit of agent knowledge: https://news.ycombinator.com/item?id=47475832
- Claude Skills (HN, 2025-10-16): https://news.ycombinator.com/item?id=45607117
- anthropics/skills, issue 518: https://github.com/anthropics/skills/issues/518
