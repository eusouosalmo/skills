#!/usr/bin/env bash
# Preflight for an unattended (AFK) Claude Code run. Call it before every run of the
# loop and abort the loop when it fails:
#
#   .claude/hooks/preflight.sh .claude/git-guardrails-afk.json || exit 1
#
# It measures the result, not the config: it runs each hook command exactly as the AFK
# settings file registers it, with a command that must be blocked and one that must
# pass. That catches a wrong path, a script without +x, a missing jq or config, and a
# hook that blocks everything. It also aborts when disableAllHooks is on in any
# settings file Claude Code could read.
#
# Exit 0: safe to start. Exit 1: do not start; the reason is on stderr.
# Needs: bash, jq, git.

set -u

fail() {
  printf 'preflight: ABORT. %s\n' "$1" >&2
  exit 1
}

SETTINGS=${1-}
[[ -n $SETTINGS ]] || fail "usage: preflight.sh <afk-settings.json>"
command -v jq >/dev/null 2>&1 || fail "jq is not installed; the git-guardrails hook needs it."
command -v git >/dev/null 2>&1 || fail "git is not installed."
ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || fail "not inside a git repository."
[[ $SETTINGS == /* ]] || SETTINGS="$PWD/$SETTINGS"
[[ -r $SETTINGS ]] || fail "AFK settings file $SETTINGS not found."
jq -e . "$SETTINGS" >/dev/null 2>&1 || fail "AFK settings file $SETTINGS is not valid JSON."

# Bare mode skips every hook, those passed with --settings included (Claude Code 2.1.288).
[[ -z ${CLAUDE_CODE_SIMPLE-} ]] || fail "CLAUDE_CODE_SIMPLE is set: bare mode skips every hook. Unset it and do not pass --bare."

# disableAllHooks in any file that could apply turns the guardrail off silently.
for f in "$SETTINGS" "$ROOT/.claude/settings.json" "$ROOT/.claude/settings.local.json" "$HOME/.claude/settings.json"; do
  [[ -r $f ]] || continue
  if [[ $(jq -r '.disableAllHooks // false' "$f" 2>/dev/null) == true ]]; then
    fail "disableAllHooks is true in $f, so no hook would run. Remove it by hand before starting the loop."
  fi
done

mapfile -t CMDS < <(jq -r '.hooks.PreToolUse[]? | select((.matcher // "") | test("Bash")) | .hooks[]? | select(.type == "command") | .command' "$SETTINGS")
GUARD=()
for c in "${CMDS[@]}"; do
  [[ $c == *git-guardrails* ]] && GUARD+=("$c")
done
((${#GUARD[@]})) || fail "$SETTINGS registers no git-guardrails PreToolUse hook on Bash."

# Harmless if it ever ran: the directory does not exist, so git exits with an error.
CANARY="git -C /nonexistent-git-guardrails-canary reset --hard"
payload() { jq -cn --arg c "$1" --arg d "$ROOT" '{tool_name: "Bash", tool_input: {command: $c}, cwd: $d, hook_event_name: "PreToolUse"}'; }

TIMEOUT=()
command -v timeout >/dev/null 2>&1 && TIMEOUT=(timeout 30) # a hook that hangs is a hook that fails open

for c in "${GUARD[@]}"; do
  [[ $c == *"--profile afk"* ]] || fail "hook '$c' does not use --profile afk."
  err=$(cd "$ROOT" && CLAUDE_PROJECT_DIR=$ROOT "${TIMEOUT[@]}" bash -c "$c" <<<"$(payload "$CANARY")" 2>&1 >/dev/null)
  rc=$?
  ((rc == 2)) && [[ $err == *git-guardrails:* ]] ||
    fail "hook '$c' did not block the canary '$CANARY' (exit $rc: ${err:-no output}). The guardrail is off."
  [[ $err == *"missing or unreadable"* ]] && fail "hook '$c' has no config file: $err"
  out=$(cd "$ROOT" && CLAUDE_PROJECT_DIR=$ROOT "${TIMEOUT[@]}" bash -c "$c" <<<"$(payload "git status")" 2>&1)
  rc=$?
  ((rc == 0)) || fail "hook '$c' blocks even 'git status' (exit $rc: $out). Check its config file."
done

echo "preflight: ok, git-guardrails AFK hook is active."
