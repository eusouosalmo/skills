#!/usr/bin/env bash
set -euo pipefail

# Symlinks every skill in this repo into the local skill directories:
#   - ~/.agents/skills: npx skills CLI and Agent Skills compatible agents
#   - ~/.claude/skills: Claude Code (symlinks supported, see code.claude.com/docs/en/skills)
# Each entry points back here, so editing a skill in the repo takes effect at once.
# Re-run after creating, renaming or removing a skill.
#
# Skips skills with `status: deprecated` in frontmatter.
# Never deletes a real directory: if something with the same name exists and
# is not a symlink, it warns and moves on.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DESTS=("$HOME/.agents/skills" "$HOME/.claude/skills")

names=()
srcs=()
while IFS= read -r -d '' skill_md; do
  src="$(dirname "$skill_md")"
  name="$(basename "$src")"

  # Frontmatter runs from the first `---` to the second.
  frontmatter="$(awk '/^---$/{n++; next} n==1' "$skill_md")"

  declared="$(printf '%s\n' "$frontmatter" | sed -n 's/^name:[[:space:]]*//p' | head -n1)"
  if [ "$declared" != "$name" ]; then
    echo "error: $skill_md declares name '$declared' but its folder is '$name'." >&2
    exit 1
  fi

  if printf '%s\n' "$frontmatter" | grep -Eq '^[[:space:]]+status:[[:space:]]*deprecated'; then
    echo "skipping $name (deprecated)"
    continue
  fi

  names+=("$name")
  srcs+=("$src")
done < <(find "$REPO/skills" -name SKILL.md -print0 | sort -z)

# A name repeated across categories would collide in the flat install dir.
dup="$(printf '%s\n' "${names[@]}" | sort | uniq -d)"
if [ -n "$dup" ]; then
  echo "error: duplicate skill name: $dup" >&2
  exit 1
fi

for DEST in "${DESTS[@]}"; do
  # If the destination is a symlink into this repo, links would land in the repo itself.
  if [ -L "$DEST" ]; then
    case "$(readlink -f "$DEST")" in
      "$REPO" | "$REPO"/*)
        echo "error: $DEST points into this repo. Remove it and re-run." >&2
        exit 1
        ;;
    esac
  fi

  mkdir -p "$DEST"

  for i in "${!names[@]}"; do
    name="${names[$i]}"
    src="${srcs[$i]}"
    target="$DEST/$name"

    if [ -e "$target" ] && [ ! -L "$target" ]; then
      echo "warning: $target exists and is not a symlink; left untouched." >&2
      continue
    fi

    ln -sfn "$src" "$target"
    echo "linked $name -> $src ($DEST)"
  done
done
