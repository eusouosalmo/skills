# Alerta do PostHog ou do Sentry vira issue da fábrica

Resumo: dá para ligar alerta a fábrica sem servidor próprio, mas por caminhos diferentes em cada ferramenta. O caminho comum às duas é o alerta criar uma issue no GitHub pela integração nativa, e a fábrica tratar essa issue como entrada não confiável: o Sentry faz isso com a ação "Create a new GitHub issue" numa regra de alerta (planos Business e Enterprise) e não cria uma segunda issue para o mesmo problema; o PostHog faz o mesmo com o destino GitHub do alerta de error tracking, sem checagem de duplicata no próprio template. Chamar o `/fire` de uma scheduled task direto do alerta só funciona no PostHog, cujo destino HTTP Webhook aceita header secreto e corpo em template; o webhook do Sentry e o webhook de alerta de insight do PostHog têm formato e headers fixos, então precisam de um intermediário. O `/fire` não tem chave de idempotência, o PostHog repete a chamada até 3 vezes, e os limites por hora (30 por task, 100 por conta) descartam ou recusam o excedente: a deduplicação tem de ficar antes do `/fire`, no throttle do alerta e nas trigger options do destino, e de novo dentro da run. Pesquisa de 2026-11-10 para o ticket [#107](https://github.com/eusouosalmo/skills/issues/107) do mapa [#103](https://github.com/eusouosalmo/skills/issues/103). Complementa [fabrica-de-software.md](fabrica-de-software.md), seções 8 (entrada não confiável) e 11.3 (scheduled tasks pela `factory-triage`), e fecha a pendência 5 de 11.9.

## Sumário

1. [Método](#1-método)
2. [O `/fire` das scheduled tasks](#2-o-fire-das-scheduled-tasks)
3. [PostHog](#3-posthog)
4. [Sentry](#4-sentry)
5. [Caminhos sem servidor próprio](#5-caminhos-sem-servidor-próprio)
6. [Onde ficam deduplicação e limite por hora](#6-onde-ficam-deduplicação-e-limite-por-hora)
7. [Texto do alerta como entrada não confiável](#7-texto-do-alerta-como-entrada-não-confiável)
8. [O que muda para a `factory-triage`](#8-o-que-muda-para-a-factory-triage)
9. [Lacunas](#9-lacunas)
10. [Fontes](#10-fontes)

## 1. Método

Só fontes primárias: a doc oficial de cada produto e, onde a doc não diz, o código-fonte público do produto, com o commit lido. **Confirmado** quer dizer que a fonte primária diz isso; **código** quer dizer que vem do código-fonte e pode mudar sem aviso na doc; **inferência** é conclusão minha. Nada foi testado com conta real.

## 2. O `/fire` das scheduled tasks

- **Forma da chamada.** `POST https://api.anthropic.com/v1/claude_code/routines/{id}/fire`, com `Authorization: Bearer` (token por task, prefixo `sk-ant-oat01-`), `anthropic-version` obrigatório e `Content-Type: application/json`. O header `anthropic-beta` passou a ser opcional. O corpo é opcional e tem um campo, `text`, de até 65.536 caracteres; o valor não é interpretado, e JSON enviado ali chega como string literal. A resposta traz o id e a URL da sessão criada e não espera a run terminar ([routines-fire](https://platform.claude.com/docs/en/api/claude-code/routines-fire)). **Confirmado.** Atenção: a página de [routines](https://code.claude.com/docs/en/routines) ainda mostra o exemplo antigo, com o header beta e sem `anthropic-version`; a referência da API é a mais recente.
- **Sem idempotência.** "Each successful request creates a new session. There is no idempotency key." Se quem chama repete a requisição, nascem várias sessões ([routines-fire](https://platform.claude.com/docs/en/api/claude-code/routines-fire)). **Confirmado.**
- **Limites por hora.** Cada task aceita 30 disparos por hora, somando API, Run now e rearme de task única; a conta aceita 100 disparos de API por hora, contados à parte do Run now. Acima do limite, o `/fire` responde `429 rate_limit_error` com `Retry-After`, e nenhum desses limites tem excedente pago. Eventos de GitHub têm teto por task e por conta, e o excedente é descartado até a janela virar ([routines](https://code.claude.com/docs/en/routines), [routines-fire](https://platform.claude.com/docs/en/api/claude-code/routines-fire)). **Confirmado.**
- **Token.** Vale para uma task só, não lê nada, e gerar outro revoga o anterior; não há API para gerenciar tokens ([routines-fire](https://platform.claude.com/docs/en/api/claude-code/routines-fire)). **Confirmado.**
- **O payload chega rotulado.** O `text` entra num bloco `<routine-fire-payload>` marcado como dado não confiável, e o modelo só age sobre ele se o prompt salvo da task mandar. A doc dá como caso de uso a triagem de alerta: a ferramenta de monitoramento chama o endpoint com o corpo do alerta em `text` e a run abre um PR draft com a correção ([routines](https://code.claude.com/docs/en/routines)). **Confirmado.**
- **Gatilho de GitHub em issue.** Além de PR e release, a task pode disparar em evento de issue (aberta, editada, fechada, reaberta, com label, atribuída), uma sessão nova por evento. Os filtros documentados (autor, título, corpo, labels e outros) aparecem só na seção de pull requests ([routines](https://code.claude.com/docs/en/routines)). **Confirmado** o evento; se os filtros valem para issue, a doc não diz.

## 3. PostHog

### 3.1 Alertas de error tracking

- **Três gatilhos:** issue criada, issue reaberta e issue em pico. O pico compara baldes de 5 minutos com a linha de base da última hora do próprio problema, com contagem mínima, multiplicador e um tempo de soneca: depois de um pico, não há novo aviso para aquele problema durante esse tempo ([alerts](https://posthog.com/docs/error-tracking/alerts.md), [spikes](https://posthog.com/docs/error-tracking/spikes.md)). **Confirmado**; a doc não dá os valores padrão.
- **Destinos.** A doc cita Slack, Discord, Teams e HTTP Webhook. O código do assistente de alertas do error tracking oferece também GitHub ("Create an issue in a repository"), GitLab, Linear e PagerDuty ([alertWizardConfig.ts](https://github.com/PostHog/posthog/blob/eed648ba16aef3763d5d9bd84a9a390b86fcb28c/products/error_tracking/frontend/scenes/ErrorTrackingConfigurationScene/alerting/alertWizardConfig.ts)). **Código.**
- **O alerta é um destino do pipeline (Hog function).** Cada gatilho é um sub-template ligado a um evento interno (`$error_tracking_issue_created`, `_reopened`, `_spiking`), e para cada um há variantes com o template HTTP Webhook e com o template GitHub ([sub-templates.ts](https://github.com/PostHog/posthog/blob/eed648ba16aef3763d5d9bd84a9a390b86fcb28c/frontend/src/scenes/hog-functions/sub-templates/sub-templates.ts)). **Código.** Por isso valem para o alerta os recursos de destino da seção 3.3 (inferência pela estrutura do código).

### 3.2 Destino GitHub: issue direto no repositório

- O template chama `POST /repos/{owner}/{repo}/issues` com o token da instalação do GitHub App do PostHog. Título e descrição são templates; o corpo inclui o stack trace do evento e um link de volta ao PostHog. O template não envia labels nem assignee e não confere se já existe issue para o mesmo problema ([github.template.ts](https://github.com/PostHog/posthog/blob/eed648ba16aef3763d5d9bd84a9a390b86fcb28c/nodejs/src/cdp/templates/_destinations/github/github.template.ts)). **Código.**
- O GitHub App do PostHog pede leitura e escrita em código, issues e pull requests ([integrations](https://posthog.com/docs/error-tracking/integrations.md)). **Confirmado.**
- **Inferência:** ligado só a "issue criada", cada problema novo do PostHog vira uma issue, e o próprio agrupamento do PostHog faz o papel de deduplicação. Ligado a "reaberta" ou "em pico", o mesmo problema pode abrir várias issues. Para pôr o label da fila, ou se edita o código do destino (a doc de customização permite editar a fonte), ou um workflow do repo põe o label depois.

### 3.3 Destino HTTP Webhook: chamar o `/fire` direto

- O template aceita método, corpo JSON com template (`{event.properties...}`), headers comuns e **headers secretos**, guardados cifrados, escondidos depois de salvos e fora dos logs, com valor enviado sem template; há também assinatura no padrão Standard Webhooks ([webhook.template.ts](https://github.com/PostHog/posthog/blob/eed648ba16aef3763d5d9bd84a9a390b86fcb28c/nodejs/src/cdp/templates/_destinations/webhook/webhook.template.ts)). **Código.** A doc confirma corpo em template e inputs secretos para credencial ([customizing destinations](https://posthog.com/docs/cdp/destinations/customizing-destinations)). **Confirmado.**
- Com isso, um destino aponta para a Fire URL, leva `Authorization: Bearer <token>` como header secreto, `anthropic-version` como header comum e um corpo `{"text": "..."}` montado com nome, descrição e link do problema. **Inferência**, montada a partir das duas fontes; não testado.
- **Retentativa.** Resposta fora de 2xx é repetida até 3 vezes conforme o código; resposta 4xx não conta como mau desempenho, e destino com erros ou lentidão prolongados é desligado ([destinations](https://posthog.com/docs/data-pipelines/destinations.md)). **Confirmado.** Somado à falta de idempotência do `/fire`, uma falha transitória pode gerar duas sessões (inferência).
- **Trigger options.** Uma versão de pré-lançamento da doc descreve opções que deduplicam o destino: disparar no máximo uma vez por intervalo, por pessoa ou por nome de evento, em janela móvel de 5 minutos a 24 horas, ou uma vez por dia UTC ([preview da doc de destinations](https://f9ce4237.posthog-preview.pages.dev/docs/cdp/destinations)). O código usa o mesmo mecanismo (`masking` com hash, TTL e limiar) em sub-templates de outros alertas ([sub-templates.ts](https://github.com/PostHog/posthog/blob/eed648ba16aef3763d5d9bd84a9a390b86fcb28c/frontend/src/scenes/hog-functions/sub-templates/sub-templates.ts)). **Código**, e doc ainda não publicada no domínio principal.

### 3.4 Alertas de insight

- Valem para trends, funnels e SQL, checados de tempo real (cerca de 2 minutos, planos Scale e Enterprise) a mensal. O webhook manda um POST no formato do Alertmanager, com headers fixos (`Content-Type` e `X-PostHog-Webhook-Version`) e só a URL configurável, e repete o envio **a cada checagem enquanto a condição valer**, sem aviso de resolução ([alerts](https://posthog.com/docs/alerts)). **Confirmado.**
- Consequência: esse webhook não chama o `/fire` (falta o header de autorização) e, mesmo com intermediário, dispararia a cada checagem. **Inferência.** O código tem um sub-template de Hog function para "insight alert firing" com o template HTTP Webhook, o que permitiria header secreto; a doc não fala dele, e fica como lacuna.

## 4. Sentry

- **Issue automática no GitHub.** Numa regra de alerta, a ação "Create a new GitHub issue" cria a issue quando o alerta dispara. Criação automática exige plano Business ou Enterprise; criação manual e sincronização de comentários, assignee e status valem a partir do Team ([GitHub integration](https://docs.sentry.io/organization/integrations/source-code-mgmt/github/)). **Confirmado.**
- **Labels e assignee.** A doc não fala de label. O código da integração monta o formulário com repositório, assignee e labels do repo, e envia `labels` na criação ([issues.py](https://github.com/getsentry/sentry/blob/f32ec8032d77a395fb9a50e7653592e12639cadb/src/sentry/integrations/github/issues.py)). **Código.** Dá para a regra já pôr o label da fila (inferência: a ação de alerta reusa esse formulário).
- **Deduplicação nativa.** Antes de criar, a ação confere se o problema do Sentry já tem issue ligada naquela integração e, se tiver, não cria outra ([create_ticket/utils.py](https://github.com/getsentry/sentry/blob/ae29b66fe41a4b1919f69f01a8918c3372a6adf7/src/sentry/rules/actions/integrations/create_ticket/utils.py)). **Código.**
- **Throttle da regra.** Cada regra tem um intervalo de ação, de "a cada disparo" (padrão) a 30 dias, passando por 5, 10, 30 e 60 minutos, 3, 12 e 24 horas e 1 semana; dentro da janela as ações não rodam de novo. Gatilhos: problema novo, regressão e filtros de frequência ([issue alert config](https://docs.sentry.io/product/alerts/create-alerts/issue-alert-config/)). **Confirmado.**
- **Webhook do Sentry não chama o `/fire`.** O webhook da integration platform tem estrutura fixa (`action`, `installation`, `data`, `actor`) e manda headers próprios, como `Sentry-Hook-Resource` e `Sentry-Hook-Signature` (HMAC-SHA256 do corpo); a doc não oferece header customizado e espera resposta em 1 segundo ([webhooks](https://docs.sentry.io/organization/integrations/integration-platform/webhooks/)). **Confirmado.** Sem `Authorization` nem campo `text`, precisa de intermediário que confira a assinatura e repasse (inferência).

## 5. Caminhos sem servidor próprio

| Caminho | PostHog | Sentry | Dedup nativa | Observação |
| :- | :- | :- | :- | :- |
| A. Alerta cria issue no GitHub; a fábrica pega a issue | destino GitHub (código) | ação "Create a new GitHub issue", Business ou Enterprise | Sentry sim; PostHog só pelo agrupamento em "issue criada" | Mantém uma fila só, como decidido em 11.2. A issue vem de um bot, ver seção 7 |
| B. Alerta chama o `/fire` direto | destino HTTP Webhook com header secreto | não dá | trigger options do destino | Run na nuvem da Anthropic, sem issue: a issue ou o PR nasce dentro da run |
| C. Alerta chama `repository_dispatch` do GitHub | destino HTTP Webhook com header secreto | não dá | trigger options do destino | Workflow do Actions recebe o alerta em `client_payload` |
| D. Issue criada em A dispara uma scheduled task | gatilho de GitHub em issue | idem | teto por hora da task | Alternativa ao Actions para quem usa a nuvem da Anthropic |

- **C, detalhes.** O endpoint pede token com escopo `repo` (classic), `event_type` de até 100 caracteres e `client_payload` com até 10 propriedades no topo e menos de 64 KB; responde 204 ([repository dispatch](https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)). `repository_dispatch` sempre cria run de workflow ([trigger a workflow](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)). **Confirmado.** Exige um PAT guardado no PostHog, o que a seção 8 da nota da fábrica desaconselha em fluxo com entrada externa; o escopo mínimo de um token fine-grained para esse endpoint não foi conferido.
- **A com Actions.** Issue criada pelo GitHub App do Sentry ou do PostHog dispara `issues: opened`: só eventos do `GITHUB_TOKEN` deixam de criar run, e a doc apresenta o token de GitHub App como a alternativa que dispara ([trigger a workflow](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)). **Confirmado** a regra do `GITHUB_TOKEN`; que o token de instalação dispara é leitura direta da doc, não dito com todas as letras.
- **Sem intermediário para o Sentry chamar o `/fire`.** Qualquer repasse (função serverless, worker) é servidor, ainda que pequeno. Para o Sentry, o caminho A é o único sem código próprio. **Inferência.**

## 6. Onde ficam deduplicação e limite por hora

Em camadas, da origem para a run (inferência, a partir das seções 2 a 4):

1. **Na fonte do alerta.** Sentry: intervalo de ação da regra e checagem de issue já ligada. PostHog: gatilho "issue criada" no lugar de "em pico", soneca do pico e trigger options do destino. Alerta de insight do PostHog não serve como gatilho direto, porque repete a cada checagem.
2. **No transporte.** O `/fire` não deduplica e o PostHog retenta até 3 vezes; os tetos de 30 por task e 100 por conta funcionam como disjuntor, mas o excedente é perdido (429 no `/fire`, evento descartado no gatilho de GitHub), não enfileirado.
3. **Na fábrica.** A primeira ação da run de triagem é procurar issue aberta com a mesma impressão digital do alerta (id do problema no Sentry ou no PostHog, que os dois põem no corpo como link) e comentar nela em vez de abrir outra. No Actions, `concurrency` por id do problema evita duas runs em paralelo (pergunta 4 da seção 12 da nota da fábrica). O teto por hora próprio da fábrica, se necessário, vai no workflow ou no `.factory/config.yml`.

## 7. Texto do alerta como entrada não confiável

- Mensagem de erro, URL, user agent e stack trace podem conter texto escolhido pelo usuário final do produto. No caminho A, esse texto vira corpo de issue escrito por um bot; no B, vira o `text` do `/fire`.
- **B já vem protegido no transporte:** o `<routine-fire-payload>` rotula o texto como dado, e o prompt salvo da task decide o que fazer com ele (seção 2). Quem tiver o token pode mandar qualquer `text`; o rótulo continua valendo. **Confirmado.**
- **A depende do workflow.** O gate da seção 11.4 da nota da fábrica aceita só autor OWNER, MEMBER ou COLLABORATOR; a issue do Sentry ou do PostHog vem de um GitHub App, e o `claude-code-action` barra bots por padrão (seção 8 da nota da fábrica). A `factory-triage` precisa liberar exatamente o login do bot de cada integração, nunca bots em geral. Os logins exatos não foram conferidos. **Inferência.**
- **Triagem lê, não escreve código.** A run que lê alerta recebe token só de leitura e de issue, sem segredo de produção no ambiente e com rede restrita; a saída é uma issue triada com label, que segue a fila normal até o `agent:implement` posto por humano ou por regra determinística. Isso responde a pergunta 11 da seção 12 da nota da fábrica com a mesma fila e permissões menores na etapa de triagem. **Inferência**, coerente com a seção 8 da nota da fábrica.
- Título e corpo nunca entram em shell nem em expressão `${{ }}` do workflow; vão para arquivo (seção 8 da nota da fábrica).

## 8. O que muda para a `factory-triage`

Proposta, não decisão:

- Perfil `sentry`: regra de alerta com "Create a new GitHub issue", label da fila e throttle; exige Business ou Enterprise. No plano Team, só criação manual, e o perfil se reduz a um botão.
- Perfil `posthog`: destino GitHub no alerta de "issue criada", label posto por workflow ou por edição do destino; opcionalmente destino HTTP Webhook para o `/fire` com header secreto e trigger options.
- Perfil `clock`: scheduled task com agenda (no mínimo de hora em hora, pela regra do cron) que varre o que os alertas não cobrem.
- Em todos: a triagem deduplica pela impressão digital antes de criar ou comentar, e a issue triada entra na mesma fila da `factory-install`.

## 9. Lacunas

1. Logins de bot das integrações GitHub do Sentry e do PostHog, e como o gate os libera.
2. Se os filtros do gatilho de GitHub das scheduled tasks valem para eventos de issue.
3. Trigger options do PostHog na doc publicada (hoje só no preview) e se aparecem para destinos de alerta do error tracking.
4. O sub-template de webhook para alerta de insight do PostHog: existe na UI, com header secreto?
5. Escopo mínimo de token fine-grained para `repository_dispatch`.
6. Teste real ponta a ponta de um destino PostHog chamando o `/fire`.

## 10. Fontes

Claude Code e Claude Platform:

- [Automate work with scheduled tasks (routines)](https://code.claude.com/docs/en/routines)
- [Trigger a routine through the API](https://platform.claude.com/docs/en/api/claude-code/routines-fire)

PostHog, doc:

- [Error tracking alerts](https://posthog.com/docs/error-tracking/alerts.md)
- [Spike detection](https://posthog.com/docs/error-tracking/spikes.md)
- [Error tracking integrations](https://posthog.com/docs/error-tracking/integrations.md)
- [Insight alerts](https://posthog.com/docs/alerts)
- [Destinations](https://posthog.com/docs/data-pipelines/destinations.md)
- [Customizing destinations](https://posthog.com/docs/cdp/destinations/customizing-destinations)
- [Destinations, versão de pré-lançamento com trigger options](https://f9ce4237.posthog-preview.pages.dev/docs/cdp/destinations)

PostHog, código (commit `eed648b` do repositório PostHog/posthog):

- [github.template.ts](https://github.com/PostHog/posthog/blob/eed648ba16aef3763d5d9bd84a9a390b86fcb28c/nodejs/src/cdp/templates/_destinations/github/github.template.ts)
- [webhook.template.ts](https://github.com/PostHog/posthog/blob/eed648ba16aef3763d5d9bd84a9a390b86fcb28c/nodejs/src/cdp/templates/_destinations/webhook/webhook.template.ts)
- [sub-templates.ts](https://github.com/PostHog/posthog/blob/eed648ba16aef3763d5d9bd84a9a390b86fcb28c/frontend/src/scenes/hog-functions/sub-templates/sub-templates.ts)
- [alertWizardConfig.ts](https://github.com/PostHog/posthog/blob/eed648ba16aef3763d5d9bd84a9a390b86fcb28c/products/error_tracking/frontend/scenes/ErrorTrackingConfigurationScene/alerting/alertWizardConfig.ts)

Sentry, doc e código:

- [GitHub integration](https://docs.sentry.io/organization/integrations/source-code-mgmt/github/)
- [Issue alert configuration](https://docs.sentry.io/product/alerts/create-alerts/issue-alert-config/)
- [Webhooks da integration platform](https://docs.sentry.io/organization/integrations/integration-platform/webhooks/)
- [integrations/github/issues.py](https://github.com/getsentry/sentry/blob/f32ec8032d77a395fb9a50e7653592e12639cadb/src/sentry/integrations/github/issues.py)
- [rules/actions/integrations/create_ticket/utils.py](https://github.com/getsentry/sentry/blob/ae29b66fe41a4b1919f69f01a8918c3372a6adf7/src/sentry/rules/actions/integrations/create_ticket/utils.py)

GitHub:

- [Create a repository dispatch event](https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)
- [Triggering a workflow](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)
