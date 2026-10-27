#!/usr/bin/env bash
# Runs the git-guardrails hook against a table of commands, in both profiles, inside a
# throwaway git repo with a local remote. Each row names the category the command
# belongs to; the expected decision comes from git-guardrails.conf, so the table stays
# right after the user loosens or tightens a rule.
#
# Usage: test-guardrails.sh [path/to/git-guardrails.sh]
#   Default hook path: git-guardrails.sh next to this script.
# Exit 0 when every row passes, 1 otherwise. Needs bash, jq, git, mktemp.

set -u

HERE=${BASH_SOURCE[0]%/*}
[[ $HERE == "${BASH_SOURCE[0]}" ]] && HERE=.
HOOK=${1:-$HERE/git-guardrails.sh}
HOOK=$(cd "${HOOK%/*}" && pwd)/${HOOK##*/}
CONF=${HOOK%/*}/git-guardrails.conf

for dep in jq git mktemp; do
  command -v "$dep" >/dev/null 2>&1 || { echo "test-guardrails: $dep is required" >&2; exit 1; }
done
[[ -x $HOOK ]] || { echo "test-guardrails: $HOOK is missing or not executable" >&2; exit 1; }
[[ -r $CONF ]] || { echo "test-guardrails: $CONF is missing" >&2; exit 1; }

declare -A CONF_VAL=()
while IFS= read -r line || [[ -n $line ]]; do
  line=${line%%#*}
  line=${line//[[:space:]]/}
  [[ $line == *=* ]] && CONF_VAL[${line%%=*}]=${line#*=}
done <"$CONF"

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

# Throwaway repos: "feat" is on branch feat with an unpushed commit, "pushed" is on
# branch feat with HEAD already on the remote, "main" is on main. origin/HEAD is main.
setup_repos() {
  local g=(git -c user.name=test -c user.email=test@example.com -c init.defaultBranch=main -c advice.detachedHead=false)
  "${g[@]}" init -q --bare "$TMP/remote.git"
  "${g[@]}" init -q "$TMP/main"
  (
    cd "$TMP/main" || exit 1
    "${g[@]}" remote add origin "$TMP/remote.git"
    echo a >file.txt
    "${g[@]}" add file.txt
    "${g[@]}" commit -qm first
    "${g[@]}" push -q origin main
    "${g[@]}" remote set-head origin main
    "${g[@]}" branch --set-upstream-to=origin/main -q
    "${g[@]}" config alias.pf 'push --force'
  ) || return 1
  "${g[@]}" clone -q "$TMP/remote.git" "$TMP/pushed" 2>/dev/null
  (
    cd "$TMP/pushed" || exit 1
    "${g[@]}" switch -qc feat
    echo b >>file.txt
    "${g[@]}" commit -qam second
    "${g[@]}" push -qu origin feat
  ) || return 1
  "${g[@]}" clone -q "$TMP/remote.git" "$TMP/feat" 2>/dev/null
  (
    cd "$TMP/feat" || exit 1
    "${g[@]}" switch -q feat
    echo c >>file.txt
    "${g[@]}" commit -qam third
    "${g[@]}" config alias.pf 'push --force'
  ) || return 1
}
setup_repos || { echo "test-guardrails: could not create the throwaway repos" >&2; exit 1; }

# Runs the hook. Prints block, ask or allow.
run_hook() {
  local agent=$1 profile=$2 json=$3 out rc
  out=$("$HOOK" --agent "$agent" --profile "$profile" <<<"$json" 2>/dev/null)
  rc=$?
  if ((rc == 2)); then
    echo block
  elif ((rc == 0)) && [[ $out == *'"permissionDecision":"ask"'* ]]; then
    echo ask
  elif ((rc == 0)) && [[ -z $out ]]; then
    echo allow
  else
    echo "error(exit $rc)"
  fi
}

payload() { jq -cn --arg c "$1" --arg d "$2" '{tool_name: "Bash", tool_input: {command: $c}, cwd: $d}'; }

strictest() {
  local r=allow d
  for d in "$@"; do
    [[ $d == block ]] && { echo block; return; }
    [[ $d == ask ]] && r=ask
  done
  echo "$r"
}

expected() {
  local cats=$1 profile=$2 agent=$3 c d
  local -a ds=()
  case $cats in
    allow) echo allow; return ;;
    unverifiable) echo block; return ;;
  esac
  IFS=+ read -ra list <<<"$cats"
  for c in "${list[@]}"; do
    d=${CONF_VAL[$profile.$c]-block}
    [[ $d == ask && $agent != claude ]] && d=block
    ds+=("$d")
  done
  strictest "${ds[@]}"
}

PASS=0
FAIL=0
check() {
  local label=$1 want=$2 got=$3
  if [[ $want == "$got" ]]; then
    ((PASS++))
  else
    ((FAIL++))
    printf 'FAIL  %-60s expected %s, got %s\n' "$label" "$want" "$got"
  fi
}

# category (or allow / unverifiable) | repo | command
ROWS=$(
  cat <<'EOF'
push-default|feat|git push origin main
push-default|feat|git -C . push origin main
push-default|feat|git -c x=y push origin main
push-default|feat|git  push origin main
push-default|feat|sh -c 'git pu''sh origin main'
push-default|feat|/usr/bin/git push origin HEAD:main
push-default|feat|git push origin HEAD:refs/heads/main
push-default|main|git push
push-default|main|git -C . push
push-branch|feat|git push
push-branch|feat|git -C . push
push-branch|feat|git push -u origin feat
history-rewrite+push-branch|feat|git push --force origin feat
history-rewrite+push-branch|feat|git push -f
history-rewrite+push-branch|feat|git push --force-with-lease
history-rewrite+push-branch|feat|git push origin +feat
history-rewrite+push-branch|feat|git push origin --delete old
history-rewrite+push-branch|feat|git push origin :old
history-rewrite+push-branch|feat|git pf
destructive|feat|git reset --hard
destructive|feat|git reset  --hard HEAD~1
destructive|feat|git -C . reset --hard
destructive|feat|git clean -f
destructive|feat|git clean -fd
destructive|feat|git clean -xdf
destructive|feat|git branch -D old
destructive|feat|git branch --delete --force old
destructive|feat|git checkout -- .
destructive|feat|git checkout .
destructive|feat|git checkout -f main
destructive|feat|git restore .
destructive|feat|git restore file.txt
destructive|feat|git restore --staged --worktree .
destructive|feat|git stash drop
destructive|feat|git stash clear
destructive|feat|git switch -f main
destructive|feat|git switch --discard-changes main
destructive|feat|rm -rf .git
destructive|feat|rm -fr ./.git/
destructive|feat|cd /tmp && git clean -f
destructive|feat|echo ok; bash -c "git reset --hard"
destructive|feat|git status && git reset --hard
destructive|feat|echo $(git reset --hard)
destructive|feat|echo `git reset --hard`
destructive|feat|timeout 10 git reset --hard
destructive|feat|FOO=1 git reset --hard
destructive|feat|sudo -u me git reset --hard
destructive|feat|(git reset --hard)
destructive|feat|bash <<'SCRIPT'
git reset --hard
SCRIPT
history-rewrite+commit|pushed|git commit --amend -m x
commit|feat|git commit --amend -m x
history-rewrite|feat|git rebase main
history-rewrite|feat|git rebase -i HEAD~3
history-rewrite|feat|git update-ref -d refs/heads/main
history-rewrite|feat|git filter-branch --tree-filter true HEAD
history-rewrite|feat|git reflog expire --expire=now --all
commit|feat|git commit -m x
commit|feat|git commit -am "fix: something"
commit|feat|git commit -m 'git push origin main'
no-verify+commit|feat|git commit --no-verify -m x
no-verify+commit|feat|git commit -nm x
no-verify+commit|feat|HUSKY=0 git commit -m x
no-verify+commit|feat|git -c core.hooksPath=/dev/null commit -m x
no-verify+push-branch|feat|git push --no-verify origin feat
no-verify|feat|git config core.hooksPath /dev/null
pr-create|feat|gh pr create --fill
pr-merge|feat|gh pr merge 3
pr-merge|feat|gh pr merge 3 --squash --admin
allow|feat|git status
allow|feat|git log --oneline -5
allow|feat|git diff HEAD~1
allow|feat|echo 'git push origin main'
allow|feat|git status && echo 'git push is blocked'
allow|feat|grep -rn "git reset --hard" docs
allow|feat|git restore --staged file.txt
allow|feat|git checkout -b new-feature
allow|feat|git switch main
allow|feat|git branch -d merged
allow|feat|git stash
allow|feat|git stash list
allow|feat|git push --dry-run origin main
allow|feat|git rebase --abort
allow|feat|git clean -n
allow|feat|ls -la
allow|feat|cat > notes.md <<'EOF2'
git push --force origin main
EOF2
allow|feat|gh pr view 3
allow|feat|git fetch origin
unverifiable|feat|g=git; $g push origin main
unverifiable|feat|echo "git push origin main" | sh
unverifiable|feat|git -c alias.p=push p origin main
unverifiable|feat|git push 'origin main
EOF
)

# Rows are split on lines; a row that continues on the next lines (heredoc) is joined
# until the next line that starts with a known category.
rows=()
current=""
while IFS= read -r line; do
  if [[ $line =~ ^(allow|unverifiable|destructive|history-rewrite|no-verify|commit|push-branch|push-default|pr-create|pr-merge)[+a-z-]*\| ]]; then
    [[ -n $current ]] && rows+=("$current")
    current=$line
  else
    current+=$'\n'"$line"
  fi
done <<<"$ROWS"
[[ -n $current ]] && rows+=("$current")

for row in "${rows[@]}"; do
  cats=${row%%|*}
  rest=${row#*|}
  repo=${rest%%|*}
  cmd=${rest#*|}
  json=$(payload "$cmd" "$TMP/$repo")
  for profile in interactive afk; do
    check "[$profile] $cmd" "$(expected "$cats" "$profile" claude)" "$(run_hook claude "$profile" "$json")"
  done
done

# Agents without "ask": every ask becomes block.
json=$(payload "git push" "$TMP/feat")
check "[codex interactive] git push (ask becomes block)" "$(expected push-branch interactive codex)" "$(run_hook codex interactive "$json")"
check "[gemini interactive] git push (ask becomes block)" "$(expected push-branch interactive gemini)" "$(run_hook gemini interactive "$json")"

# Other input shapes.
json=$(jq -cn --arg d "$TMP/feat" '{tool_name: "Bash", tool_input: {command: ["bash", "-lc", "git reset --hard"]}, cwd: $d}')
check "command as an array (codex)" block "$(run_hook codex interactive "$json")"
json=$(jq -cn --arg d "$TMP/feat" '{tool_name: "run_shell_command", tool_input: {command: "git reset --hard"}, cwd: $d}')
check "gemini tool name" block "$(run_hook gemini interactive "$json")"
json=$(jq -cn --arg d "$TMP/feat" '{tool_name: "apply_patch", tool_input: {command: "git reset --hard"}, cwd: $d}')
check "non-shell tool with a command field is ignored" allow "$(run_hook codex interactive "$json")"
json=$(jq -cn '{tool_name: "Edit", tool_input: {file_path: "x"}}')
check "non-shell tool" allow "$(run_hook claude interactive "$json")"

# Fails closed.
check "unreadable JSON" block "$(run_hook claude interactive 'not json')"
check "shell tool without a command" block "$(run_hook claude interactive '{"tool_name":"Bash","tool_input":{}}')"
check "no tool_name" block "$(run_hook claude interactive '{"tool_input":{"command":"git status"}}')"
check "unknown profile" block "$(run_hook claude nightly "$(payload "git status" "$TMP/feat")")"

mkdir -p "$TMP/nojq"
ln -s "$(command -v git)" "$TMP/nojq/git"
out_rc=$(PATH="$TMP/nojq" "$BASH" "$HOOK" --agent claude --profile interactive <<<"$(payload "git push origin main" "$TMP/feat")" >/dev/null 2>&1; echo $?)
check "no jq on PATH" block "$([[ $out_rc == 2 ]] && echo block || echo "exit $out_rc")"

mkdir -p "$TMP/noconf"
cp "$HOOK" "$TMP/noconf/git-guardrails.sh"
nc_status=$("$TMP/noconf/git-guardrails.sh" --agent claude --profile interactive <<<"$(payload "git status" "$TMP/feat")" >/dev/null 2>&1; echo $?)
nc_commit=$("$TMP/noconf/git-guardrails.sh" --agent claude --profile afk <<<"$(payload "git commit -m x" "$TMP/feat")" >/dev/null 2>&1; echo $?)
check "missing config: read-only git still allowed" 0 "$nc_status"
check "missing config: git commit blocked" 2 "$nc_commit"

printf '\n%d passed, %d failed\n' "$PASS" "$FAIL"
((FAIL == 0))
