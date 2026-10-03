# Guardrails de git e modo AFK no Claude Code

Resumo: nenhuma camada sozinha protege um repositório quando o agente roda sem supervisão. A doc oficial deixa claro que permission rules e hooks olham o texto do comando e podem ser contornados, e que só o isolamento (sandbox, container, VM) e as proteções do lado do servidor (branch protection, tokens com escopo) seguram de verdade. A comunidade combina várias camadas: hook que bloqueia git destrutivo, container, worktree, testes como backpressure, limite de iterações e revisão com contexto limpo.

Pesquisa feita em 2026-10-01 para o ticket [#7](https://github.com/eusouosalmo/skills/issues/7); a seção 12 (outros agentes) foi acrescentada em 2026-10-02. A doc do Claude Code muda rápido e cita versões (v2.1.x); confira a página antes de decidir.

## Sumário

1. [Método e níveis de confiança](#1-método-e-níveis-de-confiança)
2. [As camadas de proteção, da mais fraca à mais forte](#2-as-camadas-de-proteção-da-mais-fraca-à-mais-forte)
3. [O que a doc oficial do Claude Code diz](#3-o-que-a-doc-oficial-do-claude-code-diz)
4. [A skill git-guardrails-claude-code do Matt Pocock](#4-a-skill-git-guardrails-claude-code-do-matt-pocock)
5. [Outras ferramentas da comunidade](#5-outras-ferramentas-da-comunidade)
6. [Práticas de loop AFK](#6-práticas-de-loop-afk)
7. [Proteção do lado do servidor](#7-proteção-do-lado-do-servidor)
8. [AFK x sessão interativa](#8-afk-x-sessão-interativa)
9. [Deny rules x hooks](#9-deny-rules-x-hooks)
10. [Onde as fontes concordam e divergem](#10-onde-as-fontes-concordam-e-divergem)
11. [Perguntas abertas para o ticket de desenho](#11-perguntas-abertas-para-o-ticket-de-desenho)
12. [Guardrails em outros agentes](#12-guardrails-em-outros-agentes)
13. [Fontes](#13-fontes)

## 1. Método e níveis de confiança

Fontes primárias: a doc oficial do Claude Code (baixada em Markdown direto de code.claude.com), o código da skill do Matt Pocock via `gh api`, o post original do Geoffrey Huntley, o post do Matt sobre Ralph, os READMEs de duas ferramentas de guarda populares e os exemplos de settings do repositório anthropics/claude-code.

Além de ler, rodei o script do Matt localmente contra uma lista de comandos, alimentando o JSON pelo stdin como o Claude Code faz, sem instalar nada em nenhum settings.json. Os resultados estão na seção 4.

Cada prática traz quatro campos, conforme as Notes do mapa ([#1](https://github.com/eusouosalmo/skills/issues/1)):

- **confirmado**: está na doc oficial.
- **convenção**: vários repositórios ou autores independentes fazem.
- **relato**: um autor afirma.

## 2. As camadas de proteção, da mais fraca à mais forte

A doc oficial descreve estas camadas como complementares ([permissions](https://code.claude.com/docs/en/permissions#how-permissions-interact-with-sandboxing), [sandbox-environments](https://code.claude.com/docs/en/sandbox-environments)). Em ordem de força:

| Camada | Quem aplica | O que segura | Ponto fraco |
| :- | :- | :- | :- |
| Instruções (CLAUDE.md, prompt, "não faça push") | O modelo | Intenção | Não é enforcement; some com compactação de contexto |
| Permission rules (allow, ask, deny) | Claude Code, pelo texto do comando | A forma usual do comando | `git -C . push`, `sh -c`, caminho absoluto passam |
| Hook PreToolUse | Seu script, antes da regra | O que o seu parser reconhecer | Falha aberta se o script quebrar; regex é contornável |
| Classificador do auto mode | Outro modelo | Ações de risco por julgamento | Probabilístico; push normal é permitido por padrão |
| Sandbox do Bash | Sistema operacional (bubblewrap, Seatbelt) | Arquivos e rede dos comandos Bash | Não cobre Read, Edit, Write, MCP nem hooks |
| Container, VM, sandbox runtime | Sistema operacional ou hypervisor | O processo inteiro do Claude Code | O workspace montado continua gravável; rede liberada vaza dados |
| Servidor (branch protection, token sem permissão de push) | GitHub | O remoto | Não protege o trabalho local não commitado |

A ideia que atravessa todas as fontes: as camadas de cima reduzem acidentes, as de baixo contêm o estrago.

## 3. O que a doc oficial do Claude Code diz

### 3.1 Permission rules: allow, ask, deny

- **O que é:** regras `Tool` ou `Tool(specifier)` nas listas `permissions.allow`, `ask` e `deny`. Avaliação em ordem fixa: deny, depois ask, depois allow; a primeira que casar decide, e especificidade não muda a ordem. Um deny amplo (`Bash(aws *)`) vence um allow estreito. Um deny com nome puro (`Bash`) tira a ferramenta do contexto do modelo.
- **Por que existe:** trocar o prompt a cada ação por uma política declarada. A doc frisa que "Permission rules are enforced by Claude Code, not by the model": instrução no CLAUDE.md muda o que o Claude tenta, não o que é permitido.
- **Fonte:** [permissions, Manage permissions](https://code.claude.com/docs/en/permissions#manage-permissions).
- **Confiança:** confirmado.

Detalhes relevantes para git:

- O `*` tem que vir depois do subcomando. `Bash(git push *)` pega só `git push`; `Bash(git * main)` pega qualquer subcomando, inclusive `git -c core.fsmonitor=<script> diff main`.
- Compound commands são separados (`&&`, `||`, `;`, `|`, `&`, newline), e deny/ask valem para qualquer subcomando, inclusive dentro de subshell, `$(...)` e laços. `cd /tmp && git clean -f` ainda cai num `ask` de `Bash(git clean *)`.
- Wrappers fixos são removidos antes de casar (`timeout`, `time`, `nice`, `nohup`, `stdbuf`, `command`, `builtin`, `xargs` sem flags). Atribuição de variável no começo não esconde o comando de uma regra deny.

### 3.2 O que uma Bash rule não pega

- **O que é:** a doc publica uma tabela do que escapa. Para `Bash(git push *)` em deny, passam `git -C . push origin main`, `git -c push.default=current push origin main` e `git 'push' origin main`. Para `Bash(rm *)`, passam `/bin/rm` e `bash -c 'rm ...'`.
- **Por que existe:** deixar claro que a regra "covers the invocation Claude usually produces and isn't a security boundary around the program". Para algo que não dependa do texto, a doc manda usar sandbox; para lógica própria, hook PreToolUse.
- **Fonte:** [permissions, What a Bash rule doesn't match](https://code.claude.com/docs/en/permissions#bash-rule-limits).
- **Confiança:** confirmado.

### 3.3 Hooks PreToolUse

- **O que é:** comando (ou HTTP, MCP tool, prompt, agent) que roda antes de cada chamada de ferramenta, recebe JSON no stdin (`tool_name`, `tool_input.command` etc.) e devolve uma decisão. O `matcher` filtra pelo nome da ferramenta: só letras, dígitos, `_`, `-`, espaço, `,` e `|` viram comparação exata (`Bash`, `Edit|Write`); qualquer outro caractere vira regex JavaScript sem âncora (`Edit.*` também pega `NotebookEdit`). O campo `if` usa a sintaxe de permission rule (`"Bash(git *)"`) para filtrar por argumento.
- **Por que existe:** permitir política com lógica própria, além do que a sintaxe de regra expressa.
- **Fonte:** [hooks reference](https://code.claude.com/docs/en/hooks), seções Matcher patterns, Exit code output e PreToolUse decision control.
- **Confiança:** confirmado.

Como a decisão sai:

- **Exit 2** bloqueia; o stderr vira o motivo que o Claude lê. Nem um JSON com `permissionDecision: "allow"` desfaz um exit 2.
- **Exit 0 com JSON** em `hookSpecificOutput`: `permissionDecision` pode ser `allow`, `deny`, `ask` ou `defer` (este só em `-p`). Com vários hooks, vale `deny` > `defer` > `ask` > `allow`. `updatedInput` reescreve a entrada.
- **Exit 1 ou outro código sem JSON válido não bloqueia.** A doc avisa em destaque: exit 1 é "non-blocking error", a ação segue.
- **Hook que não inicia** (caminho errado, sem permissão de execução, código 127) também não bloqueia: "a mistyped path in `settings.json` leaves the gate silently disabled".
- **Timeout** de um hook `command` em PreToolUse não bloqueia; a chamada segue o fluxo normal. O timeout padrão é 10 minutos.

Esses três últimos pontos querem dizer que um hook de guarda falha aberto por padrão. Cabe ao script ser robusto.

### 3.4 Hooks valem em todo permission mode

- **O que é:** PreToolUse dispara antes da checagem de modo, em todos os modos, inclusive `dontAsk` e `bypassPermissions`. Um `deny` de hook bloqueia mesmo com `--dangerously-skip-permissions`. O inverso não vale: um `allow` de hook não passa por cima de uma deny rule. Hooks também disparam dentro de subagents.
- **Por que existe:** dar uma política que o usuário não desliga trocando de modo. Nas palavras da doc, hooks "can tighten restrictions but not loosen them".
- **Fonte:** [hooks-guide, Hooks and permission modes](https://code.claude.com/docs/en/hooks-guide#hooks-and-permission-modes); [hooks, Hook locations](https://code.claude.com/docs/en/hooks#hook-locations).
- **Confiança:** confirmado.

### 3.5 Permission modes

- **O que é:** o modo define o que roda sem perguntar. `default` (Manual), `acceptEdits`, `plan`, `auto` (classificador revisa), `dontAsk` (nega tudo que pediria aprovação, roda só o que está em allow) e `bypassPermissions` (pula prompts e até as escritas em protected paths). Deny rules valem em todos, inclusive no bypass.
- **Por que existe:** cada modo troca conveniência por supervisão. A doc indica `dontAsk` para "Locked-down CI and scripts" e `bypassPermissions` para "Isolated containers and VMs only".
- **Fonte:** [permission-modes](https://code.claude.com/docs/en/permission-modes#available-modes).
- **Confiança:** confirmado.

Detalhes que importam para AFK:

- O Claude Code recusa `--dangerously-skip-permissions` como root ou sob `sudo` no Linux e no macOS, a menos que esteja num sandbox reconhecido.
- `bypassPermissions` e `auto` postos no `.claude/settings.json` do projeto não fazem efeito: um repositório não consegue se auto-promover a bypass.
- `permissions.disableBypassPermissionsMode: "disable"` funciona em qualquer escopo; o usuário pode se trancar fora do bypass.
- Em versões recentes, `auto` é o modo inicial padrão no terminal. Para `-p`, depende de feature flags; a doc recomenda passar o modo explicitamente.

### 3.6 O classificador do auto mode

- **O que é:** em `auto`, um modelo separado revisa ações antes de rodar. Bloqueia por padrão, entre outros: force push, `git reset --hard`, `git checkout -- .`, `git restore .`, `git clean -fd`, `git stash drop` e `git stash clear`, `git commit --amend` em commit que não é da sessão ou já foi empurrado, merge de PR sem aprovação humana, desligar CI, trocar remoto com `git remote set-url`, e lançar loop autônomo com `--dangerously-skip-permissions`. **Permite por padrão** push para qualquer branch do repositório atual, inclusive a default.
- **Por que existe:** reduzir o cansaço de prompt sem abrir mão de uma checagem por ação.
- **Fonte:** [permission-modes, What the classifier blocks by default](https://code.claude.com/docs/en/permission-modes#what-the-classifier-blocks-by-default).
- **Confiança:** confirmado.

Ressalvas da própria doc:

- Limites ditos na conversa ("não faça push") viram sinal de bloqueio, mas "a boundary can be lost if context compaction removes the message". Para garantia, ela manda usar deny rule.
- Para exigir checkpoint humano antes do push em auto mode, a doc sugere `permissions.ask`.
- Em `-p` sem `--permission-prompt-tool`, depois de 3 bloqueios seguidos ou 20 no total, a ação não roda e o agente continua; o run não para.
- A doc descreve o classificador como "a per-action control, not an isolation boundary".

### 3.7 Protected paths e critical paths

- **O que é:** escritas em `.git`, `.claude` (menos `.claude/worktrees`), `.husky`, `.devcontainer`, `.gitconfig`, `.pre-commit-config.yaml`, `lefthook.yml`, arquivos de shell e outros nunca são aprovadas automaticamente, exceto em `bypassPermissions`. Allow rules não pré-aprovam esses caminhos. À parte, `rm` e `rmdir` em critical paths (raiz, home, diretório de trabalho e pais) nunca são aprovados por allow rule nem por hook `allow`.
- **Por que existe:** impedir que o agente corrompa o estado do repositório ou reescreva a própria configuração (dar-se permissões, instalar hooks, desarmar pre-commit).
- **Fonte:** [permission-modes, Protected paths](https://code.claude.com/docs/en/permission-modes#protected-paths) e [Critical paths](https://code.claude.com/docs/en/permission-modes#critical-paths).
- **Confiança:** confirmado.

Isso conversa direto com guardrails: um hook em `.claude/hooks/` e o `.claude/settings.json` ficam protegidos contra edição silenciosa, a não ser em bypass.

### 3.8 Sandbox do Bash

- **O que é:** isolamento no nível do SO (Seatbelt no macOS, bubblewrap no Linux e WSL2) para comandos Bash, PowerShell e Monitor e seus filhos. Escrita liberada só no diretório de trabalho e no temp; leitura no disco todo (inclusive `~/.ssh`, a não ser que se configure `sandbox.credentials` ou `denyRead`); rede via proxy, sem domínio liberado por padrão. Dentro do workspace, o sandbox ainda nega escrita em `.claude`, `.git/hooks`, `.git/config` e afins, sem exceção possível.
- **Por que existe:** a boundary "holds regardless of what the model chose to run", ao contrário das regras por texto. É a resposta oficial para os bypasses da seção 3.2.
- **Fonte:** [sandboxing](https://code.claude.com/docs/en/sandboxing).
- **Confiança:** confirmado.

Limites que a doc lista:

- Só cobre Bash. Read, Edit, Write, MCP e hooks rodam fora. A doc diz que o sandbox do Bash "is not sufficient for fully unattended runs".
- Há um escape: o Claude pode tentar de novo fora do sandbox, passando pelo fluxo de permissão. Para fechar, `allowUnsandboxedCommands: false` (strict sandbox mode).
- Liberar domínios amplos como `github.com` abre caminho de exfiltração (domain fronting).
- `enableWeakerNestedSandbox` (para rodar dentro de Docker) enfraquece bastante a proteção.

Para git, uma consequência indireta: se `github.com` não estiver liberado, `git push` falha por rede, seja qual for o texto do comando.

### 3.9 Ambientes isolados: dev container, container, VM, sandbox runtime

- **O que é:** isolar o processo inteiro do Claude Code. A doc compara: sandbox do Bash (só comandos), sandbox runtime `@anthropic-ai/sandbox-runtime` (o processo todo, sem Docker), dev container, container próprio, VM e cloud sessions. Para rodar sem supervisão com `--dangerously-skip-permissions` ou auto mode, recomenda dev container, container, VM ou sandbox runtime. O dev container de referência roda como usuário não root e traz um `init-firewall.sh` que restringe a saída de rede.
- **Por que existe:** "With no prompts to catch mistakes, the isolation boundary you choose is what protects your system."
- **Fonte:** [sandbox-environments](https://code.claude.com/docs/en/sandbox-environments); [devcontainer](https://code.claude.com/docs/en/devcontainer); [dev container de referência](https://github.com/anthropics/claude-code/tree/main/.devcontainer).
- **Confiança:** confirmado.

Ressalvas oficiais que importam para git:

- O workspace montado continua gravável e as mudanças aparecem no host. O container não protege o próprio repositório de um `reset --hard`.
- Em bypass, o container não impede exfiltração do que estiver dentro dele, inclusive as credenciais do Claude Code em `~/.claude`.
- A doc recomenda não montar `~/.ssh` nem credenciais de nuvem e preferir "repository-scoped or short-lived tokens". É daí que vem a defesa mais forte contra push indesejado: o container sem credencial de push.
- Managed settings em `/etc/claude-code/managed-settings.json` dentro da imagem têm precedência máxima, mas quem tem escrita no repositório pode mudar o Dockerfile.

### 3.10 Headless e modo não interativo

- **O que é:** `claude -p` roda sem TUI. `--allowedTools` e `--disallowedTools` passam regras por run. `--permission-prompts none` nega tudo que pediria aprovação e avisa o Claude para não tentar de novo. `--bare` pula a descoberta de hooks, skills, plugins, MCP e CLAUDE.md.
- **Por que existe:** automação em scripts, CI e loops.
- **Fonte:** [headless](https://code.claude.com/docs/en/headless); [cli-reference](https://code.claude.com/docs/en/cli-reference).
- **Confiança:** confirmado.

Três armadilhas para quem desenhar guardrails:

1. **`--bare` desliga os hooks de guarda, inclusive os passados por `--settings`.** A doc diz só que ele pula a descoberta de hooks e que settings entram por `--settings`; o `claude --help` diz "skip hooks (those defined in settings...)". Testei no Claude Code 2.1.288, em 2026-10-02: um hook vindo de `--settings` não dispara com `--bare` e dispara sem ele. Para um loop AFK isolado com hook, use `--setting-sources "" --settings <arquivo>`: carrega só os hooks do arquivo e pula os do usuário e do projeto (também testado, com PreToolUse numa sessão `-p` real). A doc avisa que `--bare` "will become the default for `-p` in a future release". Correção feita em 2026-10-02; a versão anterior desta nota dizia que `--settings` bastava.
2. **Em `-p` não há diálogo de workspace trust.** Os hooks do `.claude/settings.json` de qualquer repositório rodam direto. Em repositório de terceiros, a doc sugere `--bare`, `--setting-sources user` ou `--settings '{"disableAllHooks": true}'`.
3. **`disableAllHooks` do projeto vence o do usuário** por precedência. Um repositório pode religar ou desligar hooks com um `false` ou `true` no próprio settings. Só managed settings protegem hooks de serem desligados.

### 3.11 Worktrees

- **O que é:** `claude --worktree <nome>` cria um checkout em `.claude/worktrees/<nome>/` numa branch nova. Enquanto a sessão está isolada, o Claude Code bloqueia edição de arquivos do checkout principal, comandos cujo diretório resolve para ele e redirecionamentos do git para ele (`git -C`, `--git-dir`, `GIT_DIR`, `cd`), além de comandos cujo alvo ele não consegue verificar. Vale para subagents. `/batch` dá um worktree para cada subagent.
- **Por que existe:** sessões paralelas sem colisão e uma área descartável para o agente.
- **Fonte:** [worktrees](https://code.claude.com/docs/en/worktrees).
- **Confiança:** confirmado.

Limites:

- O `.git` é compartilhado. Commits, refs e push afetam o repositório inteiro; o worktree não protege branches nem o remoto.
- Aprovações "don't ask again" num worktree são salvas no `.claude/settings.local.json` do checkout principal e valem para todos os worktrees.

### 3.12 Verificação: testes, Stop hook, /goal e revisor com contexto limpo

- **O que é:** a doc de boas práticas manda dar ao Claude "a check it can run" (testes, build, lint) e escalonar quão duro ele trava a parada. Pode ser só o prompt, um `/goal` reavaliado a cada turno, um Stop hook que impede o fim do turno até o check passar, ou um subagent que tenta refutar o resultado. Para AFK, ela recomenda uma revisão adversarial: um subagent com contexto limpo que só vê o diff e os critérios.
- **Por que existe:** "It's the difference between a session you watch and one you walk away from." Sem check, "looks done" é o único sinal, e o humano vira o loop de verificação.
- **Fonte:** [best-practices, Give Claude a way to verify its work](https://code.claude.com/docs/en/best-practices#give-claude-a-way-to-verify-its-work) e [Add an adversarial review step](https://code.claude.com/docs/en/best-practices#add-an-adversarial-review-step); [hooks, Stop](https://code.claude.com/docs/en/hooks#stop).
- **Confiança:** confirmado.

Dois detalhes:

- O Stop hook tem um teto: o Claude Code ignora o hook depois de 8 bloqueios seguidos sem progresso, e o script deve checar `stop_hook_active`.
- A doc alerta que um revisor sempre acha alguma coisa. Sugere pedir só lacunas que afetem correção ou requisitos, para não cair em over-engineering.

### 3.13 Escopos de settings

- **O que é:** quatro escopos. User (`~/.claude/settings.json`, todos os projetos da máquina), project (`.claude/settings.json`, commitado), local (`.claude/settings.local.json`, fora do git) e managed (organização, não sobrescrevível). Listas como `permissions.deny` e hooks se somam entre escopos em vez de se substituir. Uma deny em qualquer escopo bloqueia uma allow em qualquer outro.
- **Por que existe:** separar preferência pessoal, política do time e política da organização.
- **Fonte:** [settings](https://code.claude.com/docs/en/settings); [permissions, Settings precedence](https://code.claude.com/docs/en/permissions#settings-precedence).
- **Confiança:** confirmado.

Consequência para o desenho:

- Um guardrail global (user) protege todos os seus projetos, mas não chega a quem clonar o repositório.
- Um guardrail no projeto viaja com o repositório, mas só vale nos projetos que o têm.
- As allow rules do projeto só valem depois do workspace trust; deny e ask valem sempre.

## 4. A skill git-guardrails-claude-code do Matt Pocock

- **O que é:** skill que instala um hook PreToolUse com `matcher: "Bash"` apontando para `block-dangerous-git.sh`. A skill pergunta o escopo (projeto ou global), copia o script para `.claude/hooks/` ou `~/.claude/hooks/`, faz merge no settings.json, oferece customizar a lista e testa com `echo '{"tool_input":{"command":"git push origin main"}}' | <script>`, esperando exit 2.
- **Por que existe:** impedir que o agente faça operações git destrutivas ou irreversíveis. A mensagem de bloqueio diz ao Claude que "The user has prevented you from doing this", para ele não insistir.
- **Fonte:** [mattpocock/skills, skills/misc/git-guardrails-claude-code](https://github.com/mattpocock/skills/tree/main/skills/misc/git-guardrails-claude-code) (SKILL.md e scripts/block-dangerous-git.sh).
- **Confiança:** relato (um autor; o padrão de hook com exit 2 é confirmado pela doc).

O script lê o comando com `jq -r '.tool_input.command'` e testa cada padrão com `grep -qE`: `git push`, `git reset --hard`, `git clean -fd`, `git clean -f`, `git branch -D`, `git checkout \.`, `git restore \.`, `push --force` e `reset --hard`. Se casar, escreve no stderr e sai com 2.

### Teste local do script

Rodei o script original com JSON simulado no stdin. Exit 2 é bloqueio, exit 0 é liberação:

| Comando | Exit | Observação |
| :- | :- | :- |
| `git push origin main` | 2 | Bloqueia, como esperado |
| `git -C . push` | 0 | Passa: opção global entre `git` e o subcomando |
| `git -c x=y push` | 0 | Passa, mesmo motivo |
| `git  push` (dois espaços) | 0 | Passa: o padrão exige um espaço só |
| `sh -c 'git pu''sh'` | 0 | Passa: concatenação de aspas |
| `git reset  --hard` | 0 | Passa: espaço duplo |
| `git clean -xdf` | 0 | Passa: flags em outra ordem |
| `git branch --delete --force x` | 0 | Passa: forma longa de `-D` |
| `git checkout -- .` | 0 | Passa: o padrão espera `checkout .` colado |
| `git restore --staged --worktree .` | 0 | Passa |
| `git stash drop` | 0 | Fora da lista |
| `git commit --amend` | 0 | Fora da lista |
| `git update-ref -d refs/heads/main` | 0 | Fora da lista |
| `git switch -f main` | 0 | Fora da lista; descarta mudanças locais |
| `rm -rf .git` | 0 | Fora da lista |
| `gh pr merge 3` | 0 | Fora da lista; age no remoto sem `git push` |
| `git status && echo 'git push is blocked'` | 2 | Falso positivo: casa o texto dentro de uma string |
| `git push origin main` sem `jq` no PATH | 0 | Falha aberta: `jq` não encontrado, comando vazio, exit 0 |

### Limites observados

- **Regex sobre texto cru.** Mesma fragilidade que a doc aponta para as Bash rules (seção 3.2), e às vezes maior: as Bash rules ao menos separam compound commands e removem wrappers, o script não.
- **Falha aberta.** Sem `jq`, com script sem `chmod +x` ou com caminho errado no settings, nada é bloqueado e o único sinal é um aviso de hook error (seção 3.3).
- **Lista curta.** Ficam de fora `stash drop` e `stash clear`, `commit --amend`, `rebase`, `update-ref`, `switch -f`, `rm -rf .git` e ações no remoto via `gh`.
- **Bloqueia todo push.** É uma escolha deliberada e forte. Combina com AFK (o humano revisa e empurra), mas atrapalha um fluxo interativo em que o push é desejado.
- **Defesa contra o modelo distraído, não contra o adversário.** O hook funciona porque o Claude normalmente escreve `git push` do jeito canônico e respeita o bloqueio. Ele não segura um prompt injection que tente contornar.

## 5. Outras ferramentas da comunidade

### 5.1 destructive_command_guard (dcg)

- **O que é:** binário em Rust instalado como hook PreToolUse em vários agentes. Faz parse e normalização (tira caminho absoluto, `/usr/bin/git` vira `git`), olha dentro de heredocs e de `bash -c` e `python -c`, e distingue dado de execução (`grep "rm -rf"` passa). Tem packs modulares (git, filesystem, banco, nuvem). Por padrão, bloqueia `reset --hard`, `clean -f` e force push, mas **deixa passar `git push` comum** e `--force-with-lease`. Um pack `strict_git` opcional bloqueia rebase e reescrita de histórico. Tem escape `DCG_BYPASS=1` e allowlist. Por padrão falha aberto em entrada que não consegue parsear; `DCG_FAIL_CLOSED=1` inverte.
- **Por que existe:** nasceu de um script Python de Jeffrey Emanuel contra agentes que "occasionally run catastrophic commands that destroy hours of uncommitted work".
- **Fonte:** [Dicklesworthstone/destructive_command_guard](https://github.com/Dicklesworthstone/destructive_command_guard) (README).
- **Confiança:** relato (um projeto), mas reforça a convenção de hook PreToolUse para git destrutivo.

### 5.2 CC Safety Net

- **O que é:** hook em Node para vários agentes. Faz parse do que o comando faz, e segundo o README "Wrapping the command or reordering flags does not hide it". Bloqueia `reset --hard`, force push, `rm -rf` em alvos perigosos e leitura de segredos (`.env`, `~/.ssh`, `~/.aws`). Tem presets Standard, Strict (bloqueia comando dinâmico ou que não consegue parsear) e Paranoid, além de `doctor` com autoteste, `explain` e log local de auditoria. Diz nos limites que "does not set filesystem permissions, watch network egress, or contain a process".
- **Por que existe:** mesma dor, com foco em resistir a formas alternativas de escrever o comando.
- **Fonte:** [kenryu42/cc-safety-net](https://github.com/kenryu42/cc-safety-net) (README).
- **Confiança:** relato.

### 5.3 Exemplos oficiais de settings

- **O que é:** três arquivos no repositório da Anthropic. `settings-lax.json` desliga o bypass. `settings-strict.json` desliga o bypass, põe `ask` em todo Bash, nega WebFetch e WebSearch e aceita só hooks e regras do managed. `settings-bash-sandbox.json` exige sandbox sem escape (`allowUnsandboxedCommands: false`). O README avisa que são "community-maintained snippets which may be unsupported or incorrect".
- **Por que existe:** pontos de partida para política de organização.
- **Fonte:** [anthropics/claude-code, examples/settings](https://github.com/anthropics/claude-code/tree/main/examples/settings).
- **Confiança:** confirmado quanto à existência (repositório oficial); o conteúdo é marcado como sem garantia.

### 5.4 O que as três ferramentas de hook têm em comum

Matt, dcg e CC Safety Net usam o mesmo mecanismo: PreToolUse, matcher `Bash` e exit 2 ou JSON `deny`. Também concordam no núcleo: `reset --hard`, `clean -f` e force push. **Convenção.** Divergem em `git push` comum (Matt bloqueia; dcg e CC Safety Net não) e em robustez: regex simples no Matt, parser e normalização nos outros dois.

## 6. Práticas de loop AFK

### 6.1 Ralph, o loop original

- **O que é:** `while :; do cat PROMPT.md | claude-code ; done`, o mesmo prompt repetido. O prompt manda fazer uma coisa só por iteração, com specs em arquivos, um `fix_plan.md` priorizado como lista de tarefas, um arquivo de aprendizados do agente e backpressure por testes, compilação e análise estática.
- **Por que existe:** automatizar desenvolvimento greenfield deixando o agente escolher a próxima tarefa, sem um humano escrevendo prompt novo a cada fase.
- **Fonte:** [Geoffrey Huntley, "Ralph Wiggum as a software engineer"](https://ghuntley.com/ralph/), julho de 2025.
- **Confiança:** relato.

O post original manda o agente fazer `git add -A`, `git commit`, **`git push`** e criar tag a cada build verde. Não menciona sandbox, container, permissões nem segurança. Diz também que não usaria a técnica num código existente ("There's no way in heck would I use Ralph in an existing code base") e que ela exige supervisão de engenheiro experiente.

### 6.2 Ralph na versão do Matt Pocock

- **O que é:** 11 dicas. Começar em HITL (humano no loop) para afinar o prompt e só depois ir para AFK. Definir o escopo como PRD em JSON com critérios de aceite. Manter um `progress.txt` commitado. Usar feedback loops (types, testes, lint, pre-commit) que travam o commit. Passos pequenos. Atacar primeiro as tarefas de risco. Dizer explicitamente se o código é protótipo ou produção. Rodar em Docker sandbox (`docker sandbox run claude`). Sempre limitar iterações ("5-10 iterations for small tasks, or 30-50 for larger ones"). Commit a cada feature.
- **Por que existe:** tornar o Ralph previsível e seguro o bastante para rodar enquanto o autor dorme.
- **Fonte:** [Matt Pocock, "11 Tips For AI Coding With Ralph Wiggum"](https://www.aihero.dev/tips-for-ai-coding-with-ralph-wiggum), janeiro de 2026.
- **Confiança:** relato. Várias dicas coincidem com a doc oficial e com a Anthropic (seção 6.4); nesses pontos vira convenção.

Segundo o post, o Docker sandbox monta só o diretório atual: o agente edita e commita, mas não alcança "your home directory, SSH keys, or system files".

### 6.3 Sandcastle

- **O que é:** biblioteca TypeScript do Matt que orquestra agentes em sandboxes (Docker, Podman, Vercel). Cada agente trabalha num worktree e numa branch, com `maxIterations` (padrão 1) e pipeline implementar-depois-revisar no mesmo sandbox. Os commits são trazidos de volta para o host por uma estratégia de branch configurável. Se o sandbox fecha com mudanças não commitadas, o worktree é preservado.
- **Por que existe:** paralelizar agentes AFK com isolamento e revisão sem montar a infraestrutura à mão.
- **Fonte:** [mattpocock/sandcastle](https://github.com/mattpocock/sandcastle) (README).
- **Confiança:** relato.

Note o desenho: o agente não empurra para o remoto. O orquestrador traz os commits para o host, e o humano decide o resto. É o mesmo princípio do hook que bloqueia `git push`, só que aplicado pela arquitetura.

### 6.4 Harness de agente de longa duração (Anthropic)

- **O que é:** uma sessão inicial prepara o ambiente (`init.sh`, `claude-progress.txt`, lista de features em JSON com `passes: false` e commit inicial). Cada sessão seguinte lê o git log e o progresso, roda um teste básico, implementa "only one feature at a time", testa ponta a ponta e commita. O prompt diz que "It is unacceptable to remove or edit tests".
- **Por que existe:** agentes tendem a tentar fazer tudo de uma vez e a deixar trabalho pela metade entre janelas de contexto. Commits frequentes dão pontos de rollback.
- **Fonte:** [Anthropic Engineering, "Effective harnesses for long-running agents"](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), novembro de 2025.
- **Confiança:** relato (post de engenharia, não doc de produto), mas da mesma organização que mantém o Claude Code.

### 6.5 Práticas que se repetem

| Prática | Fontes que a defendem | Confiança |
| :- | :- | :- |
| Uma tarefa por iteração | Huntley, Matt, Anthropic (long-running) | convenção |
| Arquivo de progresso ou checklist commitado | Huntley (`fix_plan.md`), Matt (`progress.txt`), Anthropic (`claude-progress.txt` mais JSON de features) | convenção |
| Testes e checks como backpressure | Huntley, Matt, Anthropic, doc oficial (seção 3.12) | confirmado |
| Não apagar nem afrouxar testes | Anthropic (long-running); o classificador do auto mode bloqueia afrouxar teste de segurança | confirmado (classificador), relato (regra geral) |
| Commit pequeno por feature | Huntley, Matt, Anthropic | convenção |
| Limite de iterações | Matt, Sandcastle (`maxIterations`) | convenção |
| Container ou sandbox para AFK | Matt, Sandcastle, doc oficial (seção 3.9) | confirmado |
| Worktree e branch por agente | Sandcastle, doc oficial (`--worktree`, `/batch`) | confirmado |
| Revisor com contexto limpo | doc oficial (writer/reviewer, subagent adversarial), Sandcastle (implementar e revisar) | confirmado |
| Começar em HITL, depois AFK | Matt | relato |

## 7. Proteção do lado do servidor

- **O que é:** proteger o remoto em vez do comando. Branch protection ou rulesets no GitHub (bloquear force push e deleção, exigir PR e revisão na `main`) e dar ao agente uma credencial sem permissão de push, ou com escopo de um repositório e vida curta.
- **Por que existe:** é a única camada que nenhuma forma de escrever o comando contorna. Um `git -C . push --force` some no hook mas bate no servidor.
- **Fonte:** recomendação de tokens com escopo e vida curta em [devcontainer](https://code.claude.com/docs/en/devcontainer) (confirmado). Branch protection: [GitHub Docs, About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets) (doc oficial do GitHub, não do Claude Code).
- **Confiança:** confirmado como recurso. Usar isso como guardrail de agente aparece na doc da Anthropic só via tokens; nas fontes de comunidade lidas, aparece de forma indireta (Sandcastle não empurra; Matt bloqueia push).

Limite: não protege nada local. `reset --hard`, `clean -f` e `checkout -- .` destroem trabalho não commitado sem tocar o remoto. Por isso o hook local continua fazendo sentido mesmo com o servidor protegido.

Em paralelo: um hook git local de pre-push protege pouco contra o agente, porque `git push --no-verify` o pula, e o hook mora em `.git/hooks`. A doc protege `.git` e `.husky` contra edição automática (seção 3.7), mas não contra `--no-verify`. O classificador do auto mode trata como risco rodar comando "with a flag that disarms a safety guard". Este parágrafo é inferência minha a partir dessas duas fontes, não uma recomendação explícita delas.

## 8. AFK x sessão interativa

| Aspecto | Interativo | AFK |
| :- | :- | :- |
| Quem pega o erro | O humano, no prompt ou olhando a tela | Só o que estiver automatizado |
| Modo sugerido pela doc | Manual, ou Manual mais sandbox auto-allow, ou auto | `dontAsk` com allowlist exata em CI; auto com `--permission-prompts none`; bypass só dentro de container ou VM |
| `git push` | Pode ficar em `ask` (a doc sugere `permissions.ask` para checkpoint humano) | Bloquear, ou não ter credencial de push no ambiente |
| Git destrutivo local | Hook bloqueia; o humano roda à mão se quiser | Hook bloqueia; o trabalho deve estar commitado em passos pequenos |
| Isolamento | Opcional (sandbox do Bash reduz prompts) | Necessário com bypass; recomendado com auto |
| Hooks carregados | Só depois do workspace trust | Em `-p`, sem trust; com `--bare`, nenhum hook, nem os de `--settings`; com `--setting-sources "" --settings`, só os do arquivo |
| Limites ditos na conversa | Funcionam no auto mode, mas podem sumir na compactação | Não confiar; usar deny rule ou hook |
| Verificação | O humano revisa | Testes, Stop hook ou `/goal`, revisor com contexto limpo, limite de iterações |
| Falha de um hook | O humano vê o aviso de hook error | Ninguém vê; o guardrail some em silêncio |

O ponto mais delicado é a última linha. Em AFK, um hook que falha aberto é pior do que nenhum hook, porque dá falsa segurança.

## 9. Deny rules x hooks

| Critério | Deny rule (`permissions.deny`) | Hook PreToolUse |
| :- | :- | :- |
| Quem aplica | Claude Code, nativo | Seu script, chamado pelo Claude Code |
| Vale em `bypassPermissions` | Sim | Sim |
| Pode ser afrouxado por outro escopo | Não: deny vence allow de qualquer escopo | Um `allow` de hook não vence deny; um hook pode ser desligado por `disableAllHooks` do projeto |
| Compound commands e wrappers | Separa e remove wrappers nativamente | Só se o script fizer |
| Bypasses conhecidos | `git -C`, `git -c`, aspas, caminho absoluto, `sh -c` (tabela oficial) | Os mesmos e outros, conforme o parser (seção 4) |
| Falha | Regra malformada gera aviso na inicialização | Script ausente, exit 1 ou timeout liberam em silêncio |
| Dependências | Nenhuma | `jq`, bash, o binário da ferramenta |
| Expressividade | Prefixo com `*` | Qualquer lógica: parse, contexto, mensagem explicativa, log |
| Mensagem ao modelo | Genérica | Customizável pelo stderr ou `permissionDecisionReason` |
| Carregado com `--bare` | Só via `--settings` | Não carrega, nem via `--settings`; use `--setting-sources "" --settings` sem `--bare` |
| Portabilidade para outros agentes | Só Claude Code; cada agente tem sintaxe própria (seção 12) | O script pode servir a outros agentes que aceitam hooks no formato do Claude Code (dcg e CC Safety Net fazem isso; seção 12) |

As fontes convergem num ponto. Deny rule e hook são a mesma categoria de defesa, decisão sobre o texto antes de executar, e servem contra erro do modelo. Contra comando escrito de outro jeito, a doc oficial manda para sandbox e isolamento.

## 10. Onde as fontes concordam e divergem

**Concordam:**

- `reset --hard`, `clean -f`, force push e descartar mudanças locais (`checkout -- .`, `restore .`) são o núcleo a bloquear. Aparecem no Matt, no dcg, no CC Safety Net e no classificador do auto mode.
- PreToolUse com exit 2 é o mecanismo de comunidade para isso. A doc confirma que ele vale em todos os modos.
- Para AFK sem prompts, a doc, o Matt e o Sandcastle pedem container ou sandbox.
- Testes como backpressure, uma tarefa por vez e commits pequenos aparecem em Huntley, Matt, Anthropic e na doc.
- Regra baseada em texto não é fronteira de segurança. A doc diz isso com todas as letras, e o CC Safety Net também.

**Divergem:**

- **`git push` comum.** O Matt bloqueia sempre. O dcg e o CC Safety Net deixam passar. O classificador do auto mode permite por padrão. O Ralph original manda o agente empurrar e taguear a cada build verde. O Sandcastle não empurra: traz os commits para o host.
- **Robustez do hook.** O Matt usa regex em bash. O dcg e o CC Safety Net fazem parse e normalização e olham dentro de `sh -c`. A doc nem tenta vender hook como fronteira.
- **Falhar aberto ou fechado.** O padrão do Claude Code e do dcg é falhar aberto. O CC Safety Net Strict e o `DCG_FAIL_CLOSED=1` bloqueiam o que não conseguem verificar. O script do Matt falha aberto sem `jq`.
- **Onde instalar.** A skill do Matt deixa o usuário escolher entre projeto e global. Os exemplos oficiais miram managed. O dcg e o CC Safety Net instalam no user global, e o CC Safety Net também versiona a política no repositório (`.cc-safety-net/`).
- **Quão longe o AFK vai.** Huntley diz que não usaria em código existente. O Matt manda começar em HITL. A doc oferece auto mode como padrão para tarefas longas.

## 11. Perguntas abertas para o ticket de desenho

Sem decisão aqui; só o que precisa ser decidido.

**Perfis AFK x interativo**

1. Um perfil só, ou dois (interativo com `push` em `ask` e AFK com `push` bloqueado)? Como o perfil é escolhido: flag, variável de ambiente, `--settings` no loop, arquivo diferente?
2. No perfil interativo, `git push` fica em `ask`, liberado, ou bloqueado como no Matt?
3. A lista de bloqueio fica no núcleo comum (`reset --hard`, `clean -f`, force push, `checkout -- .`, `restore .`, `branch -D`) ou estende para `stash drop` e `stash clear`, `commit --amend`, `rebase`, `update-ref`, `switch -f`, `rm -rf .git` e `gh pr merge`?
4. A skill cobre só git ou também o loop AFK (limite de iterações, progresso, revisor, container), ou isso vira outra skill?

**Global x projeto**

5. Instalar no user (`~/.claude`), no projeto (`.claude/`, viaja com o repositório) ou perguntar, como o Matt faz? Como lidar com o `disableAllHooks` de um projeto vencendo o do usuário?
6. Deny rules, hook ou os dois? Deny rules não têm dependências e não falham em silêncio; o hook dá mensagem melhor e lógica própria.
7. Escrever um script próprio, adaptar o do Matt (MIT) ou recomendar uma ferramenta pronta (dcg, CC Safety Net)? Se for próprio, regex ou parse?
8. Falhar aberto ou fechado quando o script não consegue ler o comando (sem `jq`, JSON inesperado)?
9. A skill deve também sugerir a camada do servidor (branch protection, token sem push) e a do container, ou fica só no Claude Code?
10. Como garantir que o loop AFK não rode com `--bare`, que desliga o hook mesmo passado por `--settings`?

**Como testar o bloqueio**

11. Basta o teste do Matt (JSON no stdin, esperar exit 2), ou o teste deve rodar uma tabela de comandos que precisam bloquear e de comandos que precisam passar, incluindo os bypasses da seção 4 e os falsos positivos?
12. Como testar que o hook está de fato carregado na sessão (e não só que o script funciona isolado)? Por exemplo `/hooks`, `claude doctor` ou uma sessão `-p` de prova num repositório descartável.
13. Como detectar a falha silenciosa (caminho errado, sem `chmod +x`, sem `jq`) num run AFK em que ninguém vê o aviso?
14. Os evals da skill (formato ainda não definido no mapa) entram nesse teste ou ficam separados?

## 12. Guardrails em outros agentes

Pesquisa feita em 2026-10-02. A pergunta: a skill `setting-up-git-guardrails` consegue instalar, por projeto, o bloqueio de git destrutivo nos agentes que o `npx skills` atende, e não só no Claude Code? Fontes: README e código do vercel-labs/skills (via `gh api`), a doc oficial de cada agente, os READMEs e exemplos nos repositórios oficiais do Cline e do Gemini CLI, e os READMEs do dcg e do CC Safety Net.

Essas docs mudam ainda mais rápido que a do Claude Code. Durante a pesquisa: a doc do Codex redireciona para learn.chatgpt.com, o Windsurf virou Devin Desktop (docs.devin.ai), o Kiro trocou o formato de hooks na CLI 3.0 e IDE 1.0, e o Cline levou a doc de hooks para o SDK. Confira cada link antes de implementar.

### 12.1 O que o instalador faz e o que não faz

- **O que é:** o `npx skills add` instala a pasta da skill no diretório de skills de cada agente escolhido. A tabela "Supported Agents" lista cerca de 70 agentes. Muitos dividem `.agents/skills/` no projeto (Amp, Codex, Cursor, Gemini CLI, GitHub Copilot, OpenCode, Cline, Kilo, Droid e outros); o Claude Code usa `.claude/skills/`, o Windsurf `.windsurf/skills/`, o Kiro CLI `.kiro/skills/`, o Roo `.roo/skills/`.
- **Tabela "Compatibility" do README:** `allowed-tools` funciona em quase todos; `context: fork` só no Claude Code; a linha "Hooks" diz Yes só para Claude Code, Cline e Kiro CLI. O README não explica o que conta como "Hooks" nessa linha, e ela está atrás das docs dos agentes: Codex, Cursor, Gemini CLI e Copilot têm hooks hoje e aparecem como No. Leia como "o instalador não garante nada sobre hooks", não como "o agente não tem hooks".
- **O que o código faz:** copia ou cria symlink da pasta para uma cópia canônica, pula `.git`, `__pycache__` e `metadata.json`, e aplica no destino o modo do arquivo de origem (`chmod`), então um `scripts/*.sh` executável chega executável. Além da pasta, grava só os lockfiles (`skills-lock.json` no projeto e `~/.agents/.skill-lock.json` no global). Não achei código que toque settings, hooks ou permissões de agente em `src/installer.ts`, `src/local-lock.ts` e `src/skill-lock.ts`.
- **Fonte:** [vercel-labs/skills](https://github.com/vercel-labs/skills) (README e `src/`).
- **Confiança:** confirmado.

Consequências para o desenho:

- Instalar a skill não instala o guardrail. Quem registra o hook é o agente, ao seguir a skill, editando o arquivo de config de cada agente.
- O caminho do script muda por agente (`.claude/skills/...` ou `.agents/skills/...`), e com symlink aponta para a cópia canônica. Um hook que aponte para dentro da pasta da skill quebra se ela for removida ou movida, e na maioria dos agentes isso falha aberto (tabela da seção 12.2). Copiar o script para um caminho próprio do projeto evita a dependência; é inferência minha, nenhuma fonte trata disso.

### 12.2 Tabela comparativa

"Libera" quer dizer que o comando segue quando o hook sai com outro código, quebra ou estoura o tempo. "Por projeto" é o arquivo que pode ir commitado no repositório.

| Agente | Hook pré-execução | Formato de entrada | Como bloqueia | Deny rules nativas | Onde configura por projeto | Fonte | Confiança |
| :- | :- | :- | :- | :- | :- | :- | :- |
| Claude Code | `PreToolUse`, matcher `Bash` | JSON no stdin, `tool_input.command` | Exit 2 com stderr, ou `hookSpecificOutput.permissionDecision: "deny"`; outro código libera | `permissions.deny`, `Bash(git push *)` | `.claude/settings.json` | Seção 3 | confirmado |
| OpenAI Codex CLI | `PreToolUse`; cobre `Bash`, `apply_patch`, MCP | JSON no stdin, `tool_name: "Bash"`, `tool_input.command`, mais `turn_id` | Exit 2 com stderr, ou `permissionDecision: "deny"`; erro e timeout liberam | Rules (experimental) em Starlark: `prefix_rule(pattern = ["git", "push"], decision = "forbidden")` | `.codex/hooks.json` ou `.codex/config.toml`; rules em `.codex/rules/*.rules`. Só valem com o projeto confiável, e cada hook precisa ser revisado e confiado (por hash) | [hooks](https://learn.chatgpt.com/docs/hooks), [rules](https://learn.chatgpt.com/docs/agent-configuration/rules) | confirmado |
| Cursor (IDE e CLI) | `beforeShellExecution` (shell e MCP) e `preToolUse` genérico; também roda hooks do Claude Code | `beforeShellExecution`: `command`, `cwd`, `sandbox` | Exit 2, ou `{"permission": "deny"}` com `user_message` e `agent_message`; outro código libera, a não ser com `failClosed: true` | Só o Cursor CLI: `permissions.deny` com `Shell(git push)` | `.cursor/hooks.json` (`version: 1`); ou `.claude/settings.json` via Third-Party Imports, ligado por padrão; deny do CLI em `.cursor/cli.json` | [hooks](https://cursor.com/docs/agent/hooks), [third-party hooks](https://cursor.com/docs/reference/third-party-hooks), [CLI permissions](https://cursor.com/docs/cli/reference/permissions) | confirmado |
| Gemini CLI | `BeforeTool`, matcher regex, ferramenta `run_shell_command` | JSON no stdin, `tool_name`, `tool_input.command` | Exit 2 com stderr, ou exit 0 com `{"decision": "deny", "reason": ...}`; outro código só avisa; stdout que não é JSON vira allow | Policy engine em TOML (`commandPrefix`, `decision = "deny"`), mas a camada de workspace (`.gemini/policies/`) está desligada; só user e admin funcionam | `hooks` em `.gemini/settings.json`; o Gemini avisa quando um hook do projeto muda | [hooks](https://geminicli.com/docs/hooks/), [reference](https://geminicli.com/docs/hooks/reference/), [policy engine](https://geminicli.com/docs/reference/policy-engine/) | confirmado |
| GitHub Copilot CLI (e cloud agent) | `preToolUse` (camelCase) ou `PreToolUse` (PascalCase, semântica do Claude) | camelCase: `toolName: "bash"`, `toolArgs.command`; PascalCase: `tool_name` com o nome do Claude e `tool_input` | `{"permissionDecision": "deny", "permissionDecisionReason": ...}`, ou exit 2. **Qualquer outro código não zero também nega**; só timeout libera | Só por sessão: `--deny-tool='shell(git push)'`, que vence `--allow-all`; aprovações ficam em `~/.copilot`, não no projeto | `.github/hooks/*.json` (`version: 1`); também lê `.claude/settings.json` e `.claude/settings.local.json` do repositório | [hooks configuration](https://docs.github.com/en/copilot/reference/hooks-configuration), [allowing tools](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/allowing-tools) | confirmado |
| GitHub Copilot no VS Code (agent, em Preview) | `PreToolUse` | `tool_name`, `tool_input`, `tool_use_id`. O nome da ferramenta de terminal não está documentado; o dcg relata `runTerminalCommand` e `run_in_terminal`, com `tool_input.command` | Exit 2, ou `hookSpecificOutput.permissionDecision: "deny"`; outro código só avisa | Não pesquisado | `.github/hooks/*.json`; `.claude/settings.json` só com `chat.useClaudeHooks`, que a doc diz vir desligado. No formato do Claude o matcher é ignorado: todo hook do evento roda | [hooks](https://code.visualstudio.com/docs/copilot/customization/hooks), [hooks reference](https://code.visualstudio.com/docs/agents/reference/hooks-reference) | confirmado (formato); relato (nome da ferramenta) |
| OpenCode | Sem hook de comando; plugin JS/TS com `tool.execute.before` | `input.tool === "bash"`, `output.args.command` | Lançar um `Error` no plugin | `permission.bash` com glob: `{"*": "ask", "git push *": "deny"}`; a última regra que casa vence | `opencode.json`; plugins em `.opencode/plugins/` | [permissions](https://opencode.ai/docs/permissions/), [plugins](https://opencode.ai/docs/plugins/) | confirmado |
| Windsurf, agora Devin Desktop (Cascade) | `pre_run_command` | JSON no stdin, `tool_info.command_line`, `tool_info.cwd` | Exit 2, o Cascade lê o stderr; outro código libera | Deny list de terminal só de usuário e de time (admin); no modo Turbo ela faz pedir aprovação, não bloqueia | `.devin/hooks.json` (legado `.windsurf/hooks.json`) | [Cascade hooks](https://docs.devin.ai/desktop/cascade/hooks), [terminal](https://docs.devin.ai/desktop/terminal) | confirmado |
| Cline (extensão VS Code) | Arquivo executável `PreToolUse`, sem extensão, com shebang | JSON no stdin, `preToolUse.toolName`, `preToolUse.parameters` (nome da ferramenta de shell não documentado) | Stdout `{"cancel": true, "errorMessage": ...}`; exit code não bloqueia | Não pesquisado | `.clinerules/hooks/PreToolUse`, depois de ligar "Enable Hooks"; sem suporte a Windows | [.clinerules/hooks/README.md](https://github.com/cline/cline/blob/main/.clinerules/hooks/README.md) | confirmado (README no repositório oficial) |
| Cline CLI e SDK | `PreToolUse` em `.cline/hooks/`, ou plugin TS com `beforeTool` | Exemplo oficial: `tool_call.name == "run_commands"`, `tool_call.input.command` | Stdout `{"cancel": true, "errorMessage": ...}` | Não pesquisado | `.cline/hooks/`, `.cline/plugins/` | [sdk/examples/hooks](https://github.com/cline/cline/tree/main/sdk/examples/hooks), [plugins](https://docs.cline.bot/customization/plugins) | relato (exemplo, não referência) |
| Amp | Sem hook de comando; plugin TS com `amp.on('tool.call')` | `amp.helpers.shellCommandFromToolCall(event).command` | Retornar `{action: 'reject-and-continue', message}` | A doc atual de settings não tem regra de shell, só `amp.mcpPermissions` | Plugins em `.amp/plugins/`; settings em `.amp/settings.json` | [plugins](https://ampcode.com/docs/customize/plugins), [configuration](https://ampcode.com/docs/cli/settings) | confirmado |
| Kiro (IDE 1.0+, CLI 3.0+) | `PreToolUse`, matcher `shell` ou `execute_bash` | JSON no stdin, `hook_event_name`, `cwd`, `tool_name`, `tool_input`. A doc só mostra o exemplo de MCP; `tool_input.command` para shell é inferência | Exit 2 com stderr (aba CLI); a aba IDE diz que qualquer código não zero bloqueia | `permissions` com `capability: shell`, `match: ["git push *"]`, `effect: deny`; deny vence sempre e separa compound commands | `.kiro/hooks/*.json` (`version: "v1"`); permissions no `permissions` de `.kiro/agents/*.json`. A camada de workspace fica fora do repositório (`~/.kiro/workspace-roots/<hash>/`) | [hooks](https://kiro.dev/docs/hooks/), [actions](https://kiro.dev/docs/hooks/actions/), [types](https://kiro.dev/docs/hooks/types/), [permissions](https://kiro.dev/docs/permissions/) | confirmado (formato parcial) |

### 12.3 Compatibilidade com o formato do Claude Code

- **Leem o `.claude/settings.json` do repositório:** Cursor (por padrão; troca `Bash` por `Shell` e aceita exit 2 e `hookSpecificOutput`), Copilot CLI (junto com `.github/copilot/settings.json`) e Copilot no VS Code (só com `chat.useClaudeHooks`, e ignorando o matcher). Confirmado. O dcg relata que o Grok também lê e que o VS Code atual já carrega `~/.claude/settings.json` por padrão, o que diverge da doc do VS Code. Relato.
- **Mesmo formato, outro arquivo:** Codex, Gemini CLI e Kiro recebem `tool_name` e `tool_input` e bloqueiam com exit 2. O Gemini tem `gemini hooks migrate --from-claude`, que converte uma vez (`Bash` vira `run_shell_command`), e expõe `CLAUDE_PROJECT_DIR` como alias. O Codex rejeita campos desconhecidos na saída JSON, segundo o dcg; exit 2 evita o problema.
- **Formato próprio:** Cursor nativo (`command`), Copilot camelCase (`toolArgs`), Windsurf (`tool_info.command_line`), Cline (`cancel` no stdout), OpenCode e Amp (plugin TS).

Consequência: um único hook no `.claude/settings.json` já alcança Claude Code, Cursor e Copilot CLI. Mas o mesmo script recebe nomes de ferramenta diferentes (`Bash`, `Shell`, `bash`), e se o hook também estiver na config nativa do agente ele roda duas vezes.

### 12.4 Sandbox por agente

- **Claude Code:** seção 3.8.
- **Codex:** `workspace-write` é o padrão em projeto versionado. Rede desligada por padrão, e `.git`, `.agents` e `.codex` ficam somente leitura dentro do workspace. Fonte: [agent approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security). Confirmado. Inferência minha: isso barra o push (por rede) e o que precisa gravar em `.git` (commit, `reset`, `branch -D`), mas não o que só reescreve a árvore de trabalho, como `checkout -- .` ou `clean -f`.
- **Cursor:** o sandbox de terminal bloqueia rede e acesso a arquivo não autorizado, com `sandbox.json` por projeto; a página não fala de `.git`. Fonte: [terminal](https://cursor.com/docs/agent/terminal). Confirmado quanto à existência.
- **Gemini CLI:** `tools.sandbox` (docker, podman ou perfil Seatbelt) e `tools.sandboxNetworkAccess`, `false` por padrão. Fonte: [configuration](https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/configuration.md). Confirmado.
- **Copilot CLI:** a doc recomenda sandbox local ou sessão na nuvem antes de liberar tudo, sem sandbox embutido descrito. Confirmado.
- **Kiro:** existe a capability `sandbox_network`; não aprofundei.
- **Windsurf, Cline, Amp, OpenCode:** não achei sandbox de comando nas páginas lidas.

### 12.5 Ferramentas multiagente da comunidade

Só o padrão, não para adotar.

- **dcg:** um binário que decide e várias entradas. Detecta o agente pelo payload (`turn_id` para Codex, `hookEventName` em camelCase para Grok, envelope `toolCall` para Antigravity) e troca a saída: para o Codex, só os campos de deny documentados; para o Hermes, `{"decision": "block"}`, porque lá código não zero não interrompe. No Cursor usa um script ponte que falha fechado; no OpenCode, um plugin. Para Aider e Continue diz que não há interceptação e sugere git pre-commit. Instala no escopo do usuário, não do projeto. Relata que os `PreToolUse` do Codex ainda não pegam todo caminho de `unified_exec`. Fonte: [README](https://github.com/Dicklesworthstone/destructive_command_guard). Relato.
- **CC Safety Net:** um comando de hook com flag por agente (`cc-safety-net hook --cursor`), empacotado no formato de cada ecossistema: plugin do Amp, extensão do Gemini, marketplace para Claude Code, Codex e Copilot, plugin do OpenCode. No Cursor grava `failClosed: true`. A política vai versionada em `.cc-safety-net/`. Fontes: [README](https://github.com/kenryu42/cc-safety-net), [installation](https://ccsafetynet.com/docs/installation). Relato.
- **Padrão comum:** um núcleo que decide e adaptadores finos de entrada e saída por agente. O agente é identificado pelo formato do payload (dcg) ou por uma flag explícita no comando registrado (CC Safety Net). Convenção (dois projetos independentes).

### 12.6 Conclusão prática: adaptadores mínimos

Exit 2 com motivo no stderr bloqueia em Claude Code, Codex, Gemini CLI, Cursor, Copilot (CLI e VS Code), Windsurf e Kiro. Então o script em bash precisa variar quase só na leitura da entrada. Adaptadores mínimos:

| Adaptador | Agentes | Onde está o comando | Sinal de bloqueio | Falhar fechado |
| :- | :- | :- | :- | :- |
| Formato Claude | Claude Code, Codex, Gemini CLI, Kiro, Copilot PascalCase, VS Code, Cursor via `.claude` | `.tool_input.command` | Exit 2 com stderr | Exit 2 também em erro de parse |
| Cursor nativo | Cursor | `.command` | Exit 2 | Exit 2, mais `failClosed: true` no `hooks.json` para crash e timeout |
| Copilot camelCase | Copilot CLI e cloud agent | `.toolArgs.command` | Exit 2 | Já nega em qualquer código não zero |
| Windsurf | Windsurf, Devin Desktop | `.tool_info.command_line` | Exit 2 | Exit 2 em erro de parse |
| Cline | Cline (extensão) | `.preToolUse.parameters.command` | Stdout `{"cancel": true, "errorMessage": "..."}` | O script precisa pegar todo erro e imprimir `cancel`; exit code não bloqueia |
| Plugin TS | OpenCode, Amp | `output.args.command`, `shellCommandFromToolCall(event)` | Wrapper que chama o script e converte exit 2 em `throw` ou `reject-and-continue` | Tratar falha ao chamar o script como bloqueio |

Dois cuidados que valem para todos:

1. **Filtrar pelo nome da ferramenta dentro do script.** O VS Code ignora o matcher no formato do Claude, o `preToolUse` do Cursor é genérico, e no Codex o `apply_patch` também traz `tool_input.command`, com o texto do patch. Nomes de shell vistos: `Bash`, `Shell`, `bash`, `run_shell_command`, `execute_bash`, `shell`, `runTerminalCommand`, `run_in_terminal`.
2. **Ligar o hook no projeto pede um passo do usuário em vários agentes:** confiar o hook no `/hooks` do Codex, aceitar o aviso de fingerprint do Gemini, ligar "Enable Hooks" no Cline, ligar `chat.useClaudeHooks` no VS Code. Sem esse passo o guardrail não roda, e nada avisa num run AFK.

Onde o hook local não resolve sozinho:

- **Sem hook de shell por projeto:** OpenCode e Amp só por plugin TS. O OpenCode compensa com deny nativa por projeto (`opencode.json`). O Amp não tem regra de shell nativa.
- **Sem deny nativa por projeto:** Gemini CLI (workspace policies desligadas), Copilot CLI (só flag por sessão), Windsurf (deny list de usuário ou time, e só pede aprovação). Nesses fica só o hook.
- **Sem proteção local nenhuma:** Cline no Windows. Pelos relatos do dcg, também Aider e Continue. Os outros agentes da lista do instalador (Zed, Warp, Roo Code, Goose, Junie e afins) não foram verificados aqui. Para eles sobram a camada do servidor (seção 7) e o isolamento.

Perguntas novas para o ticket de desenho:

1. Quais agentes a skill suporta na primeira versão? Um recorte natural: os que bloqueiam com exit 2 e leem `tool_input.command`.
2. O script fica dentro da pasta da skill (caminho varia por agente e pode sumir num `npx skills remove`) ou é copiado para um caminho fixo do projeto?
3. Registrar só no `.claude/settings.json` e aproveitar a compatibilidade (Cursor, Copilot CLI) ou sempre na config nativa de cada agente, evitando execução dupla?
4. OpenCode e Amp entram com wrapper TS, ou só com a deny nativa do OpenCode e um aviso de que o Amp fica sem guardrail local?

## 13. Fontes

Doc oficial do Claude Code (consultada em 2026-10-01):

- Permissions: https://code.claude.com/docs/en/permissions
- Permission modes: https://code.claude.com/docs/en/permission-modes
- Hooks reference: https://code.claude.com/docs/en/hooks
- Hooks guide: https://code.claude.com/docs/en/hooks-guide
- Settings: https://code.claude.com/docs/en/settings
- Sandboxing: https://code.claude.com/docs/en/sandboxing
- Sandbox environments: https://code.claude.com/docs/en/sandbox-environments
- Dev containers: https://code.claude.com/docs/en/devcontainer
- Headless: https://code.claude.com/docs/en/headless
- CLI reference: https://code.claude.com/docs/en/cli-reference
- Worktrees: https://code.claude.com/docs/en/worktrees
- Best practices: https://code.claude.com/docs/en/best-practices
- Security: https://code.claude.com/docs/en/security
- Exemplos de settings: https://github.com/anthropics/claude-code/tree/main/examples/settings
- Dev container de referência: https://github.com/anthropics/claude-code/tree/main/.devcontainer

Anthropic Engineering:

- Effective harnesses for long-running agents: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents

Matt Pocock:

- Skill git-guardrails-claude-code: https://github.com/mattpocock/skills/tree/main/skills/misc/git-guardrails-claude-code
- 11 Tips For AI Coding With Ralph Wiggum: https://www.aihero.dev/tips-for-ai-coding-with-ralph-wiggum
- Sandcastle: https://github.com/mattpocock/sandcastle

Comunidade:

- Geoffrey Huntley, Ralph: https://ghuntley.com/ralph/
- destructive_command_guard: https://github.com/Dicklesworthstone/destructive_command_guard
- CC Safety Net: https://github.com/kenryu42/cc-safety-net

Outros agentes (consultados em 2026-10-02, seção 12):

- vercel-labs/skills, README e código: https://github.com/vercel-labs/skills
- Codex, hooks: https://learn.chatgpt.com/docs/hooks
- Codex, rules: https://learn.chatgpt.com/docs/agent-configuration/rules
- Codex, approvals e sandbox: https://learn.chatgpt.com/docs/agent-approvals-security
- Cursor, hooks: https://cursor.com/docs/agent/hooks
- Cursor, third-party hooks: https://cursor.com/docs/reference/third-party-hooks
- Cursor, CLI permissions: https://cursor.com/docs/cli/reference/permissions
- Cursor, terminal e sandbox: https://cursor.com/docs/agent/terminal
- Gemini CLI, hooks: https://geminicli.com/docs/hooks/
- Gemini CLI, hooks reference: https://geminicli.com/docs/hooks/reference/
- Gemini CLI, policy engine: https://geminicli.com/docs/reference/policy-engine/
- Gemini CLI, configuration: https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/configuration.md
- Gemini CLI, migração de hooks do Claude: https://github.com/google-gemini/gemini-cli/blob/main/packages/cli/src/commands/hooks/migrate.ts
- GitHub Copilot, hooks configuration: https://docs.github.com/en/copilot/reference/hooks-configuration
- GitHub Copilot CLI, allowing tools: https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/allowing-tools
- VS Code, agent hooks: https://code.visualstudio.com/docs/copilot/customization/hooks
- VS Code, hooks reference: https://code.visualstudio.com/docs/agents/reference/hooks-reference
- OpenCode, permissions: https://opencode.ai/docs/permissions/
- OpenCode, plugins: https://opencode.ai/docs/plugins/
- Windsurf (Devin Desktop), Cascade hooks: https://docs.devin.ai/desktop/cascade/hooks
- Windsurf (Devin Desktop), terminal: https://docs.devin.ai/desktop/terminal
- Cline, hooks da extensão: https://github.com/cline/cline/blob/main/.clinerules/hooks/README.md
- Cline, exemplos de hooks do SDK: https://github.com/cline/cline/tree/main/sdk/examples/hooks
- Cline, plugins: https://docs.cline.bot/customization/plugins
- Amp, plugins: https://ampcode.com/docs/customize/plugins
- Amp, configuration: https://ampcode.com/docs/cli/settings
- Kiro, hooks: https://kiro.dev/docs/hooks/
- Kiro, hook actions: https://kiro.dev/docs/hooks/actions/
- Kiro, hook types: https://kiro.dev/docs/hooks/types/
- Kiro, permissions: https://kiro.dev/docs/permissions/
- CC Safety Net, installation: https://ccsafetynet.com/docs/installation

Outras:

- GitHub Docs, rulesets: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
- Docker Sandboxes: https://docs.docker.com/ai/sandboxes/
