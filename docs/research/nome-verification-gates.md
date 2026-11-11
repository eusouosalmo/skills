# O nome verification-gates está livre?

Pesquisa do ticket #108 (mapa #103), feita em 2026-11-10.

## Resposta

Não está livre. Pelo menos cinco skills públicas já se chamam exatamente `verification-gates`, e há variantes com prefixo. Alternativas propostas, na regra de nomes do repo (tema primeiro, substantivo, sem `factory-`, ver `docs/adr/0006`): `done-gates` e `agent-checks`.

## Achados

### skills.sh

A busca da API do diretório (`https://skills.sh/api/search?q=verification-gates`) devolve skills com `name: verification-gates` exato em:

- `dorav/reality-check` (2 instalações)
- `kshitijpalsinghtomar/depth-skills`
- `josix/agent-flow`
- `icampana/e-van-opencode`
- `smithery.ai` (espelho)

Variantes com prefixo: `saltbo/bstack/bep-verification-gates` e `agentpatterns-ai/skills/audit-verification-gates`.

Todas têm poucas instalações, mas a colisão importa porque `npx skills` instala tudo plano em `~/.agents/skills/<name>` (AGENTS.md, seção Layout): quem tiver uma dessas instalada perde uma das duas.

### GitHub

`gh search code "name: verification-gates"` confirma o repo `josix/agent-flow`, cujo `scripts/validate-plugin.sh` lista `verification-gates` entre as skills esperadas. Há também `openshift/rosa` com `.claude/skills/rosa-verification-gates/` e vários documentos (não skills) com o termo. A busca de repos não achou repo com esse nome.

### Repos de skills mais usados

`gh search code verification` em `anthropics/skills`, `mattpocock/skills`, `obra/superpowers` e `vercel-labs/agent-skills` não acha skill com esse nome. O mais próximo é `obra/superpowers/skills/verification-before-completion`: nome diferente, mas tema vizinho (exigir evidência antes de declarar pronto). Vale lembrar dele ao escrever a description, para não disputarem o gatilho.

### Instalação local

`~/.agents/skills` e `~/.claude/skills` não têm nada com `verif` ou `gate` no nome.

## Alternativas

| Nome | skills.sh | GitHub (`name:`) | Observação |
|---|---|---|---|
| `check-gates` | ocupado | | descartado |
| `done-gates` | livre | livre | diz o que o gate decide: quando o trabalho do agente conta como pronto |
| `agent-checks` | sem nome exato | sem skill com esse nome | mais genérico; o tema `agent` agrupa com outras skills de harness |

Recomendação: `done-gates`. Curto, digitável e sem colisão.

## Fontes

- API de busca do skills.sh: `https://skills.sh/api/search?q=<nome>`
- GitHub code search via `gh search code`
- Regra de nomes: `AGENTS.md` (seção Names) e `docs/adr/0006`
