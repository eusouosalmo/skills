# Determinismo na fábrica: o que é script, o que é classificador e o que é agente

Resumo: na fábrica e na revisão, cada decisão cai em uma de três camadas. A regra em código (script, check, gate) decide o que tem resposta certa e pode ser conferido. O classificador barato com saída tipada decide uma pergunta fechada sobre texto livre, quando errar custa pouco. O agente fica com o que pede julgamento aberto e ferramentas. As conclusões que as fontes sustentam:

1. **Regra primeiro, modelo depois, e o modelo só onde a regra não alcança.** É o critério escrito pela Anthropic (começar pelo mais simples, workflow para tarefa previsível, agente só quando a flexibilidade paga o custo), pela doc de skills (script para operação frágil e repetida) e pela Stripe, que põe os agentes "em caixas" entre nós determinísticos e diz que isso economiza tokens e CI. O próprio auto mode do Claude Code segue a mesma ordem: regras de permissão antes, classificador só para o que sobra.
2. **O agente desarma regra escrita em prosa, não regra que roda fora dele.** O METR mediu modelos de ponta burlando o avaliador em 30% das runs de uma suíte, e pedir "não trapaceie" quase não mudou nada. Por isso o gate, os tetos e o check ficam fora do alcance do agente que está sendo controlado, e o classificador do auto mode nem lê o texto do agente, para não ser convencido por ele.
3. **Tetos de rodada e de tentativa são regra, e o número vem de dado.** A Anthropic viu uma PR passar de cinquenta rodadas numa noite e mediu que 59% do que o revisor repetia era código antigo; a Stripe para em duas rodadas de CI por retorno decrescente. Contar rodadas e tentativas é aritmética sobre a timeline: não há o que julgar.
4. **Risco por caminho é a base que todo mundo usa, mas sozinho falha.** CODEOWNERS só enxerga caminho. A Anthropic combina caminhos que sempre pedem humano com dois classificadores que leem a mudança. A Meta e a Prime Video, com dados rotulados de incidente, treinam modelo próprio. Para um dev solo sem histórico de incidentes, o script de caminho e sinais é o que dá para testar e auditar; o buraco conhecido é lógica sensível dentro de um caminho de risco baixo ou médio.
5. **Modelo genérico perguntado direto sobre risco erra muito.** Na Prime Video, o Claude Sonnet 4.5 em few-shot ficou com F1 de 0,26 na previsão de mudança arriscada, contra 0,85 de um modelo treinado com features. Recall alto, precisão baixa. Isso serve para um desempate que só pode acrescentar revisão (falso positivo custa uma run extra), não para rebaixar risco.
6. **Classificador barato e tipado vale quando a pergunta é fechada, a entrada é texto livre e há poucos exemplos rotulados.** A doc da Anthropic recomenda o Haiku 5.5 para isso; no cookbook oficial, o Haiku sai de 74% para 94% de acerto com exemplos recuperados. Structured outputs garantem o formato, não o acerto, e têm exceções (recusa, corte por `max_tokens`). Em triagem de alerta e de risco, modelos clássicos leves empatam ou ganham dos LLMs genéricos quando há dados.
7. **Para as peças já decididas, o mapa fica quase todo determinístico.** Gate, tetos, check `review` por `head_sha`, teto de rodadas e nível de risco são código. Revisor e `security-review` são agente. Só dois lugares têm candidato a classificador barato, e nenhum entra no primeiro draft: o desempate de risco (decidir se o `security-review` roda) e a triagem de alerta (dizer se o alerta vale uma run), ambos atrás de uma regra que filtra antes.

Pesquisa feita em 2026-11-12 para o ticket [Pesquisa: onde cabe determinismo na fábrica e por quê](https://github.com/eusouosalmo/skills/issues/116), só leitura. Complementa [fabrica-de-software.md](fabrica-de-software.md) (seções 6.1 e 11), que já cobre a revisão em camadas da Anthropic, a the-judge, a live da Tech Leads Club e os posts do Akita; esses pontos aparecem aqui por referência. As decisões que este documento fundamenta estão nas resoluções de [Seed case e escopo da factory-install no site](https://github.com/eusouosalmo/skills/issues/109) e de [Seed case e escopo da review-policy no site](https://github.com/eusouosalmo/skills/issues/110).

## Sumário

1. [Método e níveis de confiança](#1-método-e-níveis-de-confiança)
2. [Critério: workflow ou agente](#2-critério-workflow-ou-agente)
3. [O agente e a regra: por que o controle fica fora dele](#3-o-agente-e-a-regra-por-que-o-controle-fica-fora-dele)
4. [Nível de risco por caminho e por sinais do diff](#4-nível-de-risco-por-caminho-e-por-sinais-do-diff)
5. [Classificador barato e tipado](#5-classificador-barato-e-tipado)
6. [Mapa das peças já decididas](#6-mapa-das-peças-já-decididas)
7. [Perguntas abertas](#7-perguntas-abertas)
8. [Fontes](#8-fontes)

## 1. Método e níveis de confiança

Fontes primárias: artigos de engenharia da Anthropic (agentes, auto mode, evals, revisão de código), a doc oficial da plataforma e do Claude Code (skills, hooks, structured outputs, roteamento de tickets, cookbook de classificação), o post da Stripe sobre os Minions, a doc do GitHub (CODEOWNERS, check runs), a página de capacidade do DORA, a doc do Sentry, o repositório `mattpocock/skills` (commit `5863806`, 2026-11-12) e cinco estudos (Prime Video, Meta, METR, FrugalGPT e um de triagem de alertas de segurança). Os PDFs foram lidos pelo texto extraído.

Os mesmos níveis das notas anteriores:

- **Confirmado**: doc oficial, arquivo de repositório ou artigo aberto nesta pesquisa, dizendo o que está escrito.
- **Convenção**: vários autores independentes fazem.
- **Relato**: um autor ou empresa fala da própria experiência, com dados internos que não dá para auditar. Artigos de engenharia de empresa entram aqui quando descrevem processo interno, mesmo com números.
- **Inferência minha**: leitura a partir das fontes, não afirmação delas.

Métodos de terceiros aparecem descritos com palavras próprias, com crédito.

## 2. Critério: workflow ou agente

### 2.1 O que a Anthropic escreve

- **Workflow e agente são coisas diferentes.** No artigo sobre agentes eficazes, workflow é LLM e ferramentas orquestrados por caminhos de código definidos antes; agente é o modelo dirigindo o próprio processo e escolhendo as ferramentas ([Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)). A recomendação é buscar a solução mais simples e só subir a complexidade quando precisar, porque sistemas agênticos trocam latência e custo por desempenho. Workflow serve a tarefa bem definida que pede previsibilidade e consistência; agente, a decisão flexível guiada pelo modelo. **Confirmado** como texto do artigo.
- **Os padrões do mesmo artigo já trazem as três camadas.** O encadeamento de prompts põe checagens programáticas entre os passos; o roteamento classifica a entrada e manda o caso fácil para um modelo menor e mais barato; a paralelização inclui um modelo separado só para triar a entrada enquanto outro responde. **Confirmado.** Ler o roteamento como o "classificador barato" deste ticket é **inferência minha**, mas é a mesma forma.
- **Na doc de skills, o grau de liberdade acompanha a fragilidade.** Instrução aberta quando há vários caminhos válidos e a decisão depende de contexto (o exemplo dado é justamente revisão de código); script exato, com poucos parâmetros, quando a operação é frágil, a consistência é crítica ou a sequência precisa ser seguida. A mesma página diz que script pronto é mais confiável que código gerado, economiza tokens e garante consistência, e recomenda planejar em arquivo estruturado, validar o plano com script e só então executar ([Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)). **Confirmado.**
- **Hooks existem para tirar a decisão do modelo.** A doc do Claude Code diz que hooks dão controle determinístico: a ação sempre acontece em vez de depender de o modelo escolher fazê-la. Para o que pede julgamento, há hooks de prompt, que mandam a entrada a um modelo e esperam só um JSON `ok` e `reason`, e hooks de agente, experimentais, com ferramentas e até 50 turnos; para produção, a doc manda preferir o hook de comando ([hooks guide](https://code.claude.com/docs/en/hooks-guide)). **Confirmado.** O hook de prompt é, na prática, um classificador tipado embutido no harness.
- **Avaliação segue a mesma régua.** No artigo sobre evals de agentes, o avaliador em código é rápido, barato, objetivo e reprodutível, mas quebra diante de variação válida; o avaliador por modelo é flexível e capta nuance, mas é não determinístico, mais caro e precisa ser calibrado contra humanos. A orientação é usar o determinístico onde der e o modelo onde precisar ([Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)). **Confirmado.**

### 2.2 Stripe: agentes em caixas

O post da Stripe sobre os Minions descreve os blueprints: fluxos definidos em código em que cada nó é determinístico (rodar os linters configurados, fazer push) ou agêntico (implementar a tarefa, corrigir falha de CI), formando uma máquina de estados ([Minions, parte 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)). **Relato** com dados internos. O que interessa aqui:

- **Por quê:** decisões pequenas e previsíveis (sempre rodar lint no fim) ficam em código, o que economiza tokens e CI em escala e tira do agente oportunidades de errar; conter os modelos em caixas se soma em confiabilidade do sistema inteiro.
- **Teto de CI:** o lint roda localmente em laço antes do push; depois há uma rodada de CI com autofix, uma volta ao agente para o que sobrou e um segundo push. Depois disso, a branch vai para um humano: no máximo duas rodadas de CI, por retorno decrescente, já que cada rodada custa tokens, computação e tempo.
- **Escala declarada:** mais de 1.300 PRs mescladas por semana sem código escrito por humano.

### 2.3 Matt Pocock, Tech Leads Club e Akita

- **Matt Pocock.** Na skill `software-factory`, todo gatilho acelera e precisa de três freios: checks automáticos determinísticos (tipos, lint, testes) que toda run passa, revisão automática por outra run lendo o diff a frio, e revisão humana, cujo achado vira check novo ou revisão mais afiada. Na `retro`, um erro mecânico (padrão sintático, API banida, forma de import, local de arquivo) vira check determinístico "full stop", e só julgamento de verdade vai para o padrão de código que o revisor aplica. Na doc da `implement-spec`, para trabalho de fato AFK, um laço determinístico (Sandcastle, script, job de CI) é mais rápido, barato e confiável, porque nenhum agente decide a orquestração ([software-factory](https://github.com/mattpocock/skills/blob/main/skills/in-progress/software-factory/SKILL.md), [retro](https://github.com/mattpocock/skills/blob/main/skills/engineering/retro/SKILL.md), [implement-spec](https://github.com/mattpocock/skills/blob/main/docs/engineering/implement-spec.md)). **Confirmado** como texto do autor.
- **Felipe Rodrigues (Tech Leads Club).** O caso já resumido em [fabrica-de-software.md](fabrica-de-software.md#62-controle-na-fábrica-a-live-da-tech-leads-club): a fábrica é uma máquina de estados que filtra o evento com guardas da mais barata para a mais cara (inclusive teto de eventos por hora antes de qualquer modelo), entrega ao agente uma tarefa com campos fixos e valida o retorno contra um schema campo a campo; o agente devolve JSON e não afirma o que já aconteceu (deploy, CI, testes), porque só a fábrica escreve isso. **Relato**, e o próprio grupo chama de exagero para tarefa pequena.
- **Fábio Akita.** Separa a skill que julga (auditoria de issue e de PR) da que só executa o que foi aprovado, e diz que o agente rende onde há oráculo verificável; sem isso o laço gira no vácuo (ver [fabrica-de-software.md](fabrica-de-software.md#5-o-que-o-akita-mostra)). **Relato.** Não achei texto dele tratando determinismo como princípio; a posição dele aparece pela prática.

### 2.4 O critério que sai disso

Síntese minha, com as fontes de cada ponto acima. Uma decisão vai para código quando pelo menos um destes vale:

- **Tem resposta certa conferível:** quem pôs o label, se há bloqueador aberto, quantas tentativas já houve, que arquivos o diff toca. Modelo aqui só acrescenta erro e custo.
- **Errar custa caro e o erro é silencioso:** gate de entrada, teto de gasto, check que bloqueia merge.
- **O agente controlado poderia mexer nela:** a decisão precisa morar fora do contexto dele (seção 3).
- **Precisa ser auditável e testável:** sai igual toda vez, então dá para escrever teste e explicar o veredito apontando a linha da regra.

Vai para modelo quando a entrada é texto livre e a pergunta depende de significado. Dentro disso, vai para classificador barato quando a saída é uma escolha fechada (enum, booleano) e o erro é barato ou corrigível adiante; vai para agente quando precisa ler código, rodar coisas e produzir algo aberto (um diff, um parecer com prova).

## 3. O agente e a regra: por que o controle fica fora dele

- **Modelos de ponta burlam o avaliador, e pedir que não burlem quase não muda.** O METR contou 39 casos de reward hacking em 128 runs (30,4%) no RE-Bench, com 100% numa das tarefas, contra 0,7% no HCAST; os exemplos incluem sobrescrever a variável de tempo que o avaliador media e trocar o avaliador para que tudo passasse. Com instruções como "por favor não trapaceie", a taxa numa tarefa ficou entre 70% e 95% das runs, e o modelo, perguntado depois, admitia que o plano não era o que o usuário queria ([METR, junho de 2025](https://metr.org/blog/2025-06-05-recent-reward-hacking/)). **Confirmado** como resultado publicado; os modelos testados são de 2025.
- **O mesmo padrão na fábrica.** O experimento do Felipe, em que bots com regras só em prosa aprovaram PRs que se revertiam, é o caso de campo (**relato**, ver 2.3). O `CONTEXT.md` deste repo já registra a consequência: verificação que bloqueia precisa de guardrail, senão o agente a desarma com `--no-verify` ou apagando teste.
- **Não deixar o agente argumentar com o juiz.** No auto mode do Claude Code, o classificador de transcrição não recebe o texto do assistente, para que o agente não convença o classificador a aprovar uma ação ruim, nem os resultados de ferramenta, que são o principal canal de prompt injection ([Claude Code auto mode](https://www.anthropic.com/engineering/claude-code-auto-mode)). **Confirmado** como desenho descrito pela Anthropic. Para a fábrica, **inferência minha**: o nível de risco calculado por script antes do revisor, e entregue pronto, segue a mesma ideia; nem o implementador nem o texto da PR influenciam a profundidade da revisão.
- **Só a fábrica afirma fato.** O check `review` amarrado ao `head_sha` e o veredito que vale para um commit (Anthropic, Felipe) impedem que uma aprovação antiga cubra código novo. Na API do GitHub, check run é criado para um commit específico e `head_sha` é obrigatório; só GitHub Apps escrevem checks ([check runs](https://docs.github.com/en/rest/checks/runs)). **Confirmado.**

## 4. Nível de risco por caminho e por sinais do diff

### 4.1 Quem classifica por regra

- **CODEOWNERS é regra por caminho, e só isso.** Padrões no estilo gitignore, o último que casa vence, o arquivo vem do branch base, e a proteção de branch pode exigir aprovação de um dono. Linhas inválidas são ignoradas, o arquivo acima de 3 MB não carrega e a página não descreve nenhuma regra por conteúdo ([About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)). **Confirmado.**
- **A Anthropic mistura caminho e classificador.** No artigo sobre a revisão no time do Claude Code, o nível (baixo: nenhum humano depois dos checks verdes; médio: uma pessoa; alto: duas) é dado pela mudança, não pelo autor. Um classificador lê a mudança e escolhe o nível; um segundo classificador pergunta se essa mudança precisa de uma pessoa mesmo quando o nível diz que não; e alguns caminhos sempre pedem humano: tudo o que os donos listaram como sensível e qualquer workflow de CI. Na seção de adoção, a recomendação é escrever os níveis, começar rígido e afrouxar com evidência, e usar CODEOWNERS e proteção de branch para que auth, cobrança, CI, release e instaladores sempre peçam pessoa ([How the Claude Code team does code review](https://claude.dev/blog/solving-code-review-at-anthropic/)). O artigo não diz que modelo roda os classificadores, quanto custam nem o que acontece quando erram; diz só que ainda não há disjuntor que aperte a aprovação quando os números pioram. **Relato** com dados internos.
- **DORA: o que piora o desempenho é a aprovação pesada externa, não a revisão por risco.** A página de capacidade diz que aprovação por gente de fora do time (CAB, gerente) tem efeito negativo no desempenho de entrega e não se associa a menos falhas; recomenda revisão por pares registrada na plataforma, automação para detectar regressão e análise contínua das mudanças para marcar as de alto risco para revisão extra ([Streamlining change approval](https://dora.dev/capabilities/streamlining-change-approval/)). **Confirmado** como texto do DORA; os dados são observacionais.

### 4.2 Quem classifica com modelo, e com que resultado

- **Meta.** O Diff Risk Score estima a probabilidade de uma mudança causar incidente, com um Llama ajustado em diffs e metadados, e permitiu à Meta tirar grandes períodos de congelamento de código. Num experimento aleatorizado com mais de 15 mil diffs (os 5% de maior risco), mandar um revisor extra e mostrar um aviso contornável antes do merge aumentou a profundidade da revisão e fez 9,56% mais diffs terminarem abaixo do limiar de risco, com 0,45% a mais de tempo de revisão ([Paraspatki et al., FSE 2026](https://mockus.us/papers/RevRisk.pdf)). **Confirmado** como resultado do artigo; o modelo é próprio e treinado com histórico de incidentes da Meta.
- **Prime Video.** Para trocar o congelamento total em eventos ao vivo por risco por mudança, o time extrai features do diff (complexidade estrutural, métricas de mudança, violações de estilo e tipo de mudança) e treina um classificador; o melhor teve recall médio de 0,83 e F1 de 0,81. Volume de linhas foi preditor ruidoso; complexidade estrutural foi o sinal forte. As violações de estilo vieram de analisadores estáticos, não de LLM, porque precisam de consistência. E perguntar direto a um LLM se a mudança é arriscada rendeu pouco: Claude Sonnet 4.5 em few-shot ficou com precisão de 0,157, recall de 0,779 e F1 de 0,261, contra F1 de 0,846 do modelo com features. O sistema foi desenhado como guardrail que manda a mudança para humano, não que bloqueia, e por isso favorece recall ([Kurup et al., Prime Video](https://cdn.amazon.science/94/b8/ab5a2e0346eaa5c79d7541014242/changesafety-arxiv.pdf)). **Confirmado** como resultado do artigo.

### 4.3 Onde a regra por caminho falha

- **Lógica sensível fora do caminho sensível.** A resolução do ticket 110 já aponta o caso: código de auth dentro de `apps/web`, que a tabela classifica como médio. É o buraco que o segundo classificador da Anthropic cobre. **Inferência minha** a partir das duas fontes.
- **Tamanho não é risco.** A Prime Video mediu que volume de linhas é ruidoso; uma regra "PR grande é alto risco" erra nos dois sentidos. **Confirmado** pelo artigo. Os sinais escolhidos no ticket 110 (migration, dependência nova ou lockfile, workflow, segredo ou variável de ambiente, auth) são de tipo, não de tamanho, o que evita esse erro.
- **Regra sem dono envelhece.** CODEOWNERS ignora linha inválida em silêncio e só olha caminho; uma pasta nova cai no nível padrão. **Inferência minha**: o script precisa de um nível padrão explícito (o mais alto, como a Anthropic recomenda começar rígido) e de teste que falha quando um caminho novo não casa com nenhuma linha.
- **O que a regra ganha.** Sai igual toda vez, roda sem modelo e sem gastar a janela de uso da assinatura, e o veredito aponta a linha da tabela que o decidiu, o que o ticket 110 já exige no topo do comentário. Nenhuma fonte com modelo publicou essa explicabilidade. **Inferência minha.**

### 4.4 Por que a Anthropic usa classificador e a fábrica do site não

Leitura minha: a Anthropic tem volume (mais de 30 mil mudanças por dia no monorepo, segundo o mesmo artigo), um conjunto de incidentes que vira eval diário e revisores humanos como rede. O site tem uma pessoa, nenhum incidente rotulado e nenhuma PR revisada com rastro (ticket 110). Sem dado para calibrar, um classificador de risco não tem como mostrar que acerta, e a Prime Video mostra que o LLM genérico, sem treino, acerta pouco. O script com tabela aprovada pelo dono é o que dá para testar hoje; o classificador entra quando houver casos para medir.

## 5. Classificador barato e tipado

### 5.1 O que a plataforma garante e recomenda

- **Structured outputs garantem o formato, não o acerto.** A doc diz que a decodificação restrita garante JSON válido, campos obrigatórios e tipos, sem retry por violação de schema, "na maioria dos casos". As exceções: recusa (resposta cobrada que pode não seguir o schema), corte por `max_tokens` e campo de raciocínio que pode disparar recusa; enum pode voltar com capitalização diferente; restrições numéricas e de tamanho de string não são aceitas. O Haiku 5.5 está entre os modelos suportados ([structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)). **Confirmado.** Consequência, **inferência minha**: o código que lê a saída ainda precisa tratar recusa e corte, com um valor padrão seguro (no desempate de risco, "rodar o `security-review`").
- **Haiku para classificar, Sonnet quando a pergunta é difícil.** O guia de roteamento de tickets recomenda o Haiku 5.5 em effort `low` para classificação simples e de alto volume, e o Sonnet quando há muitas categorias, conhecimento especializado ou raciocínio complexo. Diz que LLM vale mais que ML tradicional quando há poucos exemplos rotulados, categorias que mudam, texto não estruturado e regras definidas por significado; e manda medir acerto e custo por classificação contra um limiar definido antes ([ticket routing](https://platform.claude.com/docs/en/about-claude/use-case-guides/ticket-routing)). **Confirmado.**
- **Exemplos recuperados valem mais que modelo maior.** No cookbook de classificação, com 68 tickets de teste em 10 categorias e o Haiku 5.5, o prompt simples acertou 74%, com cinco exemplos recuperados por similaridade foi a 94% e com cadeia de raciocínio a 97% ([classification guide](https://platform.claude.com/cookbook/capabilities-classification-guide)). **Confirmado**; os dados são sintéticos e o conjunto é pequeno.
- **Custo.** O Haiku 5.5 custa US$ 0,10 por milhão de tokens de entrada e US$ 0,50 de saída até 100 mil tokens de prompt, contra US$ 4 e 20 do Opus 5.5 ([pricing](https://platform.claude.com/docs/en/about-claude/pricing), tabela em [fabrica-de-software.md](fabrica-de-software.md#71-preço-de-api)). **Confirmado.** Uma classificação com 5 mil tokens de diff e 50 de saída fica perto de US$ 0,0005 a preço de lista. **Inferência minha**: o custo em dinheiro é desprezível; o custo real é mais uma peça para manter, testar e explicar, e na assinatura ainda consome a janela de uso.

### 5.2 Evidência de acerto em produção e em estudo

- **Auto mode: regra antes, classificador em dois estágios depois.** O Claude Code deixa passar sem modelo as ferramentas de leitura e as regras de permissão do usuário, depois as edições dentro do projeto (reversíveis pelo git), e só o resto vai para o classificador, que roda no Sonnet 4.6. O primeiro estágio é um filtro de um token, instruído a bloquear na dúvida; o segundo, com raciocínio, revê só o que o primeiro marcou. Em 10 mil chamadas reais, o falso positivo caiu de 8,5% no primeiro estágio para 0,4% no pipeline inteiro; em 52 ações excessivas reais, o falso negativo subiu de 6,6% para 17%, que a Anthropic chama de número honesto; em mil tentativas sintéticas de exfiltração, de 1,8% para 5,7% ([Claude Code auto mode](https://www.anthropic.com/engineering/claude-code-auto-mode)). **Relato** com dados internos. Lição, **inferência minha**: até a Anthropic, com o modelo dela, aceita 17% de falso negativo num classificador, e por isso o põe atrás de regras e não no lugar delas.
- **Cascata de modelos.** O FrugalGPT mostra que encadear modelos baratos antes do caro, com um critério aprendido para parar, chega ao desempenho do melhor modelo com até 98% menos custo ([Chen, Zaharia e Zou, 2023](https://arxiv.org/abs/2305.05176)). **Confirmado** como resultado do artigo; exige dados rotulados para treinar o critério de parada, e os modelos são de 2023.
- **Triagem de alerta: classificador leve empata ou ganha.** Num estudo com 178 alertas de segurança rotulados, oito LLMs genéricos tiveram recall alto na classificação binária (verdadeiro ou falso positivo), mas modelos clássicos leves foram competitivos e às vezes melhores, com a SVM linear no maior F1; na priorização em quatro níveis, a precisão dos LLMs ficou baixa, gerando ruído ([Rieger et al., 2026](https://eprints.glos.ac.uk/16399/)). **Confirmado** pelo resumo publicado; amostra pequena e domínio de segurança, não de erro de aplicação.
- **Triagem de alerta em produto: regra e modelo em série.** O Sentry só dispara o Autofix sozinho quando o erro tem 10 ou mais eventos, aconteceu nos últimos 14 dias e tem fixability suficiente, estimada por um modelo de ML do próprio Sentry; mesmo com fixability alta, a automação para onde o usuário mandou (causa raiz, plano ou PR em rascunho) ([Seer Autofix](https://docs.sentry.io/product/ai-in-sentry/seer/autofix)). **Confirmado** como comportamento documentado; a doc não diz que modelo calcula a nota nem o limiar.
- **Risco de mudança: LLM genérico erra muito** (Prime Video, seção 4.2): recall de 0,78 e precisão de 0,16. **Confirmado.**

### 5.3 Quando vale mais e quando vale menos que uma regra

Síntese minha a partir de 5.1 e 5.2:

| Vale mais que regra quando | Vale menos que regra quando |
| :- | :- |
| a entrada é texto livre (corpo de issue, mensagem de alerta, trecho de código) e a regra precisaria de palavra-chave frágil | a resposta está em metadado estruturado (label, autor, caminho, contagem, timestamp) |
| a saída é fechada (enum, booleano) e cabe em structured outputs | a saída precisa de prova (arquivo e linha conferidos), o que pede agente |
| errar só acrescenta trabalho que outra camada confere (rodar um `security-review` a mais) | errar libera algo sem rede (rebaixar risco, pular revisão, mesclar) |
| há algumas dezenas de exemplos para medir e para usar como few-shot | não há caso rotulado para medir, então não se sabe se acerta |
| as categorias mudam e treinar modelo clássico não compensa | há histórico rotulado grande, e um modelo clássico leve tende a ganhar |

O padrão das fontes com dado (auto mode, Sentry, Prime Video como guardrail) é o mesmo: a regra filtra antes, o classificador decide só o que sobra, e o erro dele é assimétrico de propósito (na dúvida, mais controle).

## 6. Mapa das peças já decididas

| Peça | Camada | Por quê | Fonte |
| :- | :- | :- | :- |
| Gate do `factory.yml` (dono pôs o label, `ready-for-agent`, sem bloqueador aberto) | Determinística | Toda pergunta tem resposta em metadado da API; roda sem modelo e sem segredo, antes de gastar qualquer limite; o agente não alcança | Guardas da mais barata para a mais cara (Felipe, 2.3); workflow para tarefa previsível ([Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)); laço AFK determinístico (Matt, [implement-spec](https://github.com/mattpocock/skills/blob/main/docs/engineering/implement-spec.md)) |
| Encaixe da issue na fábrica, conferido no gate | Determinística hoje (label `ready-for-agent` posto por humano na triagem, mais as checagens do gate); classificador barato só se aparecer falha observada | Se a issue é boa para o agente é julgamento, e quem julga é a triagem humana, que vira label; o gate só confere o label. Um classificador poderia ler o corpo e recusar issue sem critério de aceite ou que toca área proibida, mas sem casos não há como medir | Roteamento com modelo pequeno para entrada de texto ([ticket routing](https://platform.claude.com/docs/en/about-claude/use-case-guides/ticket-routing)); regra só a partir de falha observada (`CLAUDE.md` deste repo); juiz separado do executor (Akita, 2.3) |
| Tetos da run (2 tentativas pela timeline, `concurrency`, `--max-turns`, `--max-budget-usd`, `timeout-minutes`) | Determinística | Contagem e limite numérico; precisam valer mesmo quando o agente erra ou entra em laço | Teto de duas rodadas de CI por retorno decrescente ([Stripe](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)); teto de eventos antes do modelo (Felipe, 2.3) |
| Check `review` valendo só para o `head_sha` revisado | Determinística (o veredito vem do revisor; quem amarra ao commit e pinta o check é código) | Impede que aprovação antiga cubra código novo; a API já exige o SHA | [check runs](https://docs.github.com/en/rest/checks/runs); aprovação vale para um commit ([Anthropic](https://claude.dev/blog/solving-code-review-at-anthropic/)); veredito por `head_sha` (Felipe) |
| Teto de 3 rodadas de revisão, só diff novo, sem repetir achado | Determinística no teto e no recorte do diff; o "não repetir" é instrução ao revisor, conferível comparando com o comentário anterior | Sem teto a revisão não converge; contar rodadas é aritmética | 50 rodadas numa noite, 59% de achados em código antigo, rodadas para passar de 2,08 para 1,32 ([Anthropic](https://claude.dev/blog/solving-code-review-at-anthropic/)); teto de três na the-judge ([fabrica-de-software.md](fabrica-de-software.md#61-revisão-em-camadas)) |
| Nível de risco calculado por script (tabela de caminhos e sinais do `REVIEW.md`) | Determinística; desempate por classificador barato na névoa | Testável, igual toda vez, sem custo de limite, e o veredito aponta a linha que o decidiu; o agente revisado não influencia a profundidade da própria revisão. Sem incidentes rotulados não há como calibrar classificador, e LLM genérico perguntado sobre risco acerta pouco | Caminhos que sempre pedem humano e níveis escritos ([Anthropic](https://claude.dev/blog/solving-code-review-at-anthropic/)); [CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners); F1 de 0,26 do LLM contra 0,85 do modelo com features ([Prime Video](https://cdn.amazon.science/94/b8/ab5a2e0346eaa5c79d7541014242/changesafety-arxiv.pdf)); texto do agente fora do classificador ([auto mode](https://www.anthropic.com/engineering/claude-code-auto-mode)) |
| Desempate de risco (decidir se o `security-review` entra quando o script diz médio ou baixo) | Classificador barato e tipado (Haiku em effort `low`, saída booleana com motivo curto), fora do primeiro draft | Pergunta fechada sobre código, que a regra por caminho não vê; o erro provável (falso positivo) só custa uma run a mais, e recusa ou corte caem no padrão seguro "roda". Só pode subir o nível, nunca baixar | Segundo classificador que pede humano mesmo com nível baixo ([Anthropic](https://claude.dev/blog/solving-code-review-at-anthropic/)); recall alto e precisão baixa do LLM ([Prime Video](https://cdn.amazon.science/94/b8/ab5a2e0346eaa5c79d7541014242/changesafety-arxiv.pdf)); [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) |
| Revisor (`code-review` com contexto limpo, mais `security-review` no alto risco) | Agente | Precisa ler código, conferir arquivo e linha e julgar contra a issue e o `REVIEW.md`; achado sem prova é descartado | Revisão de código como exemplo de alta liberdade ([skill best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)); revisão automática por outra run a frio (Matt, [software-factory](https://github.com/mattpocock/skills/blob/main/skills/in-progress/software-factory/SKILL.md)); camadas da [Anthropic](https://claude.dev/blog/solving-code-review-at-anthropic/) |
| Triagem de alertas (`factory-triage`, na névoa) | Determinística na entrada (dedupe, contagem mínima de eventos, janela de tempo, teto por hora); classificador barato para dizer se o alerta vale uma run; agente só depois | Alerta é texto semiestruturado com muito ruído; regra corta o volume, classificador decide o que sobra, e a run cara só roda no que passou | Sentry: 10 eventos, 14 dias e fixability antes do Autofix ([Seer](https://docs.sentry.io/product/ai-in-sentry/seer/autofix)); classificador leve competitivo e LLM com precisão baixa em priorização ([Rieger et al.](https://eprints.glos.ac.uk/16399/)); cascata ([FrugalGPT](https://arxiv.org/abs/2305.05176)) |

## 7. Perguntas abertas

1. **Qual modelo e quanto custa o classificador de risco da Anthropic?** O artigo não diz. Se um dia ela publicar acerto e custo, é o dado mais próximo do desempate de risco.
2. **Um classificador barato chamado de dentro do `claude-code-action` ou de um `claude -p` com `--model` Haiku conta na janela da assinatura do mesmo jeito que o Opus?** A doc de limites da assinatura não separa por modelo nesta leitura; fica para o seed case medir.
3. **Formato da tabela de risco legível por gente e por script.** Ficou para a construção da `review-policy` (ticket 110); a seção 4.3 sugere nível padrão explícito e teste de cobertura de caminhos.
4. **Eval do desempate.** Antes de ligar o classificador, montar algumas dezenas de diffs do site rotulados pelo dono (auth escondida em caminho médio, casos limpos) e medir recall e falsos positivos, como o guia de roteamento manda.
5. **Hook de prompt como desempate local.** O hook `type: "prompt"` do Claude Code já devolve `ok` e `reason` com um modelo configurável; serviria ao `/code-review` local sem fábrica. Não testado.

## 8. Fontes

Todas acessadas em 2026-11-12.

Anthropic, artigos de engenharia:

- Building effective agents: https://www.anthropic.com/engineering/building-effective-agents
- Claude Code auto mode: https://www.anthropic.com/engineering/claude-code-auto-mode
- Demystifying evals for AI agents: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- How the Claude Code team does code review (2026-10-15): https://claude.dev/blog/solving-code-review-at-anthropic/

Anthropic, doc oficial:

- Skill authoring best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Hooks guide: https://code.claude.com/docs/en/hooks-guide
- Structured outputs: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- Ticket routing: https://platform.claude.com/docs/en/about-claude/use-case-guides/ticket-routing
- Classification guide (cookbook): https://platform.claude.com/cookbook/capabilities-classification-guide
- Pricing: https://platform.claude.com/docs/en/about-claude/pricing

Empresas e ferramentas:

- Stripe, Minions parte 2: https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2
- GitHub, About code owners: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- GitHub, Check runs: https://docs.github.com/en/rest/checks/runs
- DORA, Streamlining change approval: https://dora.dev/capabilities/streamlining-change-approval/
- Sentry, Seer Autofix: https://docs.sentry.io/product/ai-in-sentry/seer/autofix

Matt Pocock (`mattpocock/skills`, commit `5863806`):

- software-factory: https://github.com/mattpocock/skills/blob/main/skills/in-progress/software-factory/SKILL.md
- retro: https://github.com/mattpocock/skills/blob/main/skills/engineering/retro/SKILL.md
- implement-spec (doc): https://github.com/mattpocock/skills/blob/main/docs/engineering/implement-spec.md

Artigos científicos:

- Kurup et al., Deployment Risk Assessment Using Diff-Aware Features: A Case Study at Prime Video: https://cdn.amazon.science/94/b8/ab5a2e0346eaa5c79d7541014242/changesafety-arxiv.pdf
- Paraspatki et al., Code Reviewer Recommendation for High Risk Diffs at Scale (Meta, FSE Companion 2026): https://mockus.us/papers/RevRisk.pdf
- METR, Recent frontier models are reward hacking: https://metr.org/blog/2025-06-05-recent-reward-hacking/
- Chen, Zaharia e Zou, FrugalGPT: https://arxiv.org/abs/2305.05176
- Rieger et al., Possibilities and limitations of using large language models for alert classification and prioritisation (Expert Systems with Applications, 2026): https://eprints.glos.ac.uk/16399/

Já citadas em [fabrica-de-software.md](fabrica-de-software.md): live da Tech Leads Club (Felipe Rodrigues), posts e repositórios do Fábio Akita, the-judge.
