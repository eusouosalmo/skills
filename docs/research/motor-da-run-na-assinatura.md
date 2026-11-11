# Motor da run da fábrica na assinatura

Resumo: com a assinatura do Claude e sem API key paga à parte, o motor mais sólido hoje para uma run disparada por label num repo privado de um dono só é o `anthropics/claude-code-action@v1` com `claude_code_oauth_token`. É o caminho documentado, roda como o app do Claude (os commits disparam a CI), barra quem não tem write access e devolve um `execution_file` com o custo estimado e o desfecho de cada run. Um step com `claude -p` faz o mesmo com mais controle e mais armadilhas. As scheduled tasks (ex routines) já recebem evento de issue sem runner, mas não devolvem custo e ainda estão em research preview. O Code Review gerenciado não existe para plano individual. O crédito de API do Max e do Ultra funciona como "API sem custo extra" até acabar, com teto de verdade em dólar, mas **o Pro não tem crédito incluso**: no Pro, a segunda pista é pagar à parte (usage credits ou crédito do Console). A mudança de cobrança de junho de 2026 continua pausada, sem data nova.

Sobre dedicar uma segunda conta Pro só à fábrica (seção 10): nenhum termo proíbe uma pessoa de ter duas contas pagas nem usar o token de uma delas na CI do próprio repo, e nenhum fala em limite de uso. Mas os termos de consumidor proíbem contornar "systems or protective measures", a Usage Policy proíbe burlar restrições dos produtos, e a doc diz que os limites pressupõem uso individual comum. Duas contas para dobrar o limite é zona cinzenta, não regra clara; os caminhos sem ambiguidade são o Max, os usage credits ou uma API key.

Pesquisa feita em 2026-11-11 para o ticket [#115](https://github.com/eusouosalmo/skills/issues/115), filho do mapa [#103](https://github.com/eusouosalmo/skills/issues/103). Complementa as seções 7 e 11 de [fabrica-de-software.md](fabrica-de-software.md), que não são repetidas aqui; o que foi reconferido aparece marcado. A doc do Claude Code muda toda semana: confira a página antes de decidir.

## Sumário

1. [Método e níveis de confiança](#1-método-e-níveis-de-confiança)
2. [O que mudou desde 2026-11-06](#2-o-que-mudou-desde-2026-11-06)
3. [claude-code-action com OAuth token](#3-claude-code-action-com-oauth-token)
4. [Step com claude -p](#4-step-com-claude--p)
5. [Scheduled tasks com gatilho de GitHub](#5-scheduled-tasks-com-gatilho-de-github)
6. [Cloud sessions, @claude e auto-fix](#6-cloud-sessions-claude-e-auto-fix)
7. [Code Review gerenciado](#7-code-review-gerenciado)
8. [Crédito de API do Max e do Ultra](#8-crédito-de-api-do-max-e-do-ultra)
9. [Termos de uso e a mudança de cobrança](#9-termos-de-uso-e-a-mudança-de-cobrança)
10. [Plano Pro e uma segunda conta só para a fábrica](#10-plano-pro-e-uma-segunda-conta-só-para-a-fábrica)
11. [Comparação](#11-comparação)
12. [Recomendação](#12-recomendação)
13. [Pendências](#13-pendências)
14. [Fontes](#14-fontes)

## 1. Método e níveis de confiança

Fontes primárias abertas nesta pesquisa: as páginas de GitHub Actions, scheduled tasks, cloud sessions, Code Review, autenticação, CLI reference, headless, custos, model config e legal da doc do Claude Code; a página de crédito de API e a de cost tracking do Agent SDK; os artigos de suporte sobre o Agent SDK no plano, o Claude Code no plano e o plano Pro; a página de preços; os Consumer Terms e a Usage Policy; e o repositório `anthropics/claude-code-action` (README, `action.yml`, `docs/usage.md` e o código de `base-action/src`, commit `d5f7970` de 2026-11-10, release `v1.0.271`).

- **confirmado**: doc oficial ou arquivo do repositório, aberto nesta pesquisa.
- **inferência**: leitura minha a partir das fontes, não afirmação delas.
- **não testado**: comportamento que a doc permite deduzir, mas que ninguém rodou aqui.

A busca por um `@claude` no GitHub que rode sem workflow só trouxe páginas de terceiros; nenhuma conta como fonte.

## 2. O que mudou desde 2026-11-06

- **Routines viraram scheduled tasks.** O nome antigo ainda aparece na URL e no admin; o gatilho de GitHub agora cobre issues, além de pull requests e releases ([routines](https://code.claude.com/docs/en/routines)). **Confirmado.**
- **Ultra mudou de formato.** A página de preços lista o Ultra com "No 5-hour limit" e 10 vezes o uso do Pro por semana; o Max segue com 5 vezes o Pro na janela de 5 horas e na semanal ([pricing](https://claude.com/pricing)). **Confirmado.** Para a fábrica, inferência: no Ultra a run longa não bate na janela de 5 horas, só na semanal.
- **A action segue na v1.** Releases quase diários (v1.0.267 a v1.0.271 entre 3 e 10 de novembro), sem mudança de input listada ([releases](https://github.com/anthropics/claude-code-action/releases)). **Confirmado.**
- **A mudança de cobrança continua pausada** (seção 9). **Confirmado.**

## 3. claude-code-action com OAuth token

**Funciona com a assinatura.** O secret `CLAUDE_CODE_OAUTH_TOKEN`, gerado com `claude setup-token`, vale em Pro, Max, Ultra, Team e Enterprise, e vai no input `claude_code_oauth_token`. A doc diz que, com OAuth token, as runs usam a assinatura em vez de cobrança de API ([github-actions](https://code.claude.com/docs/en/github-actions)). O token dura um ano e só faz requisições de modelo: não abre Remote Control nem busca connectors do claude.ai ([authentication](https://code.claude.com/docs/en/authentication)). **Confirmado.**

**Como conta no limite.** A run consome a mesma janela de uso da sessão interativa, mais os minutos do GitHub Actions no repo privado ([github-actions, Manage costs](https://code.claude.com/docs/en/github-actions)). **Confirmado.** A doc pede API key em vez de OAuth token quando o secret é compartilhado entre repositórios de uma organização, porque o token fica preso à assinatura de quem o gerou. **Confirmado.** Num repo de um dono só, isso não se aplica.

**Disparo por label.** Há dois modos. Sem `prompt`, a action espera o `@claude` ou o label de `label_trigger` (padrão `claude`) e responde num comentário. Com `prompt`, roda em automation mode em qualquer evento, como `issues: labeled`, e o resultado vai para o log da run. Em ambos, num evento de issue, quem disparou precisa de write access, e ator bot é recusado salvo se listado em `allowed_bots` ([github-actions](https://code.claude.com/docs/en/github-actions), [action.yml](https://github.com/anthropics/claude-code-action/blob/main/action.yml)). **Confirmado.** Para a fábrica serve o automation mode, com o `if:` do workflow conferindo o nome do label (inferência).

**Modelo e effort por tarefa.** `claude_args` aceita qualquer flag da CLI ([github-actions, Pass CLI arguments](https://code.claude.com/docs/en/github-actions)). No código, a action tira `--model` e `--max-turns` para opções próprias do SDK e repassa o resto como argumento extra da CLI ([parse-sdk-options.ts](https://github.com/anthropics/claude-code-action/blob/main/base-action/src/parse-sdk-options.ts)). **Confirmado.** Então `--model claude-opus-5-5 --effort high` vai em `claude_args`. Outra forma é a variável `CLAUDE_CODE_EFFORT_LEVEL`, que vence o `--effort` na precedência ([model-config](https://code.claude.com/docs/en/model-config)), posta no `env` do input `settings` (o `docs/usage.md` manda configurar ambiente em `settings`). **Confirmado** o mecanismo; o `--effort` repassado não foi testado. Opus 5.5 começa em `medium`, por isso o effort precisa ser fixado (já estava na seção 11.7 da nota da fábrica, reconferido).

**Teto de gasto.** A action não tem input de orçamento ([action.yml](https://github.com/anthropics/claude-code-action/blob/main/action.yml)). O `--max-budget-usd` é flag da CLI, só de print mode, e para a run quando o gasto **estimado** chega ao valor; a estimativa é local, a preço de lista, e o gasto pode passar do teto ([cli-reference](https://code.claude.com/docs/en/cli-reference)). A doc não diz que a flag exige API key. **Confirmado** o que está escrito. **Inferência, não testado:** com OAuth, a flag passa por `claude_args` como argumento extra e corta a run pela estimativa; não limita fatura nenhuma (não há fatura), mas funciona como teto de consumo por run, medido em dólar de lista. O freio real na assinatura continua sendo a janela de uso, mais `timeout-minutes` e `concurrency` do workflow, que a própria doc recomenda junto com `--max-turns`.

**Resultado para a telemetria.** O output `execution_file` aponta para `$RUNNER_TEMP/claude-execution-output.json`, que guarda a lista inteira de mensagens do SDK, inclusive a mensagem `result` ([execution-file.ts](https://github.com/anthropics/claude-code-action/blob/main/base-action/src/execution-file.ts), [run-claude-sdk.ts](https://github.com/anthropics/claude-code-action/blob/main/base-action/src/run-claude-sdk.ts)). Essa mensagem traz `total_cost_usd`, `modelUsage` por modelo, `num_turns`, `duration_ms` e o `subtype`, que vale `error_max_budget_usd` quando o teto corta a run ([cost-tracking](https://code.claude.com/docs/en/agent-sdk/cost-tracking)). Os outros outputs são `conclusion`, `session_id`, `branch_name` e `structured_output` (com `--json-schema`). **Confirmado.** Dois cuidados: o arquivo carrega a transcrição completa, então o step de telemetria extrai só os campos do `result` e não sobe o arquivo como artifact; e o custo é estimativa a preço de lista, que na assinatura só serve para comparar runs.

## 4. Step com claude -p

**Funciona com a assinatura.** `CLAUDE_CODE_OAUTH_TOKEN` é a credencial indicada para CI e scripts sem navegador ([authentication](https://code.claude.com/docs/en/authentication)), e o artigo de suporte, na atualização de 7 de outubro de 2026, diz que `claude -p` logado no plano continua tirando do limite da assinatura ([suporte](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan)). **Confirmado.**

**Controle total, sem camada no meio.** `--model`, `--effort`, `--max-turns`, `--max-budget-usd`, `--permission-mode`, `--permission-prompts none` para run sem ninguém olhando, `--output-format json` com `total_cost_usd` e `--json-schema` com `structured_output` ([headless](https://code.claude.com/docs/en/headless), [cli-reference](https://code.claude.com/docs/en/cli-reference)). **Confirmado.**

**Três armadilhas confirmadas:**

1. **API key vence o OAuth token.** Na ordem de credenciais, `ANTHROPIC_API_KEY` vem antes de `CLAUDE_CODE_OAUTH_TOKEN`, e em `-p` a key é usada sempre que existe, sem perguntar ([authentication](https://code.claude.com/docs/en/authentication)). Uma key esquecida no ambiente do runner troca a assinatura por cobrança de API em silêncio. **Confirmado.**
2. **`--bare` não lê o OAuth token.** O modo bare só aceita API key ou `apiKeyHelper` ([authentication](https://code.claude.com/docs/en/authentication), [headless](https://code.claude.com/docs/en/headless)). A doc recomenda bare para scripts e avisa que ele vai virar o padrão do `-p` numa versão futura. **Confirmado.** Inferência: na assinatura, a run não pode usar bare, o que carrega hooks, skills e `CLAUDE.md` do repo (bom para a fábrica); e, quando bare virar padrão, o step pode parar de autenticar até ganhar a forma de desligar.
3. **Sem bare, o `-p` roda o que o repo manda.** Hooks do `.claude/settings.json` e servidores do `.mcp.json` rodam sem diálogo de confiança ([headless](https://code.claude.com/docs/en/headless)). **Confirmado.** Num repo de um dono só é aceitável; o conteúdo não confiável é o texto da issue.

**O que a action faz e o step precisa montar à mão** (inferência): instalar o Claude Code, conferir quem pôs o label e se tem write access, e escolher a identidade do push. Com o `GITHUB_TOKEN` padrão, os commits não disparam a CI ([github-actions, Troubleshooting](https://code.claude.com/docs/en/github-actions)); precisa de token de app próprio.

## 5. Scheduled tasks com gatilho de GitHub

**Funciona com a assinatura, sem runner.** Scheduled tasks existem em Pro, Max, Ultra, Team e Enterprise, rodam como sessão completa do Claude Code na nuvem da Anthropic e aceitam três gatilhos: horário, chamada de API e evento de GitHub. O evento de issue cobre aberta, editada, fechada, reaberta, com label e atribuída. Exigem o app do Claude instalado no repo ([routines](https://code.claude.com/docs/en/routines)). **Confirmado.** Estão em research preview: comportamento, limites e API podem mudar.

**Como conta no limite.** Gastam a assinatura do mesmo jeito que a sessão interativa. Além disso, cada forma de iniciar tem teto por hora (100 runs agendadas por conta, 30 disparos manuais ou por API por tarefa), e eventos de GitHub têm tetos por tarefa e por conta, sem número publicado; evento acima do teto é descartado. Ao bater no limite da assinatura, a run é recusada, salvo com usage credits ligados, que cobram à parte ([routines, Usage and limits](https://code.claude.com/docs/en/routines)). **Confirmado.** Não há VM cobrada à parte nem minutos do GitHub ([claude-code-on-the-web](https://code.claude.com/docs/en/claude-code-on-the-web)).

**Modelo e effort.** Escolhidos no seletor da tarefa, valem para todas as runs dela ([routines](https://code.claude.com/docs/en/routines)). **Confirmado.** Por tarefa, sim; por issue, não. Uma tarefa para implementar e outra para revisar cobrem o desenho da seção 11.7 da nota da fábrica.

**Filtro e permissões.** Os filtros documentados (autor, labels, draft, branch) são só de pull request. **Confirmado.** Inferência: uma tarefa ligada a "issue com label" dispara em qualquer label, e o prompt precisa conferir qual foi, gastando uma sessão a cada label que não interessa. A run começa em auto mode, empurra para branch `claude/` e aparece como o usuário: commits e PRs levam a identidade de GitHub dele. **Confirmado.**

**Resultado para a telemetria.** O histórico mostra Succeeded, Failed ou Cancelled, e a doc avisa que isso diz como a sessão terminou, não se o trabalho foi feito; o detalhe está na transcrição, e `/schedule` sabe ler o log de uma run ([routines, View and interact with runs](https://code.claude.com/docs/en/routines)). **Confirmado.** A doc não mostra campo de custo, export nem webhook de fim de run. Inferência: a telemetria da fábrica fica sem custo por run; o máximo é o prompt mandar a run comentar o desfecho na issue.

## 6. Cloud sessions, @claude e auto-fix

- **Cloud session (Claude Code na web, `claude --cloud`).** Contam no limite do plano, sem cobrança da VM; usam sempre as credenciais da assinatura, mesmo com `ANTHROPIC_API_KEY` no ambiente ([claude-code-on-the-web](https://code.claude.com/docs/en/claude-code-on-the-web), [authentication](https://code.claude.com/docs/en/authentication)). **Confirmado.** Não têm gatilho de GitHub próprio: o gatilho é a scheduled task. `--cloud` exige login no claude.ai, e o token do `setup-token` só faz requisições de modelo. Inferência: um workflow não consegue abrir cloud session com o secret da fábrica; não é motor de run por label.
- **`@claude` no GitHub.** Mencionar `@claude` numa issue ou PR é o modo interativo da própria action e depende do workflow no repo ([github-actions](https://code.claude.com/docs/en/github-actions)). Não achei, em fonte primária, um `@claude` que implemente sem workflow. O `@claude review` é do Code Review (seção 7). **Confirmado** o que a doc diz; a ausência é o que a busca mostrou.
- **Auto-fix de PR.** Uma cloud session acompanha um PR e reage a falha de CI e a comentário de revisão, empurrando a correção quando ela é clara. Precisa do app do Claude no repo, liga-se pela sessão, pelo `/autofix-pr` ou pelo app, e responde no GitHub pela conta do usuário, marcada como Claude Code ([claude-code-on-the-web, Auto-fix](https://code.claude.com/docs/en/claude-code-on-the-web)). **Confirmado.** Inferência: é a peça natural da rodada de retrabalho depois que a run abre o PR, ligada à mão por PR; não substitui o motor.

## 7. Code Review gerenciado

Só para Team e Enterprise, ligado por um Owner da organização, rodando na infraestrutura da Anthropic; lê o diff sem rodar o código, não empurra commit, não aprova nem bloqueia, e escolhe o modelo sozinho, com níveis Quick, Standard e Deep ([code-review](https://code.claude.com/docs/en/code-review)). **Confirmado.** Fica fora para um dono só no Max ou no Ultra. As alternativas que a própria página lista para qualquer plano são o `/code-review` local e a revisão na própria CI, que é a `code-review` rodando pela action.

## 8. Crédito de API do Max e do Ultra

**O que é.** Max recebe US$ 100 e Ultra US$ 200 por mês numa organização do Console vinculada; o crédito cobre Claude API, Managed Agents, Agent SDK e playground, e não cobre Claude Code nem uso extra nos apps; expira no fim do ciclo, sem acumular; dispensa cartão no Console ([api-credits](https://platform.claude.com/docs/en/about-claude/api-credits-for-subscribers)). O artigo de suporte detalha que o crédito vale para o Agent SDK e o `claude -p` rodados com API key da organização vinculada ([suporte](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan)). **Confirmado.** A tabela diz "Claude Code: não" e o suporte diz "`claude -p` com API key: sim"; leio que o "não" é o Claude Code logado na assinatura (inferência).

**A action com API key da organização vinculada** roda sobre o Agent SDK ([github-actions](https://code.claude.com/docs/en/github-actions)), então a run deve sair do crédito. **Inferência**, nenhuma das duas páginas cita a action pelo nome.

**"API sem custo extra" vale, com um freio melhor que o da assinatura.** Quando o crédito acaba e não há crédito comprado, as requisições param até o mês seguinte e nada é cobrado do plano; com auto-reload ou crédito comprado, seguem cobrando. Todas as keys da organização dividem o saldo, e um workspace próprio com spend limit põe teto por projeto ([api-credits](https://platform.claude.com/docs/en/about-claude/api-credits-for-subscribers)). **Confirmado.** Aqui o `--max-budget-usd` mede dinheiro de verdade, só que pela estimativa local.

**Diferenças práticas.** Com API key o cache dura 5 minutos por padrão; na assinatura, dentro do uso incluso, as próprias turns ganham 1 hora sem configurar nada, e `ENABLE_PROMPT_CACHING_1H` pede 1 hora com API key, a um preço de escrita maior ([cost-tracking](https://code.claude.com/docs/en/agent-sdk/cost-tracking)). Com API key não há janela de uso, só rate limit, e a organização vinculada sobe pelo menos para o tier Start ([api-credits](https://platform.claude.com/docs/en/about-claude/api-credits-for-subscribers)). **Confirmado.**

**Quanto cabe.** No cenário da seção 7.4 da nota da fábrica (cerca de US$ 4 por tarefa com Opus 5.5, antes de retrabalho), o crédito do Max paga umas 25 tarefas por mês e o do Ultra umas 50. **Inferência**, sobre premissas que o piloto precisa medir.

**Termos.** O uso com API key cai nos Commercial Terms, e o crédito tem termos de programa próprios, aceitos ao vincular ([legal](https://code.claude.com/docs/en/legal-and-compliance), [api-credits](https://platform.claude.com/docs/en/about-claude/api-credits-for-subscribers)). **Confirmado.** Não li os termos do programa de crédito; fica como pendência.

## 9. Termos de uso e a mudança de cobrança

- **Uso individual no próprio repo.** Reconferido em 2026-11-11, sem mudança: os limites de Pro, Max e Ultra pressupõem "ordinary, individual usage of Claude Code and the Agent SDK"; o OAuth é para o uso comum do Claude Code e dos apps nativos; rotear requisições de terceiros pela credencial da assinatura é proibido, e a Anthropic pode agir sem aviso ([legal](https://code.claude.com/docs/en/legal-and-compliance)). A doc documenta a assinatura na action e nas scheduled tasks. **Confirmado.** A leitura da seção 7.3 da nota da fábrica continua de pé: a própria fábrica, nos próprios repos, com a própria assinatura, é uso previsto; o que preocupa é volume contínuo, não o motor.
- **A mudança de junho.** O artigo de suporte registra a pausa em 15 de junho de 2026 ("nothing has changed" por enquanto) e uma atualização em 7 de outubro: logado no plano, Agent SDK e `claude -p` continuam no limite da assinatura, e Max, Ultra e Team ganharam o crédito mensal de API, separado dos limites ([suporte](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan)). Não há data de retomada. **Confirmado**, mesmo status de 2026-11-06. O artigo atual não cita GitHub Actions; a página da action continua dizendo que, com OAuth, a run usa a assinatura.
- **Inferência sobre o risco.** Se a mudança voltar no formato anunciado em maio, a action com OAuth e o `claude -p` saem do limite da assinatura juntos; o crédito de API é o que já existe de pista separada. Por isso vale deixar a troca de credencial a um secret de distância.

## 10. Plano Pro e uma segunda conta só para a fábrica

### 10.1 O que vale no Pro

- **Vale:** o `claude_code_oauth_token` da action e o `CLAUDE_CODE_OAUTH_TOKEN` do `claude -p` (Pro está na lista de planos do `setup-token`), as scheduled tasks com gatilho de GitHub, as cloud sessions e o auto-fix ([authentication](https://code.claude.com/docs/en/authentication), [routines](https://code.claude.com/docs/en/routines), [claude-code-on-the-web](https://code.claude.com/docs/en/claude-code-on-the-web)). O modelo padrão no Pro também é o Opus 5.5 ([model-config](https://code.claude.com/docs/en/model-config)). **Confirmado.**
- **Não vale:** o crédito mensal de API, que é só de Max, Ultra e Team; Free, Pro e Enterprise não são elegíveis ([api-credits](https://platform.claude.com/docs/en/about-claude/api-credits-for-subscribers)). A seção 8 inteira não se aplica ao Pro. O Code Review gerenciado também não (seção 7). **Confirmado.**
- **O limite é o menor dos pagos.** O Pro tem janela de 5 horas e janela semanal, compartilhadas entre o Claude e o Claude Code; o Max tem 5 vezes isso ([pricing](https://claude.com/pricing), [suporte, Claude Code no plano](https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan), [suporte, plano Pro](https://support.claude.com/en/articles/8325606-what-is-the-pro-plan)). A Anthropic pode impor outros tetos por modelo ou recurso. **Confirmado.** Inferência: uma run de implementação com Opus 5.5 em effort `high` pode comer uma fatia grande da janela de 5 horas do Pro; o piloto precisa medir com `/usage` antes de ligar mais de uma run por vez.
- **O que fazer quando o limite acaba, no Pro.** Ligar usage credits, que cobram à parte para continuar depois do limite (inclusive nas scheduled tasks), ou comprar crédito no Console e rodar com API key, a preço de API ([suporte, Claude Code no plano](https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan), [routines, Usage and limits](https://code.claude.com/docs/en/routines)). **Confirmado.** No Pro, "API sem custo extra" não existe: a segunda pista sempre custa.

### 10.2 Uma segunda conta Pro dedicada à fábrica

A pergunta: o dono tem duas contas Pro pessoais e quer usar o token do `setup-token` da segunda só no secret do repo, para não gastar o limite da conta de uso interativo.

**O que os textos dizem. Confirmado:**

- **Termos de consumidor** (vigentes desde 8 de outubro de 2025, valem para Free, Pro, Max e Ultra): proíbem compartilhar credenciais da conta ou deixá-la disponível para outra pessoa (seção 2); proíbem abusar ou atrapalhar os serviços, "including by bypassing any of our systems or protective measures" (seção 3); e proíbem acesso automatizado "through a bot, script, or otherwise", com exceção para acesso por API key "or where we otherwise explicitly permit it" (seção 3). Não há cláusula sobre quantas contas uma pessoa pode ter nem sobre limite de uso ([consumer terms](https://www.anthropic.com/legal/consumer-terms)).
- **Usage Policy** (versão vigente a partir de 12 de novembro de 2026): proíbe criar várias contas para evitar detecção ou coordenar atividade maliciosa entre elas, contornar banimento com outra conta e burlar "capabilities, restrictions, or guardrails" dos produtos, inclusive contornando o cadastro ou o login. Não fala em limite de uso ([aup](https://www.anthropic.com/legal/aup)).
- **Legal do Claude Code:** os limites anunciados de Pro, Max e Ultra "assume ordinary, individual usage of Claude Code and the Agent SDK"; o OAuth é para quem compra o plano, para uso comum do Claude Code; a Anthropic pode agir sem aviso ([legal](https://code.claude.com/docs/en/legal-and-compliance)).
- **Permissão explícita de automação:** a doc documenta o OAuth token na action e o `setup-token` "for CI pipelines, scripts" ([github-actions](https://code.claude.com/docs/en/github-actions), [authentication](https://code.claude.com/docs/en/authentication)).
- **Suporte:** os limites e o horário de reset semanal são da conta; não achei artigo sobre uma pessoa com várias contas individuais ([suporte, plano Pro](https://support.claude.com/en/articles/8325606-what-is-the-pro-plan)).

**Leitura. Inferência:**

- **O que está claramente do lado permitido:** a conta é do próprio dono, paga por ele, usada só por ele, nos repositórios dele; o token não é compartilhado com ninguém. A automação na CI entra na exceção "where we otherwise explicitly permit it", porque a doc oficial ensina exatamente esse uso.
- **Onde fica cinzento:** o motivo declarado é não gastar o limite da outra conta. O limite de uso é, com boa chance, um dos "protective measures" da seção 3 e uma das "restrictions" da Usage Policy. Ter uma segunda assinatura paga não é o mesmo que burlar o limite de uma conta, mas também não é o caminho que a Anthropic oferece para ter mais uso: esse caminho é o Max, os usage credits ou a API. Somam-se duas coisas: a conta da fábrica só rodaria automação, o que se afasta de "ordinary, individual usage", e o limite pressupõe esse uso conta a conta.
- **O risco prático:** a ação da Anthropic pode vir sem aviso, e se as duas contas forem vistas como uma pessoa contornando limite, a medida pode alcançar as duas, inclusive a de uso interativo.
- **Conclusão:** não há regra que proíba de forma expressa, nem regra que permita. Não dá para chamar de "dentro dos termos" com a confiança de quem lê a cláusula; dá para chamar de risco baixo a moderado, que cresce com o volume.

**O que tira a ambiguidade, em ordem de custo** (inferência sobre os preços da [pricing](https://claude.com/pricing)):

1. Ficar numa conta só e medir: se a fábrica roda poucas tarefas por semana, talvez caiba no Pro.
2. Ligar usage credits na conta principal, com spend limit mensal, pagando só o que passar do limite.
3. Subir a conta principal para Max (US$ 100): 5 vezes o limite e US$ 100 por mês de crédito de API, que a seção 8 transforma em pista separada para a fábrica.
4. Crédito comprado no Console, num workspace só da fábrica, com spend limit: uso nos Commercial Terms, sem pergunta sobre conta.
5. Perguntar ao suporte da Anthropic se uma segunda conta Pro dedicada à automação do próprio repo é aceitável e guardar a resposta por escrito.

Se o dono decidir usar a segunda conta mesmo assim: conta paga por ele e usada só por ele, token em secret de repo privado, sem compartilhar, volume moderado, e a conta principal sem depender dela.

## 11. Comparação

| Opção | Assinatura e termos | Como conta | Modelo e effort por tarefa | Teto de gasto | Custo e desfecho para a telemetria |
| :- | :- | :- | :- | :- | :- |
| `claude-code-action@v1` com `claude_code_oauth_token` | sim, documentado; uso individual | janela de uso da assinatura, mais minutos do Actions no repo privado | sim: `claude_args` com `--model` e `--effort`, ou `CLAUDE_CODE_EFFORT_LEVEL` em `settings` | `--max-budget-usd` via `claude_args` (estimativa, não testado), `--max-turns`, `timeout-minutes` | sim: `execution_file` com `total_cost_usd`, `modelUsage`, turnos, duração, `subtype`; `conclusion` |
| Step com `claude -p` e `CLAUDE_CODE_OAUTH_TOKEN` | sim, documentado; sem `--bare`; nenhuma `ANTHROPIC_API_KEY` no ambiente | janela de uso, mais minutos | sim, flags diretas | `--max-budget-usd`, `--max-turns` (estimativa) | sim: `--output-format json` com os mesmos campos |
| Scheduled task com gatilho de issue | sim, documentado; research preview | janela de uso; tetos por hora; eventos acima do teto descartados | por tarefa, no seletor; não por issue | nenhum documentado além da janela de uso | só Succeeded, Failed ou Cancelled e a transcrição; sem custo |
| Cloud session e auto-fix | sim; exige login no claude.ai | janela de uso, sem cobrança de VM | `/model` e `/effort` na sessão | nenhum | transcrição; sem export |
| `@claude` pelo app do GitHub | é a própria action, com workflow | igual à action | igual à action | igual à action | igual à action |
| Code Review gerenciado | não: só Team e Enterprise | n/a | não escolhe modelo | spend limit da organização | check run e comentários |
| Action ou `claude -p` com API key da organização vinculada | só Max e Ultra (o Pro não tem crédito incluso); Commercial Terms e termos do crédito | crédito de US$ 100 (Max) ou 200 (Ultra) por mês; depois para, salvo crédito comprado | sim | spend limit do workspace (real) e `--max-budget-usd` | sim, e o custo é dinheiro de verdade (estimado) |
| Pro: usage credits ou crédito comprado no Console | sim; pago à parte | usage credits depois do limite, ou preço de API | sim | spend limit mensal dos usage credits, ou do workspace | como a action ou o `claude -p` |
| Segunda conta Pro só para a fábrica | sem proibição expressa nem permissão; zona cinzenta (seção 10.2) | janela de uso da segunda conta | sim | igual à action | igual à action |

## 11. Recomendação

Para a fábrica num repo privado de um dono só, rodando com a assinatura Pro:

1. **Motor: `anthropics/claude-code-action@v1` com `claude_code_oauth_token`**, em automation mode, disparado por `issues: labeled` com o `if:` conferindo `agent:implement`. Fixar a action num SHA ou tag, porque sai release quase todo dia. `claude_args` com `--model claude-opus-5-5 --effort high` (ou `low` para triagem e docs), `--max-turns` e `--max-budget-usd` como teto de consumo por run, lidos do `.factory/config.yml`. `timeout-minutes` e `concurrency` por issue no workflow. Motivos: é o caminho documentado, o gate de write access e o de bot já vêm prontos, o push sai como o app e dispara a CI, e o `execution_file` alimenta o perfil `file` da `factory-telemetry` sem mais nada.
2. **Telemetria:** um step depois da action lê só a mensagem `result` do `execution_file` e grava uma linha JSONL com issue, tarefa, modelo, effort, `total_cost_usd`, `num_turns`, `duration_ms`, `subtype` e `conclusion`. Nunca subir o arquivo inteiro.
3. **Plano B no mesmo workflow: step com `claude -p`**, para o perfil `local` ou `vps` ou se a action atrapalhar. Sem `--bare`, sem `ANTHROPIC_API_KEY` no ambiente, com token de app para o push.
4. **Segunda pista, no Pro: paga.** O Pro não tem crédito de API, então a pista separada custa: usage credits com spend limit mensal na conta principal, ou crédito comprado no Console num workspace só da fábrica com spend limit. Trocar `claude_code_oauth_token` por `anthropic_api_key` é uma linha, e serve também de saída pronta se a mudança de cobrança voltar. Se o piloto mostrar que a fábrica disputa o limite com o trabalho interativo, o Max (US$ 100) é a troca que resolve as duas coisas: 5 vezes o limite e US$ 100 por mês de crédito de API para a fábrica, sem custo extra.
5. **Segunda conta Pro: não como padrão.** Não há proibição expressa, mas o motivo (não gastar o limite da outra conta) bate na cláusula de não contornar "protective measures", e a medida da Anthropic pode alcançar as duas contas (seção 10.2). Se for usada, só depois de medir o consumo numa conta e, de preferência, com resposta do suporte por escrito.
6. **Scheduled tasks ficam na `factory-triage`**, para relógio e `/fire`, como já previa a seção 11.3 da nota da fábrica, e não como motor de implementação: sem custo por run, sem filtro de label em issue, research preview. Reavaliar quando a doc publicar custo e filtros de issue.
7. **Fora:** Code Review gerenciado (plano). Auto-fix de PR é opcional, ligado à mão para a rodada de retrabalho.

## 12. Pendências

1. Rodar uma vez a action com OAuth e `--max-budget-usd` baixo e confirmar que a run termina com `subtype` `error_max_budget_usd`.
2. Confirmar que `--effort` em `claude_args` chega à CLI (o `system/init` do `execution_file` mostra o modelo; conferir o effort no log).
3. Confirmar que a action com API key da organização vinculada sai do crédito, olhando o Billing do Console depois de uma run.
4. Ler os termos do programa de crédito (`anthropic.com/legal/credit-terms`).
5. Acompanhar o artigo de suporte da mudança de cobrança e a página de scheduled tasks (custo por run e filtros de issue).
6. Medir no Pro quanto da janela de 5 horas e da semanal uma run de implementação consome.
7. Se a segunda conta Pro continuar na mesa, perguntar ao suporte da Anthropic e registrar a resposta.

## 13. Fontes

Doc oficial do Claude Code (abertas em 2026-11-11):

- GitHub Actions: https://code.claude.com/docs/en/github-actions
- Scheduled tasks (ex routines): https://code.claude.com/docs/en/routines
- Cloud sessions e auto-fix: https://code.claude.com/docs/en/claude-code-on-the-web
- Code Review: https://code.claude.com/docs/en/code-review
- Autenticação e `setup-token`: https://code.claude.com/docs/en/authentication
- CLI reference: https://code.claude.com/docs/en/cli-reference
- Headless (`claude -p`): https://code.claude.com/docs/en/headless
- Custos: https://code.claude.com/docs/en/costs
- Model config e effort: https://code.claude.com/docs/en/model-config
- Legal and compliance: https://code.claude.com/docs/en/legal-and-compliance
- Cost tracking do Agent SDK: https://code.claude.com/docs/en/agent-sdk/cost-tracking

Plataforma, suporte e preços:

- API credits for subscribers: https://platform.claude.com/docs/en/about-claude/api-credits-for-subscribers
- Agent SDK no plano (pausa de junho e atualização de outubro): https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan
- Preços: https://claude.com/pricing
- Claude Code no plano Pro, Max ou Ultra: https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan
- O que é o plano Pro: https://support.claude.com/en/articles/8325606-what-is-the-pro-plan

Termos:

- Consumer Terms (vigentes desde 2025-10-08): https://www.anthropic.com/legal/consumer-terms
- Usage Policy (versão vigente a partir de 2026-11-12): https://www.anthropic.com/legal/aup

Repositório `anthropics/claude-code-action` (commit `d5f7970`, release `v1.0.271`):

- action.yml: https://github.com/anthropics/claude-code-action/blob/main/action.yml
- README: https://github.com/anthropics/claude-code-action/blob/main/README.md
- docs/usage.md: https://github.com/anthropics/claude-code-action/blob/main/docs/usage.md
- base-action/src/execution-file.ts: https://github.com/anthropics/claude-code-action/blob/main/base-action/src/execution-file.ts
- base-action/src/run-claude-sdk.ts: https://github.com/anthropics/claude-code-action/blob/main/base-action/src/run-claude-sdk.ts
- base-action/src/parse-sdk-options.ts: https://github.com/anthropics/claude-code-action/blob/main/base-action/src/parse-sdk-options.ts
- Releases: https://github.com/anthropics/claude-code-action/releases
