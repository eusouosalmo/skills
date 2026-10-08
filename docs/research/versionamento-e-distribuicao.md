# Versionamento e distribuição do repo de skills

Resumo: o repo hoje se instala só pelo CLI `npx skills` (vercel-labs/skills), que já instala, atualiza e remove, mas não tem versão: o `update` puxa o que estiver no `main`, e a maturidade vive só em `metadata.status`. O repo de referência (mattpocock/skills) tem, além disso, um plugin do Claude Code com versão no manifesto, uma lista explícita das skills que entram no plugin, e releases com Changesets (CHANGELOG, tag e PR de versão automáticos). Para este repo, que já usa Conventional Commits e é só Markdown e scripts, o release-please faz o mesmo papel do Changesets sem trazer Node para o repo. Pesquisa de 2026-10-08. Não decide nada; a seção 5 lista as decisões.

## 1. Fontes

| Sigla | Fonte | Tipo |
| - | - | - |
| VSK | [vercel-labs/skills, README](https://github.com/vercel-labs/skills) | primária (CLI) |
| CCM | [Claude Code, Create a marketplace](https://code.claude.com/docs/en/plugin-marketplaces) | primária |
| CCP | [Claude Code, Plugin manifest reference](https://code.claude.com/docs/en/plugins-reference) | primária |
| CCL | [Claude Code, Plugin loading reference](https://code.claude.com/docs/en/plugins/loading) (seção "Versions and updates") | primária |
| MPS | mattpocock/skills: `.claude-plugin/marketplace.json`, `.claude-plugin/plugin.json`, `.changeset/config.json`, `package.json`, `.github/workflows/release.yml`, `CHANGELOG.md` (lidos no `main` em 2026-10-08) | primária (exemplo, não autoridade) |
| RPL | [release-please, README](https://github.com/googleapis/release-please) e [docs/customizing.md](https://github.com/googleapis/release-please/blob/main/docs/customizing.md) | primária |

## 2. O que o repo já tem

- **Instalar, atualizar, remover:** `npx skills add eusouosalmo/skills`, `npx skills update`, `npx skills remove <nome>` (alias `rm`), `npx skills list`. Funciona para qualquer repo, sem mudar nada aqui (VSK).
- **Sem versão:** o CLI não lê versão no SKILL.md; os campos documentados são `name`, `description` e `metadata.internal` (VSK). Sem tags, sem CHANGELOG. `metadata.status` (draft, beta, stable, deprecated) diz maturidade, não versão (`docs/adr/0001`).
- **Rascunho escondido:** `metadata.internal: true` tira a skill do instalador (VSK).
- **Uso local:** `scripts/link-skills.sh` cria links em `~/.agents/skills` e `~/.claude/skills`; remover é apagar o link.

## 3. Plugin do Claude Code

- **Marketplace:** um `.claude-plugin/marketplace.json` com `name`, `owner` e `plugins` (cada um com `name` e `source`). O próprio repo pode ser o plugin, com `"source": "./"` (CCM, MPS). O usuário roda `claude plugin marketplace add eusouosalmo/skills` e `claude plugin install <plugin>@<marketplace>` (CCM).
- **Manifesto:** `.claude-plugin/plugin.json`; só `name` é obrigatório. `version` é texto livre, não conferido contra semver (CCP).
- **Skills por categoria cabem:** a chave `skills` aceita "diretórios de pastas `<nome>/SKILL.md`" ou uma pasta com `SKILL.md`, e soma à varredura padrão de `skills/` (CCP). O Matt lista skill por skill (`./skills/engineering/tdd`, ...), o que deixa rascunhos de fora do plugin (MPS). A pasta `skills/content/x` não precisa mudar de lugar.
- **Rascunho no plugin:** o plugin carrega o que estiver nos caminhos listados; o `metadata.internal` do `npx skills` não vale para ele. Para esconder rascunho, a lista do `plugin.json` só leva `beta` e `stable` (inferência da CCP e do exemplo MPS).
- **Nome com prefixo:** cada skill do plugin vira `<plugin>:<skill>` (CCP). Quem instalar pelo plugin e pelo `npx skills` ao mesmo tempo terá a skill duas vezes.
- **Nome reservado:** o nome do plugin não pode começar com `claude-` nem ser `claude`, `anthropic` etc. (CCP).
- **Versão e atualização:** com `version` no manifesto, o usuário fica naquela versão até ela mudar; sem `version`, a versão é o SHA do commit e todo push vira atualização (CCL). Atualização automática fica **desligada por padrão** para marketplaces de terceiros; o usuário liga em `/plugin` ou roda `claude plugin update` (CCL).
- **Remover:** `claude plugin uninstall`, ou `claude plugin marketplace remove <nome>`, que remove o marketplace e desinstala os plugins dele (CCM, CCL).
- **Conferir:** `claude plugin validate .` checa o JSON, os campos e os caminhos; `--strict` falha em aviso, para CI (CCP).

## 4. Release: Changesets ou release-please

| | Changesets (o que o Matt usa) | release-please |
| - | - | - |
| De onde vem a versão | Um arquivo `.changeset/*.md` por mudança, escrito à mão | Das mensagens Conventional Commits: `fix` patch, `feat` minor, `!` ou `BREAKING-CHANGE` major (RPL) |
| Fluxo | Action abre o PR "chore: version skills"; ao aceitar, `changeset version`, script que copia a versão para o `plugin.json`, e `changeset tag` (MPS) | Action mantém um PR de release; ao aceitar, CHANGELOG, tag e GitHub Release (RPL) |
| Versão no `plugin.json` | Script próprio (`sync-plugin-version.mjs`) (MPS) | `extra-files` com `{"type": "json", "path": ".claude-plugin/plugin.json", "jsonpath": "$.version"}` (RPL) |
| Custo no repo | `package.json`, `package-lock.json`, `node_modules` em CI, `@changesets/cli` (MPS) | Só `release-please-config.json`, `.release-please-manifest.json` e o workflow (RPL) |
| Controle | Fino: cada nota escolhida | O que o commit disser; `chore` e `docs` não entram (RPL) |

Este repo já escreve Conventional Commits (CLAUDE.md), então o release-please lê o que já existe. Inferência, não testada aqui.

## 5. Decisões em aberto

1. Plugin do Claude Code sim ou não, e com que nome (sem prefixo reservado).
2. Uma lista explícita de skills no `plugin.json`, e como ela acompanha `metadata.status` (à mão ou gerada por script).
3. `version` fixa no manifesto (releases) ou SHA do commit (todo push é atualização).
4. Changesets ou release-please; versão inicial (0.x enquanto houver skills em draft?).
5. Como avisar quem instala pelos dois caminhos (plugin e `npx skills`).
6. README e README.pt-BR: seção de instalar, atualizar e remover pelos dois caminhos.
