# Limite de uso numa run da fábrica sem ninguém olhando

Resumo: `autoContinueAtUsageLimit` não vale numa run da fábrica. A doc diz que o Claude Code não oferece a espera em runs `-p` nem em sessões em background; a continuação automática é coisa da sessão interativa aberta. O que serve à fábrica é outra chave, a variável `CLAUDE_CODE_RETRY_WATCHDOG=1`, feita para sessões sem ninguém olhando (CI, workers remotos): com ela, o pedido que bate no limite de sessão ou semanal da assinatura espera o reset e segue, dentro da mesma run. Sem ela, a run termina com erro, código de saída diferente de zero e um `result` de erro; o `claude-code-action` devolve `conclusion: failure`. A espera tem que caber no tempo do job (6 horas no runner do GitHub), então o desenho fica em dois degraus: watchdog com teto de espera menor que o timeout do job, e o plano B do `agent:blocked` com re-enfileiramento por relógio para o que passar do teto, como o limite semanal. Com API key não há janela de assinatura: há rate limit por minuto, que o Claude Code já repete sozinho, e o teto mensal de gasto, que nenhum retry resolve.

Pesquisa de 2026-11-10, ticket [#106](https://github.com/eusouosalmo/skills/issues/106), mapa [#103](https://github.com/eusouosalmo/skills/issues/103). Fecha a pendência 4 da seção 11.9 e corrige a seção 11.8 de [fabrica-de-software.md](fabrica-de-software.md). Nada foi rodado até bater no limite: tudo vem da doc e do código, e o formato exato da saída no limite fica para o piloto.

## Sumário

1. [Método](#1-método)
2. [autoContinueAtUsageLimit numa run headless](#2-autocontinueatusagelimit-numa-run-headless)
3. [O que a run devolve quando bate no limite](#3-o-que-a-run-devolve-quando-bate-no-limite)
4. [Esperar dentro da run: o watchdog](#4-esperar-dentro-da-run-o-watchdog)
5. [Na claude-code-action](#5-na-claude-code-action)
6. [Plano B: agent:blocked e relógio](#6-plano-b-agentblocked-e-relógio)
7. [Com API key](#7-com-api-key)
8. [O que muda no desenho](#8-o-que-muda-no-desenho)
9. [Lacunas](#9-lacunas)
10. [Fontes](#10-fontes)

## 1. Método

Fontes primárias: a doc do Claude Code (modo interativo, referência de settings, variáveis de ambiente, erros, headless, tipos do Agent SDK em TypeScript, CLI), o `action.yml` do `anthropics/claude-code-action` no commit `d5f7970` (main em 2026-11-10), a doc da API (rate limits, SDK Python), a central de ajuda da Anthropic para a janela da assinatura e a doc do GitHub Actions para o gatilho por relógio. Cada afirmação leva o nível: **Confirmado** (está escrito na fonte), **Inferência** (dedução minha a partir do que está escrito).

## 2. autoContinueAtUsageLimit numa run headless

- A chave existe, vem `true` por padrão, exige v2.1.234 ou mais nova e só é lida das configurações de usuário, de `--settings` e das gerenciadas; se só um arquivo de projeto ou local a define, ela desliga em vez de ser ignorada ([settings reference](https://code.claude.com/docs/en/settings-reference#autocontinueatusagelimit)). **Confirmado.**
- A doc descreve a continuação automática como ligada "in interactive sessions signed in with a claude.ai subscription", e lista os casos em que o Claude Code não oferece a espera de jeito nenhum: sessões em background e runs `-p` ("the menu row isn't available"); API key, provedores de nuvem e cobrança por uso, porque ali não há reset para esperar ([interactive mode, wait for a usage limit to reset](https://code.claude.com/docs/en/interactive-mode#wait-for-a-usage-limit-to-reset)). **Confirmado.**
- Mesmo na sessão interativa, a continuação para depois de três retomadas seguidas e não começa sozinha quando o reset está a mais de 24 horas, o caso típico do limite semanal. **Confirmado.**
- Em `-p`, a doc só cita a chave para desligá-la (`/config autoContinueAtUsageLimit=false` funciona com `-p`). **Confirmado.**

Conclusão: a chave não resolve a fábrica, nem em `claude -p` direto nem na action, que roda o Claude Code em modo não interativo. **Inferência** forte, apoiada na lista acima.

## 3. O que a run devolve quando bate no limite

Sem watchdog (seção 4), a run não espera:

- As mensagens do limite da assinatura são `You've hit your session limit · resets <hora>`, e as variantes semanal, Opus e Sonnet. O Claude Code bloqueia novos pedidos até a hora do reset. Os limites de sessão e semanal valem para todos os modelos; os de Opus e de Sonnet valem só para a família, então trocar de modelo contorna esses dois ([errors, session limit](https://code.claude.com/docs/en/errors#youve-hit-your-session-limit)). **Confirmado.**
- A janela de sessão dura cinco horas a partir da primeira mensagem; a semanal reseta num horário fixo por conta; Claude Code, claude.ai e Desktop contam contra o mesmo limite ([central de ajuda](https://support.claude.com/en/articles/11647753-usage-and-length-limits)). **Confirmado.** Consequência: uma run da fábrica e o uso pessoal do dono disputam a mesma janela (**Inferência**).
- `claude -p` sai com código zero no sucesso e diferente de zero quando a run falha; falha de dentro da run sai como `result` no stdout ([headless](https://code.claude.com/docs/en/headless)). **Confirmado.**
- Em `--output-format stream-json`, o Claude Code emite um `rate_limit_event` com `status` (`allowed`, `allowed_warning` ou `rejected`) e `resetsAt`; a mensagem do assistente que falhou carrega `error: "rate_limit"` (429 contra a cota, separado de `overloaded`, que é 529); o `result` final tem `is_error` e `api_error_status`, e `terminal_reason` pode ser `api_error` ([Agent SDK TypeScript](https://code.claude.com/docs/en/agent-sdk/typescript)). **Confirmado** que os campos existem. Que exatamente essa combinação apareça no limite da assinatura é **Inferência**: a doc não mostra um exemplo de run `-p` batendo no limite.
- Com `credits_required` no `rate_limit_event`, a assinatura esgotou o incluído e a sessão só segue comprando usage credits. **Confirmado.**
- Antes de esgotar, o Claude Code avisa com `You've used 85% of your session limit` e o evento vem com `allowed_warning` ([errors](https://code.claude.com/docs/en/errors#youve-hit-your-session-limit), [Agent SDK TypeScript](https://code.claude.com/docs/en/agent-sdk/typescript)). **Confirmado.**

Quanto ela espera sem watchdog: nada além das retentativas normais (até 10, com backoff exponencial) para 429 que o Claude Code trata como transitório ([errors, automatic retries](https://code.claude.com/docs/en/errors#automatic-retries)). O limite da assinatura não é transitório, então a run termina. **Inferência** a partir da distinção que a doc faz entre o throttle sem cabeçalhos de cota e o limite real.

## 4. Esperar dentro da run: o watchdog

A doc tem um mecanismo próprio para sessões sem ninguém olhando, que o rascunho da seção 11.8 não conhecia ([env vars](https://code.claude.com/docs/en/env-vars), [errors, tune retry behavior](https://code.claude.com/docs/en/errors#tune-retry-behavior)). **Confirmado** tudo o que segue:

- `CLAUDE_CODE_RETRY_WATCHDOG=1` é indicada "for unattended sessions such as eval harnesses, CI jobs, or remote workers". Repete 429 e 529 sem limite de tentativas, com backoff de até 5 minutos entre elas, "or until the limit resets when the response carries a rate-limit reset time, so a session that hits a usage limit waits out the remaining window". Também sobe para 300 as retentativas de erro de servidor, timeout e conexão caída, cerca de três horas de backoff. Exige v2.1.186 ou mais nova.
- Não espera quando o 429 é teto de gasto ou usage credits esgotados: falha na hora (desde v2.1.239).
- `CLAUDE_CODE_RETRY_WATCHDOG_MAX_USAGE_LIMIT_WAIT_MS`: maior espera de um pedido pelo reset do limite da assinatura. Se o reset está mais longe que o teto, o pedido falha na hora. Sem teto por padrão. Exige v2.1.301.
- `CLAUDE_CODE_RETRY_WATCHDOG_MAX_WAIT_MS`: teto de espera por 429 e 529 em geral, por pedido. Sem teto por padrão. Exige v2.1.295.
- `CLAUDE_CODE_RETRY_WATCHDOG_USAGE_LIMIT_RECHECK_MS`: intervalo mínimo, de 1 minuto a 3 horas, entre checagens de que o limite já caiu antes da hora, para sair da espera mais cedo. Só vale para limite de sessão ou semanal da assinatura sem usage credits, e não com `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`. Exige v2.1.305.
- Cada retentativa aparece no stream como `system/api_retry`, com `attempt`, `retry_delay_ms`, `error_status` e `error: "rate_limit"` ([headless](https://code.claude.com/docs/en/headless#handle-api-retries)). Serve para a telemetria registrar quanto da run foi espera.

Leitura para a fábrica (**Inferência**):

- A espera acontece dentro do pedido, então a run continua de onde parou, com contexto e cache, sem reler a issue. É melhor que re-enfileirar, quando cabe no tempo.
- O tempo de espera conta no relógio do job. No runner do GitHub o job morre em 6 horas ([limits](https://docs.github.com/en/actions/reference/limits)); a janela de sessão chega a 5 horas. Uma run que bate no limite cedo pode esperar quase tudo e morrer sem terminar. Por isso o teto `MAX_USAGE_LIMIT_WAIT_MS` deve ficar abaixo do que sobra do `timeout-minutes` do job, com folga para terminar a tarefa.
- O limite semanal pode estar a dias. Sem teto, o watchdog prende o runner até lá; no self-hosted o job aguenta 5 dias. Com teto, falha rápido e cai no plano B.
- Se a conta tem usage credits ligados, a run pode seguir gastando crédito em vez de esperar, e o watchdog falha na hora quando o crédito acaba. Para a fábrica, deixar os créditos desligados ou com teto, e decidir isso de propósito.

## 5. Na claude-code-action

- A action aceita `claude_code_oauth_token` (assinatura) ou `anthropic_api_key`, um `settings` em JSON ou caminho de arquivo, e `claude_args`; devolve `conclusion` (`success` ou `failure`), `execution_file` e `session_id` ([action.yml](https://github.com/anthropics/claude-code-action/blob/main/action.yml)). **Confirmado.**
- O `action.yml` não passa `CLAUDE_CODE_RETRY_WATCHDOG` adiante e não fala de limite de uso. Um comentário no próprio arquivo diz que o bloco `env` do passo que roda o Claude Code esconde as variáveis do `env` do job, e por isso as de MCP e OpenTelemetry estão listadas uma a uma. **Confirmado** o comentário; se o watchdog posto no `env` do job chega ao Claude Code não está verificado.
- Caminho que não depende disso: a chave `env` das configurações do Claude Code aplica variáveis à sessão, e quando vem de `--settings` vale desde a inicialização; o watchdog não está na lista de variáveis que arquivos de projeto não podem definir ([settings reference, env](https://code.claude.com/docs/en/settings-reference#env)). **Confirmado.** Então `settings: '{"env":{"CLAUDE_CODE_RETRY_WATCHDOG":"1","CLAUDE_CODE_RETRY_WATCHDOG_MAX_USAGE_LIMIT_WAIT_MS":"..."}}'` na action, ou o mesmo `env` no `.claude/settings.json` do repo, deve funcionar. **Inferência**, a testar no piloto.
- A doc de GitHub Actions do Claude Code só recomenda timeout no workflow para evitar job sem fim ([github-actions](https://code.claude.com/docs/en/github-actions)). **Confirmado.**

## 6. Plano B: agent:blocked e relógio

Para o que o watchdog não cobre (limite semanal, reset além do teto, créditos esgotados), o plano B da seção 11.8 se mantém, agora com o sinal certo para disparar:

1. A run termina com `conclusion: failure` (action) ou código diferente de zero (`-p`). O passo seguinte do workflow, com `if: failure()`, lê o `execution_file` ou o stream e procura `rate_limit` no `error` do assistente, `rate_limit_event` com `rejected` ou o texto `You've hit your`. **Inferência** sobre o que procurar; os campos são **Confirmados** na seção 3.
2. Se achou, põe `agent:blocked` e comenta na issue o motivo e a hora do reset, tirada do `resetsAt` ou do texto da mensagem. Erro de outro tipo segue o caminho normal de falha, que conta tentativa.
3. Um workflow com `schedule` lista as issues `agent:blocked` por limite de uso cuja hora de reset já passou e devolve o label `agent:implement`. O `schedule` roda no mínimo a cada 5 minutos, só no branch padrão, pode atrasar em hora de carga, e num repo público é desligado depois de 60 dias sem atividade ([events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)). **Confirmado.** Um atraso de alguns minutos não importa aqui.
4. A tentativa bloqueada por limite não deve contar no teto de tentativas da issue: não é falha da tarefa. **Inferência**, decisão de desenho.
5. A run nova começa do zero; o branch da run anterior fica, e o prompt pode mandar continuar dele. Retomar a sessão com `--resume` exigiria guardar a transcrição entre jobs. **Inferência.**

## 7. Com API key

- Não há janela de assinatura. Há rate limit por minuto (RPM, ITPM, OTPM) por modelo e por tier, medido por token bucket que repõe contínuo, e o 429 vem com `retry-after` ([rate limits](https://platform.claude.com/docs/en/api/rate-limits)). Tokens lidos do cache não contam no ITPM. **Confirmado.**
- O Claude Code repete 429 transitório até 10 vezes com backoff, ou sem limite com o watchdog ([errors, automatic retries](https://code.claude.com/docs/en/errors#automatic-retries)). Os SDKs de cliente, que a fábrica não usa diretamente, repetem 429 duas vezes por padrão (`max_retries`) ([SDK Python](https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/python#retries)). **Confirmado.** A frase "o SDK já trata com retry" da seção 11.8 vale, mas quem trata na fábrica é o próprio Claude Code.
- O teto mensal de gasto do tier (Start US$ 500, Build US$ 1.000, Scale US$ 200.000) devolve 429 `rate_limit_error` com `error_code: enforced_spend_limit_reached`, sem `retry-after`, até 00:00 UTC do dia 1º do mês seguinte; o retry do SDK falha até lá. O teto que você mesmo define devolve 400 `invalid_request_error`. **Confirmado.** O watchdog falha na hora nesses casos (seção 4), então o plano B vale para API key também, com reset no mês seguinte.
- O workspace do Claude Code tem limite checado à parte, que pode devolver 429 com `retry-after`. **Confirmado.**
- Com API key também há `--max-budget-usd` por run (só em modo `-p`), que corta a run pelo custo estimado do lado do cliente ([CLI](https://code.claude.com/docs/en/cli-reference)). **Confirmado.**

| | Assinatura (OAuth) | API key |
| :- | :- | :- |
| O que esgota | janela de 5 horas, semanal, por família de modelo | RPM, ITPM, OTPM por minuto; teto mensal de gasto |
| Espera sozinha em `-p` sem configurar | não | sim, até 10 retentativas de 429 transitório |
| Com `CLAUDE_CODE_RETRY_WATCHDOG=1` | espera o reset dentro da run, com teto opcional | repete 429 e 529 sem limite; falha na hora no teto de gasto |
| Quando cai no plano B | semanal, reset além do teto, créditos esgotados | teto mensal de gasto |

## 8. O que muda no desenho

Para a `factory-install` e a seção 11.8 da nota da fábrica (**Inferência**, decisões a confirmar com o usuário):

1. Trocar a premissa: `autoContinueAtUsageLimit` sai do desenho; entra `CLAUDE_CODE_RETRY_WATCHDOG=1` em toda run, posto pelo `settings` da action.
2. `CLAUDE_CODE_RETRY_WATCHDOG_MAX_USAGE_LIMIT_WAIT_MS` derivado do `timeout-minutes` do job, com folga para a tarefa terminar; `RECHECK_MS` em algo como 10 minutos para não esperar à toa. Os dois no `.factory/config.yml`.
3. Passo `if: failure()` que separa limite de uso de falha da tarefa e aplica `agent:blocked` com a hora do reset; workflow `schedule` que re-enfileira depois dela. A tentativa por limite não conta no teto.
4. Fixar a versão mínima do Claude Code em v2.1.305 para ter as quatro variáveis do watchdog.
5. Concorrência: duas runs simultâneas dividem a mesma janela, e a do dono também. Limitar a uma run por vez na assinatura é o padrão mais seguro.
6. A telemetria (`factory-telemetry`) registra os `api_retry` de `rate_limit` para medir quanto da run foi espera.

## 9. Lacunas

- O formato exato da saída de `-p` e do `execution_file` quando a assinatura esgota: a doc lista os campos, não mostra a run. Medir no piloto, sem forçar o limite de propósito: guardar a saída da primeira vez que acontecer.
- Se o watchdog no `env` do job chega ao Claude Code dentro da action, dado o comentário do `action.yml`. O caminho pelo `settings` evita a dúvida.
- Se o watchdog espera também o limite semanal quando o reset está a dias e não há teto. A doc diz que espera "the remaining window" sem distinguir; com o teto definido, a dúvida não importa.
- Se o `resetsAt` é em segundos ou milissegundos: a doc tipa como `number` sem unidade.

## 10. Fontes

- Claude Code, [Wait for a usage limit to reset](https://code.claude.com/docs/en/interactive-mode#wait-for-a-usage-limit-to-reset)
- Claude Code, [settings reference: autoContinueAtUsageLimit e env](https://code.claude.com/docs/en/settings-reference)
- Claude Code, [environment variables](https://code.claude.com/docs/en/env-vars)
- Claude Code, [errors: automatic retries, tune retry behavior, usage limits](https://code.claude.com/docs/en/errors)
- Claude Code, [run Claude Code programmatically (headless)](https://code.claude.com/docs/en/headless)
- Claude Code, [Agent SDK TypeScript reference](https://code.claude.com/docs/en/agent-sdk/typescript)
- Claude Code, [CLI reference](https://code.claude.com/docs/en/cli-reference)
- Claude Code, [GitHub Actions](https://code.claude.com/docs/en/github-actions)
- [anthropics/claude-code-action, action.yml](https://github.com/anthropics/claude-code-action/blob/main/action.yml), commit `d5f7970`
- Claude API, [rate limits](https://platform.claude.com/docs/en/api/rate-limits)
- Claude API, [Python SDK: retries](https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/python#retries)
- Central de ajuda, [usage and length limits](https://support.claude.com/en/articles/11647753-usage-and-length-limits)
- GitHub, [events that trigger workflows: schedule](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)
- GitHub, [Actions limits](https://docs.github.com/en/actions/reference/limits)
