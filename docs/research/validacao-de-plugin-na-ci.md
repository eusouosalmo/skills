# Validação do plugin na CI do GitHub

Resumo: sim. `claude plugin validate` roda sem login e sem nenhuma credencial; testei com `HOME` vazio e `env -i`, e ele não pediu nada. O comando para a CI é `npx -y @anthropic-ai/claude-code@2.1.293 plugin validate . --strict`. Ele cobre JSON válido, campos obrigatórios e caminhos das skills, mas tem duas lacunas para este repo: não confere se o nome do plugin é igual nos dois arquivos (a doc diz que eles podem divergir) e não lê os `SKILL.md` que ficam em `skills/<categoria>/<skill>/`. Um passo curto com `jq` cobre as duas. Pesquisa de 2026-10-08 para o ticket [#14](https://github.com/eusouosalmo/skills/issues/14) (parte do #12).

## 1. Fontes

| Sigla | Fonte | Tipo |
| - | - | - |
| CLI | [Plugins CLI reference](https://code.claude.com/docs/en/plugins/cli-reference), seção `plugin validate` | primária |
| MAN | [Plugin manifest reference](https://code.claude.com/docs/en/plugins/manifest-reference) | primária |
| MKT | [Marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference) | primária |
| SET | [Set up Claude Code](https://code.claude.com/docs/en/setup), seção "Install with npm" | primária |
| NPM | `npm view @anthropic-ai/claude-code` em 2026-10-08: `latest` 2.1.293, `stable` 2.1.285, `engines.node >=22.0.0` | primária |
| RUN | [actions/runner-images](https://github.com/actions/runner-images): `ubuntu-latest` é Ubuntu 24.04, com Node.js 22.23.3 e jq 1.7 | primária |
| TESTE | Teste local, descrito na seção 3 | teste |

## 2. Confirmado pela doc

- **Pacote e Node:** o pacote npm é `@anthropic-ai/claude-code`, pede Node.js 22 ou mais novo e instala o mesmo binário nativo do instalador, por uma dependência opcional por plataforma (`linux-x64` incluída). Com Node mais antigo o npm só avisa `EBADENGINE` e o `claude` roda mesmo assim (SET).
- **Comando:** `claude plugin validate <path> [--strict] [--json]`. `--strict` transforma aviso em erro; `--json` imprime o relatório como um objeto JSON, a partir da v2.1.259 (CLI).
- **Códigos de saída:** `0` para `Validation passed` (com ou sem avisos; com `--strict`, sem avisos), `1` para `Validation failed`, `2` para `Unexpected error during validation` (falha do próprio validador; nada vai para o stdout) (CLI).
- **O que ele escolhe validar num diretório:** `.claude-plugin/marketplace.json` se existir, senão `.claude-plugin/plugin.json`, senão os componentes. Com os dois manifestos no mesmo diretório, valida o marketplace, o manifesto do plugin e os componentes, a partir da v2.1.289 (CLI).
- **Campos obrigatórios:** no `plugin.json`, só `name`; aviso para `name` fora de kebab-case e para `version`, `description` ou `author` ausentes (MAN). Caminho de componente precisa começar com `./`, ficar dentro do plugin e existir; senão, erro `Path not found` (MAN).
- **Nome diferente nos dois arquivos é permitido:** o `name` da entrada do marketplace é o que o usuário digita antes do `@`, "mesmo quando o `plugin.json` do plugin define um `name` diferente" (MKT). Por isso o validador não reclama.
- **Links simbólicos:** o validador não segue symlinks dentro do diretório; avisa ou dá erro conforme onde está o link (CLI). O repo não usa symlinks dentro de `skills/` (o `link-skills.sh` cria links fora do repo), então não afeta.
- **A doc não diz nada sobre login para `plugin validate`.** Que ele roda sem credencial vem do teste, não da doc.

## 3. Teste

Ambiente: WSL2, Linux x64, Node 24.18.0, Claude Code 2.1.293 baixado na hora pelo `npx` (o `HOME` vazio não tinha cache). Plugin mínimo com o layout que este repo teria: `.claude-plugin/marketplace.json` (`name`, `owner`, `description`, um plugin com `"source": "./"`), `.claude-plugin/plugin.json` (`name`, `description`, `version`, `author`, `"skills": ["./skills/content/writing-x"]`) e `skills/content/writing-x/SKILL.md`.

Comando, sem nenhuma variável além de `PATH` e `HOME`:

```bash
env -i PATH=/usr/bin:/bin:<dir do node> HOME=<dir vazio> \
  npx -y @anthropic-ai/claude-code@2.1.293 plugin validate ./repo --strict </dev/null
```

Não houve pedido de login, nem prompt, nem acesso a credencial; a execução levou uns 7 segundos, quase tudo download. O validador só criou `~/.claude.json` e `~/.claude/backups/` no `HOME` vazio.

| Caso | Saída literal (resumida) | Saída |
| - | - | - |
| Marketplace sem `description` | `description: No marketplace description provided...` e `Validation failed (--strict treats warnings as errors)` | 1 |
| Tudo certo | `Validation passed` | 0 |
| `name` diferente no `plugin.json` | `Validation passed` | 0 |
| Caminho de skill inexistente | `skills[0]: Path not found: ./skills/content/writing-y` (no marketplace e no plugin) | 1 |
| `plugin.json` com JSON quebrado | `json: Invalid JSON syntax: JSON Parse error: Property name must be a string literal` | 1 |
| `marketplace.json` com JSON quebrado | `json: Invalid JSON syntax: JSON Parse error: Unexpected EOF` | 1 |
| Marketplace sem `owner` | `owner: Invalid input: expected object, received undefined` | 1 |
| `plugin.json` sem `name` | `name: Invalid input: expected string, received undefined` | 1 |
| Caminho que não existe | `file: File not found: ...` e `Validation failed` | 1 |
| `SKILL.md` sem frontmatter, em `skills/content/writing-x/` | `Validation passed`; no `--json`, `"contents": []` | 0 |
| O mesmo `SKILL.md`, em `skills/writing-x/` (layout plano) | `frontmatter: No frontmatter block found...` e falha com `--strict` | 1 |
| `name` do frontmatter diferente da pasta, layout plano | `Validation passed` | 0 |

O teste foi numa máquina local, não num runner. Que o resultado se repete no `ubuntu-latest` é inferência: é o mesmo pacote `linux-x64`, e o runner tem Node 22 (RUN), que atende o `engines` (NPM).

## 4. O que o validador cobre e o que falta

| Checagem que importa | `plugin validate --strict` |
| - | - |
| JSON válido nos dois arquivos | Cobre (teste) |
| Campos obrigatórios (`name`, `owner`, `plugins`) | Cobre (teste, MAN, MKT) |
| Caminhos das skills existindo | Cobre (teste, MAN) |
| Nome do plugin igual nos dois arquivos | **Não cobre**; a doc permite divergir (MKT, teste) |
| Frontmatter dos `SKILL.md` em `skills/<categoria>/<skill>/` | **Não cobre**; só o layout plano `skills/<skill>/` é lido (teste) |
| `name` do frontmatter igual à pasta | **Não cobre**, nem no layout plano (teste) |

Por que o frontmatter fica de fora é inferência: a varredura de componentes parece descer só um nível em `skills/`, e uma pasta listada na chave `skills` do `plugin.json` só tem o caminho conferido. Passar `skills/content` direto também não resolve, porque a doc só lê componentes de um diretório chamado `skills`, `agents`, `commands` ou `.claude` (CLI).

## 5. Comando recomendado para a CI

Versão fixa, pelo menos 2.1.289 (validação dos dois manifestos juntos, CLI). Fixar evita que uma versão nova com aviso novo quebre o `--strict` sem mudança no repo; a doc dá um exemplo disso, campos que passaram a ser aceitos sem aviso só na v2.1.281 (MAN).

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: 22
- run: npx -y @anthropic-ai/claude-code@2.1.293 plugin validate . --strict
```

O `setup-node` é opcional, já que o `ubuntu-latest` já traz Node 22 (RUN). Deixá-lo explícito protege contra uma troca de imagem. Isto é inferência; não rodei num runner.

Complemento para as lacunas, testado localmente contra os casos acima (pega nome divergente, frontmatter ausente e `name` diferente da pasta). Usa só `jq` e `sed`, que o runner já tem (RUN):

```bash
#!/usr/bin/env bash
set -euo pipefail
m=$(jq -r '.plugins[0].name' .claude-plugin/marketplace.json)
p=$(jq -r '.name' .claude-plugin/plugin.json)
[ "$m" = "$p" ] || { echo "plugin name differs: marketplace=$m plugin.json=$p"; exit 1; }
fail=0
for d in $(jq -r '.skills[]' .claude-plugin/plugin.json); do
  f="$d/SKILL.md"
  [ -f "$f" ] || { echo "missing $f"; fail=1; continue; }
  n=$(sed -n '2,/^---$/{s/^name: *//p}' "$f" | head -1)
  [ "$n" = "$(basename "$d")" ] || { echo "$f: name '$n' != folder"; fail=1; }
done
exit $fail
```

Ele supõe um único plugin no marketplace e a chave `skills` como lista de pastas, o formato que a pesquisa de versionamento e distribuição do mapa #12 aponta. Se o layout mudar, o script muda junto.

## 6. Perguntas em aberto

1. Rodar uma vez num runner de verdade para confirmar a inferência da seção 3 (tempo, saída e código).
2. Quando subir a versão fixa do Claude Code: à mão, ou com Dependabot ou Renovate num `package.json` mínimo, o que traria Node para o repo.
3. Se o complemento entra num script em `scripts/` (que também serviria no pre-commit) ou direto no workflow.
