#!/usr/bin/env bash
set -euo pipefail

# Keeps the Claude Code plugin in step with each skill's maturity:
# .claude-plugin/plugin.json lists every skill whose `metadata.status` is
# beta or stable, and nothing else. The plugin loads whatever is listed, and
# `metadata.internal` (which hides drafts from `npx skills`) does not apply to it.
#
#   scripts/sync-plugin-skills.sh          rewrite the `skills` list in plugin.json
#   scripts/sync-plugin-skills.sh --check  fail if plugin.json is out of date (CI)
#
# Both modes also fail when a SKILL.md `name` differs from its folder, or when
# the plugin name differs between marketplace.json and plugin.json, two things
# `claude plugin validate` does not check (docs/research/validacao-de-plugin-na-ci.md).
# Needs jq.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
PLUGIN="$REPO/.claude-plugin/plugin.json"
MARKETPLACE="$REPO/.claude-plugin/marketplace.json"

check=false
case "${1:-}" in
  --check) check=true ;;
  "") ;;
  *) echo "usage: $0 [--check]" >&2; exit 2 ;;
esac

fail=0

m="$(jq -r '.plugins[0].name' "$MARKETPLACE")"
p="$(jq -r '.name' "$PLUGIN")"
if [ "$m" != "$p" ]; then
  echo "error: plugin name differs: marketplace.json '$m', plugin.json '$p'." >&2
  fail=1
fi

paths=()
while IFS= read -r skill_md; do
  dir="$(dirname "$skill_md")"
  name="$(basename "$dir")"

  # Frontmatter runs from the first `---` to the second.
  frontmatter="$(awk '/^---$/{n++; next} n==1' "$skill_md")"

  declared="$(printf '%s\n' "$frontmatter" | sed -n 's/^name:[[:space:]]*//p' | head -n1)"
  if [ "$declared" != "$name" ]; then
    echo "error: ${skill_md#"$REPO"/} declares name '$declared' but its folder is '$name'." >&2
    fail=1
    continue
  fi

  status="$(printf '%s\n' "$frontmatter" | sed -n 's/^[[:space:]]\{1,\}status:[[:space:]]*//p' | head -n1)"
  case "$status" in
    beta | stable) paths+=("./${dir#"$REPO"/}") ;;
    draft | deprecated) ;;
    *) echo "error: ${skill_md#"$REPO"/} has no valid metadata.status ('$status')." >&2; fail=1 ;;
  esac
done < <(find "$REPO/skills" -name SKILL.md | sort)

[ "$fail" -eq 0 ] || exit 1

want="$(printf '%s\n' "${paths[@]}" | jq -R . | jq -sc .)"
have="$(jq -c '.skills' "$PLUGIN")"

if [ "$want" = "$have" ]; then
  echo "plugin.json lists ${#paths[@]} skills (beta and stable); up to date."
  exit 0
fi

if $check; then
  echo "error: plugin.json skills are out of date with metadata.status." >&2
  echo "  plugin.json: $have" >&2
  echo "  expected:    $want" >&2
  echo "Run scripts/sync-plugin-skills.sh and commit the result." >&2
  exit 1
fi

tmp="$(mktemp)"
jq --argjson skills "$want" '.skills = $skills' "$PLUGIN" > "$tmp"
mv "$tmp" "$PLUGIN"
echo "plugin.json now lists: $want"
