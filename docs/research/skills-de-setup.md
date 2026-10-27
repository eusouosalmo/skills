# Skills de setup: onde guardar a configuração por usuário de um kit de skills

Resumo: o Claude Code tem, desde as versões recentes, um mecanismo oficial para pedir valores ao usuário: o `userConfig` do `plugin.json`, com tipos `directory` e `file`, gravado em `pluginConfigs` no `settings.json` do usuário e substituído no corpo das skills como `${user_config.KEY}`. Ele vale só para skills carregadas como plugin do Claude Code: a SPEC do Agent Skills e o `npx skills` não têm nada equivalente, e uma skill instalada fora do plugin recebe o `${user_config.KEY}` como texto literal. Como este repo distribui pelos dois caminhos, e o plugin só leva skills `beta` e `stable`, o `userConfig` não substitui um arquivo de configuração legível por qualquer agente; no máximo complementa, resolvendo para quem usa o plugin o problema de achar esse arquivo. Na comunidade, a skill de setup chamada só pelo usuário, que explora antes de perguntar, recomenda um valor, mostra o rascunho e atualiza no lugar quando roda de novo, é padrão do mattpocock/skills e de plugins menores; onde gravar varia (arquivo no repo, `~/.config/<kit>/`, `userConfig`).

Pesquisa feita em 2026-10-19, para o desenho da skill de setup que grava os caminhos (arquivo de estilo, design system, pasta de vídeos, pasta de roteiros, pasta de projetos do CapCut) numa seção "Caminhos" do `estilo.md`. Complementa [versionamento-e-distribuicao.md](versionamento-e-distribuicao.md) (plugin, `npx skills`, nomes com prefixo, quem instala pelos dois caminhos), [orquestracao-de-skills.md](orquestracao-de-skills.md) (seções 2.2, 3 e 4: skill user-invoked, instalador sem dependências, conferir o que está instalado) e [escrita-de-skills.md](escrita-de-skills.md) (seções 5.2 e 5.5: `disable-model-invocation` e campos só do Claude Code). Esses pontos aparecem aqui só por referência.

## Sumário

1. [Fontes e método](#1-fontes-e-método)
2. [userConfig no plugin do Claude Code](#2-userconfig-no-plugin-do-claude-code)
3. [Variáveis no corpo da skill](#3-variáveis-no-corpo-da-skill)
4. [Fora do plugin: SPEC e npx skills](#4-fora-do-plugin-spec-e-npx-skills)
5. [Outros lugares oficiais para estado do usuário](#5-outros-lugares-oficiais-para-estado-do-usuário)
6. [Skills de setup na comunidade](#6-skills-de-setup-na-comunidade)
7. [Riscos](#7-riscos)
8. [Onde as fontes concordam e divergem](#8-onde-as-fontes-concordam-e-divergem)
9. [O que isso sugere para a skill de setup](#9-o-que-isso-sugere-para-a-skill-de-setup)
10. [Perguntas abertas](#10-perguntas-abertas)
11. [Fontes](#11-fontes)

## 1. Fontes e método

| Sigla | Fonte | Tipo |
| - | - | - |
| MAN | [Plugin manifest reference](https://code.claude.com/docs/en/plugins/manifest-reference) (o mesmo conteúdo de [plugins-reference](https://code.claude.com/docs/en/plugins-reference)), seções User configuration e Environment variables | doc oficial Claude Code |
| CMP | [Plugin components](https://code.claude.com/docs/en/plugins/components), seções "Ask the user for configuration values" e "Reference plugin paths and store data" | doc oficial Claude Code |
| CLI | [Plugin CLI reference](https://code.claude.com/docs/en/plugins/cli-reference): `plugin install --config`, `plugin configure`, o que o uninstall apaga | doc oficial Claude Code |
| TS | [Plugin troubleshooting](https://code.claude.com/docs/en/plugins/troubleshooting), "The userConfig dialog never appears" | doc oficial Claude Code |
| SET | [Settings reference](https://code.claude.com/docs/en/settings-reference), chave `pluginConfigs` | doc oficial Claude Code |
| CC | [Extend Claude with skills](https://code.claude.com/docs/en/skills), "Available string substitutions" e "Control who invokes a skill" | doc oficial Claude Code |
| MEM | [How Claude remembers your project](https://code.claude.com/docs/en/memory), `~/.claude/CLAUDE.md` e imports com `@` | doc oficial Claude Code |
| SPEC | [Agent Skills specification](https://agentskills.io/specification) | especificação aberta |
| BP | [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | doc oficial Anthropic |
| VL | [vercel-labs/skills](https://github.com/vercel-labs/skills): README, `docs/commands.md`, `docs/creating-skills.md`, `docs/troubleshooting.md`, `docs/agents.md` | doc oficial do instalador |
| WSL | Microsoft, [Working across file systems](https://learn.microsoft.com/en-us/windows/wsl/filesystems) e [wsl.conf](https://learn.microsoft.com/en-us/windows/wsl/wsl-config) | doc oficial Microsoft |
| MP | [mattpocock/skills](https://github.com/mattpocock/skills): `setup-matt-pocock-skills/SKILL.md`, `docs/engineering/setup-matt-pocock-skills.md`, `.agents/adr/0001-explicit-setup-pointer-only-for-hard-dependencies.md`, `.out-of-scope/setup-skill-verify-mode.md` (lidos no `main` em 2026-10-19) | comunidade |
| SP | [obra/superpowers](https://github.com/obra/superpowers): `using-git-worktrees`, `using-superpowers`, `.claude-plugin/plugin.json` | comunidade |
| AN | [anthropics/skills](https://github.com/anthropics/skills): `brand-guidelines`, `internal-comms` | exemplos da Anthropic, não doc |
| LW | [MehmetGoekce/llm-wiki](https://github.com/MehmetGoekce/llm-wiki) (149 estrelas): `plugin.json`, `SKILL.md`, `setup.sh`, `CONTRIBUTING.md` | comunidade |
| VT | [viticci/shortcuts-playground-plugin](https://github.com/viticci/shortcuts-playground-plugin) (cerca de 1.150 estrelas): `claude/.claude-plugin/plugin.json` | comunidade |
| PO | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official), plugin `code-modernization` | plugin oficial da Anthropic (exemplo, não doc) |
| PW | [kaneyxx/paper-wiki](https://github.com/kaneyxx/paper-wiki) e [jason-hchsieh/claude-ntfy](https://github.com/jason-hchsieh/claude-ntfy), `skills/setup/SKILL.md` (repos sem estrelas) | comunidade, peso baixo |

As páginas oficiais foram baixadas em Markdown em 2026-10-19 e lidas por busca nos trechos relevantes; as da comunidade, pelo `gh api`. Os exemplos com `userConfig` vieram de uma busca de código no GitHub (`"userConfig" "directory" filename:plugin.json`). Níveis de confiança, como nas outras notas:

- **confirmado:** está em doc oficial (MAN, CMP, CLI, TS, SET, CC, MEM, SPEC, BP, VL, WSL).
- **convenção:** vários autores independentes fazem igual.
- **relato:** um autor faz ou afirma. Tudo da comunidade é anedótico, mesmo quando o repo é grande.

## 2. userConfig no plugin do Claude Code

### 2.1 O que é

- **O que é:** a chave `userConfig` do `plugin.json` "declares values Claude Code prompts the user for when the plugin is enabled, so users don't edit `settings.json` themselves" (MAN). Cada opção é um objeto estrito com `type` (`string`, `number`, `boolean`, `directory` ou `file`), `title` e `description` obrigatórios, e `required`, `default`, `options`, `multiple`, `sensitive`, `min` e `max` opcionais. Chave desconhecida dentro de uma opção faz o plugin não carregar.
- **Para este kit:** os tipos `directory` e `file` existem justamente para caminhos. Uma opção por pasta (vídeos, roteiros, projetos do CapCut) e por arquivo (estilo, design system) caberia no formato.
- **Exemplos reais:** o LW declara uma única opção `wiki_path` do tipo `directory`, `required: true`; o VT declara `output_dir` do tipo `directory` com fallback descrito no texto ("Leave blank to fall back to ~/Documents/Shortcuts Playground"); o PO, plugin oficial da Anthropic, usa `string` com `default` relativo ao workspace (`"legacyDir": "legacy"`). Relato.
- **Confiança:** confirmado (MAN, CMP).

### 2.2 Quando o usuário é perguntado

- **O que é:** o diálogo faz parte da interface interativa `/plugin` e abre para opções ainda não definidas quando o usuário instala pelo `/plugin`, roda `/plugin install` numa sessão ou habilita o plugin na aba Installed. `/plugin configure <plugin>@<marketplace>` reabre o diálogo a qualquer momento. Já `claude plugin install` no shell "never prompts for `userConfig` values": aceita `--config KEY=VALUE` ou, depois, `claude plugin configure --values-stdin`, e avisa `N userConfig options not yet set` (CMP, TS, CLI). Cada opção não sensível aparece também como linha no `/config` (MAN, a partir da v2.1.269).
- **O que a doc não diz:** o que acontece quando uma atualização do plugin acrescenta uma opção nova. O texto só garante o diálogo na instalação, na habilitação e no `configure`.
- **Confiança:** confirmado; a lacuna sobre atualização é inferência da ausência.

### 2.3 Onde o valor fica

- **O que é:** valores não sensíveis vão para `pluginConfigs` no `settings.json` do usuário, por ID do plugin (`"deployer@acme-tools": {"options": {...}}`); escopo `user` ou `managed` (SET). Sensíveis vão para o Keychain no macOS ou para `~/.claude/.credentials.json` (SET).
- **Ciclo de vida:** desinstalar o plugin do último escopo onde ele está instalado apaga as opções salvas e a pasta de dados, salvo `--keep-data` para os dados (CLI). Remover o marketplace também apaga (CLI).
- **Consequência:** o valor fica fora de qualquer repo, por máquina e por usuário. Não viaja para outra máquina sozinho, como qualquer coisa em `~/.claude/settings.json`.
- **Confiança:** confirmado.

### 2.4 Como a skill lê

- **O que é:** `${user_config.KEY}` é substituído "in MCP server config, LSP server config, exec-form hook `args`, and skill and agent content. In skill and agent content, only non-sensitive values are substituted, and a sensitive value there becomes a placeholder" (MAN). Para hooks, também vira variável de ambiente `CLAUDE_PLUGIN_OPTION_<KEY>` (MAN). A substituição é no texto da skill quando ela carrega; as variáveis "aren't present in the environment of commands Claude runs through the Bash tool" (MAN), então um script da skill só recebe o caminho se a skill o passar como argumento.
- **Valor não definido:** a doc não diz o que aparece no corpo da skill quando a opção está vazia e não tem `default`. O LW escreve na skill: se a linha "is not a filesystem path but an unexpanded placeholder (it starts with a dollar sign and a brace), stop and tell the user", e nunca adivinhar. Relato, mas é a defesa certa para um comportamento não documentado.
- **Confiança:** confirmado para o mecanismo; o caso vazio não está documentado.

## 3. Variáveis no corpo da skill

- **O que é:** a CC lista as substituições de uma skill: `$ARGUMENTS`, `$N`, `$nome`, `${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}`, `${CLAUDE_SKILL_DIR}`, `${CLAUDE_PROJECT_DIR}`, e, "substituted only in plugin skills", `${CLAUDE_PLUGIN_ROOT}` e `${CLAUDE_PLUGIN_DATA}`. A tabela da CC não cita `${user_config.*}`; quem cita é a MAN, também restrita a conteúdo de plugin.
- **`${CLAUDE_PLUGIN_ROOT}`:** muda a cada atualização do plugin, "so don't write state there" (MAN).
- **`${CLAUDE_PLUGIN_DATA}`:** `~/.claude/plugins/data/<id>/`, sobrevive a atualizações, é apagada no uninstall; a doc a indica para `node_modules`, código gerado e caches (MAN, CMP), não para preferências do usuário.
- **`${CLAUDE_SKILL_DIR}`:** a pasta da própria skill, em qualquer forma de instalação no Claude Code (CC). Serve para achar scripts da skill, não para guardar estado (ver 4.2).
- **Argumentos:** `$ARGUMENTS` deixa o usuário passar um caminho na invocação (`/skill caminho`), sem guardar nada (CC).
- **Confiança:** confirmado.

## 4. Fora do plugin: SPEC e npx skills

### 4.1 A SPEC não tem configuração

- **O que é:** os campos da SPEC são `name`, `description`, `license`, `compatibility`, `metadata` e `allowed-tools`. `compatibility` "Indicates environment requirements (intended product, system packages, network access, etc.)" e não guarda valores. Não há variáveis, nem estado, nem pergunta na instalação (SPEC).
- **Confiança:** confirmado.

### 4.2 O npx skills não pergunta nada e reescreve a pasta

- **O que é:** o README e os docs do VL não têm configuração por usuário para skills; as únicas variáveis de ambiente documentadas são do próprio CLI (`INSTALL_INTERNAL_SKILLS`, `DISABLE_TELEMETRY`, `DO_NOT_TRACK`, `GITHUB_TOKEN`, `GH_TOKEN`). A instalação recomendada cria "symlinks from each agent to a canonical copy", e `npx skills update` atualiza as skills a partir da fonte (VL).
- **Plugin.json lido pelo VL:** o VL lê `.claude-plugin/plugin.json` e `marketplace.json` só para descobrir caminhos de skills ("Plugin Manifest Discovery"); não há menção a `userConfig` (VL, `docs/creating-skills.md`).
- **Consequência:** uma skill instalada pelo `npx skills` recebe `${user_config.KEY}` como texto, porque quem substitui é o Claude Code ao carregar conteúdo de plugin. O LW confirma na prática: o `setup.sh` dele, para quem copia a skill fora do plugin, troca `${user_config.wiki_path}` pelo caminho escolhido no próprio arquivo, e o `CONTRIBUTING.md` avisa que o script "replaces every occurrence in a copied skill". Inferência da MAN e da CC, com relato do LW.
- **Gravar dentro da pasta da skill não serve:** a cópia canônica é reescrita no `update`; e, no uso local deste repo, `scripts/link-skills.sh` liga `~/.agents/skills` e `~/.claude/skills` de volta ao repo, então escrever na pasta da skill é escrever no repo público. Inferência do VL e do script.
- **Confiança:** confirmado que não existe mecanismo; o resto é inferência.

## 5. Outros lugares oficiais para estado do usuário

- **`~/.claude/CLAUDE.md`:** instruções do usuário para todos os projetos, só dele (MEM). Aceita imports `@caminho`, absolutos ou relativos ao arquivo, até quatro níveis; um import em memória de projeto que sai do diretório de trabalho pede aprovação, e os de memória do usuário não (MEM). Um `@/caminho/estilo.md` ali carregaria o arquivo de estilo em toda sessão, inteiro, o que custa contexto em sessões que não são de vídeo. Só Claude Code; outros agentes têm o equivalente deles (`AGENTS.md` global, por exemplo), cada um num lugar.
- **A doc de skills não define estado:** a CC não fala em arquivo de configuração de skill; o que existe é a pasta de dados do plugin (seção 3) e a memória (MEM).
- **Caminhos na BP:** "Always use forward slashes in file paths, even on Windows" e "Unix-style paths work across all platforms" (BP). A CMP diz que, no Windows, as variáveis de plugin substituídas já usam barras normais.
- **Confiança:** confirmado.

## 6. Skills de setup na comunidade

Tudo nesta seção é anedótico.

### 6.1 mattpocock/skills: `setup-matt-pocock-skills`

- **O que pergunta:** três coisas, por repo: onde ficam as issues (GitHub, GitLab, Markdown local ou outro descrito em prosa), o vocabulário de labels de triagem (só se a skill `triage` estiver instalada) e o layout dos docs de domínio (single-context por padrão, multi-context só se houver sinais de monorepo).
- **Como pergunta:** `disable-model-invocation: true`. Primeiro explora (`git remote -v`, `CLAUDE.md`, `AGENTS.md`, `docs/agents/`, `docs/adr/`, se `triage` está instalada) e só pergunta o que a exploração não resolveu: "Explore, present what you found, confirm with the user, then write." Uma seção por vez, "Lead each section with the recommended answer so the user can accept it in a word", e pula a seção quando a exploração já decidiu. Mostra o rascunho de tudo e deixa o usuário editar antes de gravar.
- **Onde grava:** arquivos `docs/agents/issue-tracker.md`, `triage-labels.md` e `domain.md` no repo, a partir de templates da pasta da skill, mais um bloco `## Agent skills` no `CLAUDE.md` ou no `AGENTS.md` que já existir (se nenhum existir, pergunta qual criar), com uma linha por arquivo e o ponteiro "See `docs/agents/...`".
- **Como as outras skills acham:** pelo bloco no arquivo de instruções, que o harness já carrega em toda sessão. Um ADR separa dependência forte de fraca: as skills que não funcionam sem a configuração (`to-tickets`, `to-spec`, `triage`) dizem "should have been provided to you; run `/setup-matt-pocock-skills` if not"; as que só ficam mais precisas com ela falam dos docs em prosa vaga e seguem sem eles.
- **Rodar de novo:** se o bloco já existe, "update its contents in-place rather than appending a duplicate", sem mexer no resto do arquivo. Re-rodar é só para trocar de tracker ou recomeçar; mudanças do dia a dia são edição à mão nos arquivos. Um modo de verificação separado foi recusado: basta rodar a skill pedindo para conferir sem reescrever (`.out-of-scope/setup-skill-verify-mode.md`).
- **Limites admitidos no doc do autor:** escolhe `CLAUDE.md` ou `AGENTS.md` pelo que existe, não pelo harness que está rodando, e já gravou num arquivo que o Codex não lê; não há modo por usuário em `~/.claude`, cada repo carrega o seu; preferências pessoais (tom, formato de pergunta) não entram no setup, ficam no `CLAUDE.md` como instrução. E uma crítica recorrente: "having a skill to set up the other skill does not feel right to me", que o autor responde com a saída em Markdown legível e editável.
- **Confiança:** relato (repo de grande alcance, mas um autor).

### 6.2 obra/superpowers

- **O que é:** não tem skill de setup nem `userConfig` no `plugin.json`. Preferências vêm das instruções do usuário: "User instructions (CLAUDE.md, AGENTS.md, GEMINI.md, etc, direct requests) take precedence over skills" (`using-superpowers`). A `using-git-worktrees` resolve a pasta numa ordem fixa: preferência declarada nas instruções, depois o que existe no disco (`.worktrees`, `worktrees`), depois um padrão; e só pergunta quando nada disso responde.
- **Confiança:** relato.

### 6.3 anthropics/skills

- **O que é:** nenhuma skill de setup. As que dependem de dados de quem usa trazem os dados no próprio corpo: `brand-guidelines` tem as cores da Anthropic escritas no `SKILL.md`; `internal-comms` guarda os formatos da empresa em `examples/`. Personalizar é fazer fork.
- **Confiança:** relato (exemplos, não doc).

### 6.4 Plugins menores

- **LW (llm-wiki):** combina os dois mundos. No plugin, uma opção `directory` obrigatória; fora dele, um `setup.sh` que grava o caminho no texto da skill copiada. Dentro da pasta escolhida fica um `llm-wiki.yml` com o resto da configuração, e o subcomando `setup` é idempotente: se o arquivo já existe, mostra o que está lá e para sem mudar nada. Se o `wiki_path` do yml diverge da opção do plugin, avisa uma vez e segue com a opção.
- **PW (paper-wiki, claude-ntfy):** gravam em `~/.config/<kit>/` (receita em YAML, `config.toml`, segredos num `.env` com `chmod 600`). Ambos detectam a configuração existente antes de perguntar e, se existe, perguntam se é para reconfigurar; o paper-wiki diz "Do not re-run unprompted". Repos sem estrelas; mostram o padrão, não a adoção.
- **Confiança:** relato.

### 6.5 Padrões que se repetem

| Padrão | Quem faz | Nível |
| - | - | - |
| Só o usuário chama o setup | MP (`disable-model-invocation: true`), LW e PW (subcomando ou skill chamada pelo nome) | convenção |
| Explorar antes de perguntar e pular o que já está respondido | MP, SP (ordem de resolução), PW (`detect-config.sh`) | convenção |
| Pergunta com o valor recomendado primeiro | MP; PW com `AskUserQuestion` | convenção |
| Mostrar o rascunho antes de gravar | MP | relato |
| Rodar de novo atualiza no lugar ou pergunta antes de sobrescrever | MP (in-place), LW (para se já existe), PW (pergunta) | convenção |
| A skill consumidora para com mensagem clara quando falta configuração obrigatória | MP (só nas de dependência forte), LW (placeholder não expandido), PW | convenção |
| Onde gravar | Repo (MP), pasta escolhida pelo usuário (LW), `~/.config/<kit>/` (PW), `settings.json` via `userConfig` (LW, VT, PO) | diverge |

## 7. Riscos

### 7.1 Caminho privado em repo público

- O `userConfig` grava em `~/.claude/settings.json`, fora do repo (SET). O `estilo.md` já é privado por regra ("Keep it out of public repositories", `reel-motion`). O risco está nas bordas: um exemplo na skill com caminho real, um `default` no `plugin.json` com caminho da máquina do autor (o `plugin.json` é público), um eval que copia o `estilo.md`, ou a skill de setup gravando dentro da pasta da skill, que localmente é um link para o repo (4.2).
- O MP grava no repo de propósito, porque a configuração dele é do projeto e não da pessoa; o que é pessoal ele manda para o `CLAUDE.md` do usuário (6.1). O caso deste kit é o oposto: tudo é pessoal.

### 7.2 Máquina nova

- `pluginConfigs` e qualquer arquivo em `~/.config` ou `~/.claude` não migram sozinhos (SET). O `estilo.md`, se morar numa pasta sincronizada pelo autor, migra, mas os caminhos absolutos dentro dele podem não valer na outra máquina (outro usuário, outra letra de drive, macOS em vez de WSL).
- Desinstalar e reinstalar o plugin apaga as opções (CLI).
- Daí a utilidade de o setup ser idempotente e de cada skill conferir que o caminho existe antes de usar: na máquina nova, o setup roda de novo e corrige só o que mudou.

### 7.3 WSL e Windows

- No WSL, o `C:\` aparece como `/mnt/c/` por padrão, mas a raiz é configurável (`[automount] root` no `wsl.conf`), então `/mnt/c` não é garantido (WSL). A Microsoft recomenda não trabalhar entre sistemas de arquivos: arquivos usados pela linha de comando Linux devem ficar no sistema de arquivos do WSL, pela velocidade (WSL).
- O CapCut é um programa Windows e guarda os projetos no perfil do Windows (`<user>/AppData/Local/CapCut/User Data/Projects/com.lveditor.draft/`, como já diz a `reel-finish`). Do WSL, isso é um caminho em `/mnt/<drive>/Users/<usuário>/...`: lento para muitos arquivos e com o nome de usuário do Windows, que não é o do Linux.
- O mesmo caminho tem duas grafias. Quem grava precisa decidir qual guarda; o `wslpath` converte nos dois sentidos (`wslpath -w /home` dá `\\wsl.localhost\<distro>\home`; `wslpath -u 'C:\Users'` dá `/mnt/c/Users`), testado nesta máquina, mas é ferramenta do WSL e não existe no Windows nativo nem no macOS.
- O Claude Code roda no Windows nativo ou no WSL (o sandbox só no WSL 2), e o autor escolhe "based on where your projects are located" (documentação de setup do Claude Code). Um caminho gravado numa sessão do WSL não serve numa sessão nativa, e vice-versa.
- A BP manda usar barras normais em caminhos; no Windows nativo, `C:/Users/...` funciona na maioria das ferramentas, mas não é a grafia que o usuário copia do Explorer. Inferência.
- Um `directory` do `userConfig` guarda o caminho como o usuário digitou; a doc não diz se valida existência nem se normaliza. Inferência da ausência.

## 8. Onde as fontes concordam e divergem

### Concordam

- Configuração de quem usa fica fora dos arquivos da skill: no `settings.json` (MAN), em arquivo do repo (MP), em `~/.config` (PW) ou numa pasta escolhida (LW). Ninguém grava na pasta da skill; a MAN proíbe estado no `${CLAUDE_PLUGIN_ROOT}`, e a skill do MP "If setup edited a `SKILL.md`, something went wrong".
- O setup é chamado pelo usuário e pode rodar de novo sem duplicar (MP, LW, PW).
- Quando falta valor obrigatório, a skill consumidora para e diz como resolver, em vez de adivinhar (MP, LW).

### Divergem

- **Mecanismo do harness ou arquivo próprio:** LW, VT e PO usam o `userConfig`; MP, SP e PW usam arquivos e instruções, que qualquer agente lê. O LW faz os dois, e paga com um script para a versão fora do plugin.
- **Por projeto ou por usuário:** MP é por repo e recusa o modo por usuário; PW é por usuário em `~/.config`; o `userConfig` é por usuário (escopo `user` do `pluginConfigs`).
- **Perguntar tudo ou explorar:** os diálogos do `userConfig` perguntam campo por campo, sem explorar o disco; as skills de setup exploram primeiro e recomendam.

## 9. O que isso sugere para a skill de setup

Não são decisões, são consequências das fontes acima para o desenho.

1. **O `userConfig` não muda a decisão.** Ele só existe para quem instala o plugin do Claude Code; para o `npx skills`, para outros agentes e para skills em `draft` (fora do plugin), o `${user_config.*}` chega como texto (2.4, 4.2). Um arquivo em Markdown que qualquer agente lê é o único caminho que vale nos dois canais de distribuição. A seção "Caminhos" no `estilo.md` atende a isso, e o `estilo.md` já é lido pelas skills de conteúdo.
2. **Falta resolver como as skills acham o próprio `estilo.md`.** Hoje ele mora na pasta de reels, e as skills o acham porque a pasta do reel está dentro dela (`reel-motion`, Files). Se o roteiro ou o vídeo bruto estiverem em outra pasta, nada leva até ele. Esse ponteiro único é onde o `userConfig` pode entrar como complemento: uma só opção `directory` no plugin (a pasta do `estilo.md`), com o padrão do LW para quando o placeholder não for expandido (perguntar, ou procurar na pasta atual e nas acima). Outras saídas: uma linha no `~/.claude/CLAUDE.md` ou no `AGENTS.md` global, ou `~/.config/<kit>/`, ambas fora do repo.
3. **Explorar antes de perguntar.** Procurar `estilo.md`, pastas de reels e a pasta de projetos do CapCut nos lugares conhecidos e oferecer o que achou como opção recomendada, uma pergunta por caminho, no formato de múltipla escolha que as skills de conteúdo já usam (MP, SP).
4. **Mostrar o bloco "Caminhos" antes de gravar e atualizar no lugar** quando a seção já existir, sem tocar no resto do `estilo.md`, que guarda os padrões de gosto do autor (MP).
5. **Conferir que cada caminho existe** ao gravar, e de novo em cada skill antes de usar, com uma mensagem que mande rodar o setup (7.2). Separar dependência forte de fraca, como o ADR do MP: a pasta do CapCut é forte para `reel-finish`; o design system é fraco para `reel-motion`, que já segue sem ele.
6. **Guardar caminhos na grafia de quem vai abrir os arquivos.** Os scripts rodam no WSL, então a grafia `/mnt/...` serve para eles; o autor no Explorer precisa da grafia Windows. Gravar uma e converter com `wslpath` quando precisar da outra, só quando o `wslpath` existir (7.3).
7. **Nenhum caminho real em arquivo do repo:** nem `default` no `plugin.json`, nem exemplo no `SKILL.md`, nem fixture de eval (7.1). Exemplos com `<usuário>` e `<pasta de reels>`.
8. **`disable-model-invocation: true`** deixa a skill de setup só com o usuário e fora do contexto do modelo (escrita-de-skills.md, 5.2). Como é campo só do Claude Code, outros agentes a verão como skill comum; a description deve dizer que roda uma vez, por pedido explícito.

## 10. Perguntas abertas

- Onde fica o ponteiro para o `estilo.md`: convenção de pasta (o que existe hoje), uma opção `userConfig` no plugin, uma linha no arquivo de instruções global do agente, ou `~/.config/<kit>/`? Cada uma tem um alcance diferente (6.5, 9.2).
- O `estilo.md` hoje é por pasta de reels. Com a seção "Caminhos", ele passa a ser um arquivo por usuário. Um autor com duas pastas de reels (dois perfis, dois estilos) teria dois arquivos com caminhos repetidos?
- Que texto o Claude Code põe no corpo da skill para uma opção `userConfig` vazia e sem `default`? A doc não diz; precisa de teste com `claude --plugin-dir` antes de depender disso.
- Uma atualização do plugin que acrescenta opção nova abre o diálogo? A doc só fala de instalação, habilitação e `configure`.
- A skill de setup entra no plugin (precisa ser `beta`) ou fica só no `npx skills` enquanto for `draft`? Se ficar fora, quem usa o plugin não a tem.
- Caminhos relativos à pasta do `estilo.md` (como o `legacyDir` do PO é relativo ao workspace) evitariam a troca de máquina? Só se as pastas do CapCut e de vídeos ficarem abaixo dela, o que o CapCut não permite.

## 11. Fontes

Oficiais (consultadas em 2026-10-19):

- Claude Code, Plugin manifest reference: https://code.claude.com/docs/en/plugins/manifest-reference (também em https://code.claude.com/docs/en/plugins-reference)
- Claude Code, Plugin components: https://code.claude.com/docs/en/plugins/components
- Claude Code, Plugin CLI reference: https://code.claude.com/docs/en/plugins/cli-reference
- Claude Code, Plugin troubleshooting: https://code.claude.com/docs/en/plugins/troubleshooting
- Claude Code, Settings reference (`pluginConfigs`): https://code.claude.com/docs/en/settings-reference
- Claude Code, Extend Claude with skills: https://code.claude.com/docs/en/skills
- Claude Code, How Claude remembers your project: https://code.claude.com/docs/en/memory
- Claude Code, Set up Claude Code (Windows e WSL): https://code.claude.com/docs/en/setup
- Agent Skills specification: https://agentskills.io/specification
- Skill authoring best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- vercel-labs/skills: https://github.com/vercel-labs/skills (README e `docs/commands.md`, `docs/creating-skills.md`, `docs/troubleshooting.md`, `docs/agents.md`)
- Microsoft, Working across Windows and Linux file systems: https://learn.microsoft.com/en-us/windows/wsl/filesystems
- Microsoft, Advanced settings configuration in WSL (`wsl.conf`): https://learn.microsoft.com/en-us/windows/wsl/wsl-config

Comunidade (anedótico):

- mattpocock/skills, `setup-matt-pocock-skills`: https://github.com/mattpocock/skills/tree/main/skills/engineering/setup-matt-pocock-skills
- mattpocock/skills, doc da skill: https://github.com/mattpocock/skills/blob/main/docs/engineering/setup-matt-pocock-skills.md
- mattpocock/skills, ADR de dependência forte e fraca: https://github.com/mattpocock/skills/blob/main/.agents/adr/0001-explicit-setup-pointer-only-for-hard-dependencies.md
- mattpocock/skills, modo de verificação fora de escopo: https://github.com/mattpocock/skills/blob/main/.out-of-scope/setup-skill-verify-mode.md
- obra/superpowers: https://github.com/obra/superpowers (skills `using-git-worktrees`, `using-superpowers`)
- anthropics/skills: https://github.com/anthropics/skills (skills `brand-guidelines`, `internal-comms`)
- anthropics/claude-plugins-official, `code-modernization`: https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-modernization
- MehmetGoekce/llm-wiki: https://github.com/MehmetGoekce/llm-wiki
- viticci/shortcuts-playground-plugin: https://github.com/viticci/shortcuts-playground-plugin
- kaneyxx/paper-wiki, `skills/setup`: https://github.com/kaneyxx/paper-wiki/tree/main/skills/setup
- jason-hchsieh/claude-ntfy, `skills/setup`: https://github.com/jason-hchsieh/claude-ntfy/tree/main/skills/setup

Notas relacionadas neste repositório:

- [versionamento-e-distribuicao.md](versionamento-e-distribuicao.md)
- [orquestracao-de-skills.md](orquestracao-de-skills.md)
- [escrita-de-skills.md](escrita-de-skills.md)
- [docs/adr/0002-skills-reference-each-other-by-name.md](../adr/0002-skills-reference-each-other-by-name.md)
- [docs/adr/0005-versioned-claude-code-plugin.md](../adr/0005-versioned-claude-code-plugin.md)
