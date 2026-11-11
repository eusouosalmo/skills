# Um workflow para os três perfis de runner: `runs-on` por variável

Resumo: sim, um único workflow de agente serve aos perfis `github`, `local` e `vps` trocando só o `runs-on` por uma variável do repositório. A doc de contextos do GitHub lista `vars` entre os contextos aceitos em `jobs.<job_id>.runs-on` e traz o exemplo `runs-on: ${{ vars.RUNNER }}`. Uma variável é uma string, então ela escolhe um label só; para uma lista de labels (`self-hosted` mais um label do perfil) a saída é guardar JSON na variável e ler com `fromJSON`, o que a regra de funções permite, mas não há exemplo oficial (inferência, falta testar). Variável não definida vira string vazia, por isso o workflow precisa de um valor padrão. Grupos de runner não servem a um repo de conta pessoal: no GitHub.com eles são de organização no plano Team ou acima; o perfil se distingue por label. O que muda entre hospedado e self-hosted não está no YAML, está em volta: VM nova por job contra máquina que guarda estado, Claude Code instalado pela action a cada run, cache e limpeza por hooks ou por runner `--ephemeral`/JIT. Pesquisa de 2026-11-10 para o ticket [#104](https://github.com/eusouosalmo/skills/issues/104) do mapa [#103](https://github.com/eusouosalmo/skills/issues/103); responde à pendência 2 de [fabrica-de-software.md](fabrica-de-software.md), seção 11.9, sem repetir a tabela de custo e isolamento da seção 11.3.

## Sumário

1. [Fontes e método](#1-fontes-e-método)
2. [`vars` em `runs-on`](#2-vars-em-runs-on)
3. [Labels e grupos](#3-labels-e-grupos)
4. [O que muda entre hospedado e self-hosted](#4-o-que-muda-entre-hospedado-e-self-hosted)
5. [Forma proposta para a `factory-install`](#5-forma-proposta-para-a-factory-install)
6. [O que falta testar](#6-o-que-falta-testar)

## 1. Fontes e método

Li a fonte Markdown da doc do GitHub no repositório público `github/docs` (branch `main`, 2026-11-10), incluindo os trechos reutilizáveis que a página renderizada monta, e o código da `claude-code-action` (branch `main`). Cada afirmação diz se é **confirmado** (está escrito na fonte primária) ou **inferência** (conclusão minha, sem teste).

| Sigla | Fonte |
| :- | :- |
| CTX | [Contexts reference](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts): tabela de disponibilidade de contextos e o contexto `vars` |
| WS | [Workflow syntax, `jobs.<job_id>.runs-on`](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idruns-on) |
| VAR | [Variables reference](https://docs.github.com/en/actions/reference/workflows-and-actions/variables#configuration-variable-precedence): precedência das variáveis de configuração |
| EXP | [Expressions, `fromJSON`](https://docs.github.com/en/actions/reference/workflows-and-actions/expressions#fromjson) |
| RG | [Runner groups](https://docs.github.com/en/actions/concepts/runners/runner-groups) |
| SH | [Self-hosted runners, concepts](https://docs.github.com/en/actions/concepts/runners/self-hosted-runners) e [reference](https://docs.github.com/en/actions/reference/runners/self-hosted-runners) |
| GH | [GitHub-hosted runners, concepts](https://docs.github.com/en/actions/concepts/runners/github-hosted-runners) e [reference](https://docs.github.com/en/actions/reference/runners/github-hosted-runners) |
| HK | [Running scripts before or after a job](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/run-scripts) |
| CA | [Dependency caching reference](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching#usage-limits-and-eviction-policy) |
| CCA | `claude-code-action`: [action.yml](https://github.com/anthropics/claude-code-action/blob/main/action.yml) e [src/entrypoints/run.ts](https://github.com/anthropics/claude-code-action/blob/main/src/entrypoints/run.ts) |

## 2. `vars` em `runs-on`

- **`vars` é aceito.** Na tabela de disponibilidade, a linha `jobs.<job_id>.runs-on` lista os contextos `github, needs, strategy, matrix, vars, inputs` e nenhuma função especial (CTX). O exemplo oficial do contexto `vars` usa `runs-on: ${{ vars.RUNNER }}` (CTX). `secrets`, `env` e `runner` não estão na lista. **Confirmado.**
- **O que `runs-on` aceita.** Uma string; uma variável que contém uma string; um array de strings, de variáveis ou dos dois misturados; ou um par `key: value` com as chaves `group` e `labels` (WS). Expressão dentro de array precisa de aspas, como em `[self-hosted, "${{ inputs.chosen-os }}"]` (WS). **Confirmado.**
- **Lista ou objeto vindo de uma variável só.** A doc fala em "variável contendo uma string", e uma variável de configuração é sempre texto. A tabela de contextos diz que, fora das funções especiais listadas, "a function can be used anywhere" (CTX), e `fromJSON` converte texto em array ou objeto (EXP). Então `runs-on: ${{ fromJSON(vars.AGENT_RUNNER) }}` com a variável valendo `["self-hosted","linux","factory-vps"]` deveria funcionar. **Confirmado** cada regra isolada; **inferência** a combinação em `runs-on`, sem exemplo oficial e sem teste.
- **Variável não definida.** O contexto devolve string vazia (CTX, e "dereference a nonexistent property" também vira string vazia). A doc não diz o que acontece com `runs-on` vazio; o mais provável é o job falhar ou ficar sem runner (inferência). Com o operador `||`, que devolve o primeiro valor verdadeiro, dá para ter um padrão: `${{ vars.AGENT_RUNNER || 'ubuntu-latest' }}`. **Inferência** o padrão; o operador é da doc de expressões.
- **Nível da variável.** Se o mesmo nome existe em organização, repositório e environment, vale o mais baixo (environment, depois repositório). Mas variáveis de environment só existem no runner depois que o job começa, e não sobrescrevem o contexto `vars` (VAR). Para `runs-on`, então, servem variáveis de repositório ou de organização; uma variável de environment não escolhe o runner. **Confirmado** a regra; a consequência para `runs-on` é leitura direta dela.
- **Gatilho `issues: labeled`.** A tabela de contextos não restringe `vars` por evento, e o exemplo oficial usa `workflow_dispatch`. Não achei nada que impeça `vars` num workflow disparado por label (inferência; teste rápido na seção 6).

## 3. Labels e grupos

- **Labels.** O runner self-hosted recebe o label `self-hosted` por padrão (dá para tirar com `--no-default-labels`); a doc recomenda um array que comece por `self-hosted`, "this must be listed first", e o job só vai para um runner que tenha todos os labels do array (WS). **Confirmado.** Para os perfis: o runner do PC leva um label próprio (ex. `factory-local`) e o da VPS outro (ex. `factory-vps`), e a variável carrega `["self-hosted","linux","factory-local"]` ou o equivalente. Os nomes dos labels são sugestão minha.
- **Grupos.** `runs-on` aceita `group:` sozinho ou `group:` com `labels:`; com os dois, o runner precisa cumprir ambos (WS). Mas no GitHub.com grupos de runner são para organizações no plano Team (RG, trecho reutilizável `about-runner-groups`), e podem conter só runners maiores ou self-hosted (WS). Os repositórios do eusouosalmo são de conta pessoal, com runners no nível do repositório (SH). **Confirmado.** Conclusão: o kit usa labels; grupo fica como opção para quem roda numa organização paga.
- **Fila sem runner.** Se nenhum runner casa com os labels, o job espera até 24 horas e expira (SH; já citado na seção 11.3 da nota da fábrica). Com o perfil `local` e o PC desligado, a issue fica parada sem erro visível nesse período.

## 4. O que muda entre hospedado e self-hosted

O YAML é o mesmo; o que muda é o estado que sobra na máquina e quem cuida dele.

| Tema | `github` (hospedado) | `local` e `vps` (self-hosted) |
| :- | :- | :- |
| Máquina | VM nova por job, exceto os runners de uma CPU, que rodam em container numa VM compartilhada; software pré-instalado e atualizado toda semana; `sudo` sem senha no Linux (GH). **Confirmado** | "Don't need to have a clean instance for every job"; você atualiza sistema e ferramentas; só o aplicativo do runner se atualiza sozinho, e quem desliga essa atualização precisa atualizar em até 63 dias (SH). **Confirmado** |
| Claude Code | A action instala a cada run pelo script oficial, com versão fixada no código da action (2.1.322 em 2026-11-10) e até três tentativas; instala também o Bun numa versão fixa (CCA). **Confirmado** | O mesmo, salvo se o workflow passar `path_to_claude_code_executable` e `path_to_bun_executable`, que pulam a instalação (CCA). **Confirmado.** Instalar uma vez na máquina economiza download, mas a versão deixa de seguir a da action; com runner efêmero em container, o lugar certo é a imagem (inferência) |
| Isolamento de subprocesso | Com `allowed_non_write_users`, a action instala `bubblewrap` e `socat` via `apt-get` (CCA). **Confirmado** | O passo exige `apt-get` e `sudo` e é pulado onde eles faltam (CCA). **Confirmado.** A fábrica não pretende usar essa opção (gate da seção 11.4), então não pesa |
| Estado do usuário | Some com a VM | Num runner persistente, o diretório de trabalho e a home do usuário do runner, inclusive `~/.claude` (configuração, memória e credenciais), ficam para o job seguinte (inferência, a partir da recomendação de efêmero para "limit the exposure of any sensitive resources from previous jobs", SH) |
| Cache | `actions/cache` guarda no GitHub: 10 GB por repositório por padrão, entrada sem acesso há 7 dias é removida (CA). **Confirmado** | O mesmo `actions/cache` vale; um runner persistente ainda tem o disco local como cache de graça, que um runner efêmero perde (inferência) |
| Limpeza | Não há o que limpar | Hooks `ACTIONS_RUNNER_HOOK_JOB_STARTED` e `ACTIONS_RUNNER_HOOK_JOB_COMPLETED`: caminho absoluto de um script, definido no sistema ou no `.env` do diretório do runner (pede reinício do runner); o script roda com o usuário do serviço do runner, de forma síncrona e sem timeout próprio; se o script de início sai com código diferente de zero, o job falha; o script não deve ficar dentro do diretório `actions-runner`; o que ele imprime aparece no log, visível a quem lê o repo (HK). **Confirmado** |
| Runner de um job só | Não se aplica | `config.sh --ephemeral` registra um runner que pega um job e é desregistrado em seguida; recriar a máquina limpa fica com a sua automação; os logs do runner efêmero precisam ir para fora; JIT é a mesma ideia pela REST API; em container, desligar a atualização automática para não atualizar a cada job (SH). **Confirmado.** O aviso de que reaproveitar o hardware do JIT ainda pode vazar dados já está na seção 11.3 |

Leitura para o kit (inferência): no perfil `vps`, runner efêmero em container descartável, recriado por um serviço do systemd (seção 11.5 da nota da fábrica), resolve estado do usuário, credenciais e limpeza de uma vez, ao custo de perder o cache local e de instalar Claude Code a cada job (ou embuti-lo na imagem). No perfil `local`, um runner persistente com usuário Linux próprio e hook `JOB_STARTED` que zera o workspace e o `~/.claude` do usuário do runner é o mínimo; o efêmero é melhor se o custo de montar couber.

## 5. Forma proposta para a `factory-install`

Inferência montada sobre as regras confirmadas acima, a testar antes de virar padrão:

```yaml
on:
  issues:
    types: [labeled]

jobs:
  implement:
    if: github.event.label.name == 'agent:implement'
    runs-on: ${{ fromJSON(vars.AGENT_RUNNER || '"ubuntu-latest"') }}
```

| Perfil | Valor de `AGENT_RUNNER` (variável de repositório) |
| :- | :- |
| `github` | não definir (cai no padrão) ou `"ubuntu-latest"` |
| `local` | `["self-hosted","linux","factory-local"]` |
| `vps` | `["self-hosted","linux","factory-vps"]` |

O padrão vai entre aspas duplas dentro das simples porque `fromJSON` recebe texto JSON, e uma string JSON precisa das aspas. A `factory-install` grava a variável com `gh variable set AGENT_RUNNER` e anota o perfil no `.factory/config.yml`; a fonte da verdade para o job é a variável, porque `runs-on` não lê arquivo do repo. A recusa do perfil `local` em repo público (seção 11.3) continua sendo checagem da skill, não do YAML.

## 6. O que falta testar

1. `runs-on: ${{ fromJSON(vars.AGENT_RUNNER || '"ubuntu-latest"') }}` num repo de teste, com a variável ausente, com string e com array, disparado por `issues: labeled`. Responde de vez à pendência 2 da seção 11.9.
2. O que o GitHub mostra quando `runs-on` resolve para vazio ou para JSON inválido (erro no início do job ou fila de 24 horas).
3. Onde o script de instalação do Claude Code grava o binário e a configuração no usuário do runner, para o hook de limpeza saber o que apagar.
