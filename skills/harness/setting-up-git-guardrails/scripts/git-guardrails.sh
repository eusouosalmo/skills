#!/usr/bin/env bash
# git-guardrails: PreToolUse hook that stops risky git commands from a coding agent.
#
# Usage, as registered in the agent's hook config:
#   git-guardrails.sh --agent claude|codex|gemini --profile interactive|afk
#
# Reads the hook JSON on stdin and decides per category, using git-guardrails.conf
# next to this script. Exit 2 blocks, with the reason on stderr (every supported
# agent reads exit 2 as a block). Exit 0 allows. "ask" exists only on Claude Code,
# as JSON on stdout; the other agents get a block that tells the agent to ask.
#
# Fails closed: no jq, unreadable JSON, a command it cannot parse, a missing config
# or any internal error blocks. It protects against a distracted model, not an
# adversary: branch protection on the server is the real barrier.
#
# Based on the idea of Matt Pocock's git-guardrails-claude-code skill (MIT), rewritten
# to parse the command instead of matching regexes on the raw text.
#
# Needs: bash 4+, jq, git. No other external command.

set -u
export LC_ALL=C # byte-wise string indexing: faster, and no locale surprises in the lexer

DONE=0
on_exit() {
  local rc=$?
  if [[ $DONE != 1 ]]; then
    printf 'git-guardrails: internal error (exit %s), blocking to be safe. Ask the user to check the hook.\n' "$rc" >&2
    exit 2
  fi
}
trap on_exit EXIT

finish() { DONE=1; exit "$1"; }

block() {
  printf 'git-guardrails: blocked. %s\n' "$1" >&2
  finish 2
}

AGENT=""
PROFILE=""
while (($#)); do
  case $1 in
    --agent) AGENT=${2-}; shift 2 || block "missing value for --agent in the hook registration." ;;
    --profile) PROFILE=${2-}; shift 2 || block "missing value for --profile in the hook registration." ;;
    *) block "unknown argument '$1' in the hook registration." ;;
  esac
done
case $AGENT in claude | codex | gemini) ;; *) block "unknown --agent '$AGENT' in the hook registration." ;; esac
case $PROFILE in interactive | afk) ;; *) block "unknown --profile '$PROFILE' in the hook registration." ;; esac

HOOK_DIR=${BASH_SOURCE[0]%/*}
[[ $HOOK_DIR == "${BASH_SOURCE[0]}" ]] && HOOK_DIR=.
CONF="$HOOK_DIR/git-guardrails.conf"

# ---------- config ----------

declare -A CONF_VAL=()
DEFAULT_BRANCH_CONF=""
load_conf() {
  [[ -r $CONF ]] || return 1
  local line key val
  while IFS= read -r line || [[ -n $line ]]; do
    line=${line%%#*}
    line=${line//[[:space:]]/}
    [[ -z $line ]] && continue
    [[ $line == *=* ]] || continue
    key=${line%%=*}
    val=${line#*=}
    if [[ $key == default-branch ]]; then
      DEFAULT_BRANCH_CONF=$val
    else
      CONF_VAL[$key]=$val
    fi
  done <"$CONF"
}
CONF_OK=1
load_conf || CONF_OK=0

# Decision for a category in the active profile. Unknown or missing values block.
decision_for() {
  local v=""
  ((CONF_OK)) && v=${CONF_VAL[$PROFILE.$1]-}
  case $v in block | ask | allow) printf '%s' "$v" ;; *) printf 'block' ;; esac
}

# ---------- input ----------

command -v jq >/dev/null 2>&1 || block "jq is not installed, so the command cannot be checked. Ask the user to install jq."

INPUT=""
IFS= read -r -d '' INPUT || true
[[ -n $INPUT ]] || block "empty hook input."

TOOL_NAME=$(jq -r 'if type == "object" then (.tool_name // "") else error("not an object") end' <<<"$INPUT" 2>/dev/null) ||
  block "unreadable hook input (not the expected JSON)."

# Shell tool names seen across agents. Any other tool (Edit, apply_patch...) is not ours.
case $TOOL_NAME in
  Bash | Shell | bash | shell | run_shell_command | execute_bash | runTerminalCommand | run_in_terminal) ;;
  "") block "hook input has no tool_name." ;;
  *) finish 0 ;;
esac

CMD=$(jq -r '.tool_input.command | if type == "array" then map(@sh) | join(" ") elif type == "string" then . else error("no command") end' <<<"$INPUT" 2>/dev/null) ||
  block "hook input has no readable tool_input.command."
CWD=$(jq -r '.cwd // ""' <<<"$INPUT" 2>/dev/null) || CWD=""
[[ -n $CWD && -d $CWD ]] || CWD=$PWD

# Fast path: nothing that looks like git, gh or rm once quotes and backslashes are gone.
STRIPPED=${CMD//[\'\"\\]/}
if ! [[ $STRIPPED =~ (^|[^[:alnum:]_.-])(git|gh|rm)([^[:alnum:]_-]|$) ]]; then
  finish 0
fi

# ---------- lexer ----------
# Splits a shell string into tokens with quotes removed. Segment boundaries (; & | && ||
# newline parentheses) become the token $SEP. Redirections become $REDIR followed by
# their target. Command substitutions ($(...) and backticks) and heredoc bodies are
# stored in LEX_SUBS and LEX_HEREDOCS for a recursive check.

SEP=$'\x1f'
REDIR=$'\x1e'
HEREDOC_MARK=$'\x1d'
LEX_TOKENS=()
LEX_SUBS=()
LEX_HEREDOCS=()

lex() {
  local s=$1 n=${#1} i=0 c tok="" has=0 depth j q
  local -a pending_heredocs=()
  LEX_TOKENS=()
  LEX_SUBS=()
  LEX_HEREDOCS=()

  push_tok() {
    if ((has)); then LEX_TOKENS+=("$tok"); fi
    tok=""
    has=0
  }

  # Captures a $( ... ) starting at i (pointing at '('); sets i after the closing ')'.
  capture_paren() {
    local start=$((i + 1)) d=1 ch inq=""
    ((i++))
    while ((i < n)); do
      ch=${s:i:1}
      if [[ -n $inq ]]; then
        if [[ $ch == "$inq" ]]; then inq=""; elif [[ $ch == '\' && $inq == '"' ]]; then ((i++)); fi
      else
        case $ch in
          "'" | '"') inq=$ch ;;
          '\') ((i++)) ;;
          '(') ((d++)) ;;
          ')')
            ((d--))
            if ((d == 0)); then
              LEX_SUBS+=("${s:start:i-start}")
              ((i++))
              return 0
            fi
            ;;
        esac
      fi
      ((i++))
    done
    return 1
  }

  capture_backtick() {
    local start=$((i + 1))
    ((i++))
    while ((i < n)); do
      if [[ ${s:i:1} == '\' ]]; then
        ((i += 2))
        continue
      fi
      if [[ ${s:i:1} == '`' ]]; then
        LEX_SUBS+=("${s:start:i-start}")
        ((i++))
        return 0
      fi
      ((i++))
    done
    return 1
  }

  # At a newline with pending heredocs: consume their bodies.
  read_heredocs() {
    local delim strip line body nl
    for delim in "${pending_heredocs[@]}"; do
      strip=0
      if [[ $delim == -* ]]; then
        strip=1
        delim=${delim:1}
      fi
      body=""
      while ((i < n)); do
        nl=$i
        while ((nl < n)) && [[ ${s:nl:1} != $'\n' ]]; do ((nl++)); done
        line=${s:i:nl-i}
        i=$((nl + 1))
        if ((strip)); then
          while [[ $line == $'\t'* ]]; do line=${line:1}; done
        fi
        [[ $line == "$delim" ]] && break
        body+="$line"$'\n'
      done
      LEX_HEREDOCS+=("$body")
      LEX_TOKENS+=("$HEREDOC_MARK$((${#LEX_HEREDOCS[@]} - 1))")
    done
    pending_heredocs=()
  }

  while ((i < n)); do
    c=${s:i:1}
    case $c in
      '\')
        if [[ ${s:i+1:1} == $'\n' ]]; then
          ((i += 2))
        else
          tok+=${s:i+1:1}
          has=1
          ((i += 2))
        fi
        continue
        ;;
      "'")
        j=$((i + 1))
        while ((j < n)) && [[ ${s:j:1} != "'" ]]; do ((j++)); done
        ((j < n)) || return 1
        tok+=${s:i+1:j-i-1}
        has=1
        i=$((j + 1))
        continue
        ;;
      '"')
        has=1
        ((i++))
        while true; do
          ((i < n)) || return 1
          c=${s:i:1}
          if [[ $c == '"' ]]; then
            ((i++))
            break
          elif [[ $c == '\' ]]; then
            q=${s:i+1:1}
            case $q in '"' | '\' | '$' | '`') tok+=$q ;; $'\n') ;; *) tok+="\\$q" ;; esac
            ((i += 2))
          elif [[ $c == '$' && ${s:i+1:1} == '(' ]]; then
            ((i++))
            capture_paren || return 1
            tok+='$SUB'
          elif [[ $c == '`' ]]; then
            capture_backtick || return 1
            tok+='$SUB'
          else
            tok+=$c
            ((i++))
          fi
        done
        continue
        ;;
      '$')
        if [[ ${s:i+1:1} == '(' ]]; then
          ((i++))
          capture_paren || return 1
          tok+='$SUB'
          has=1
          continue
        fi
        tok+=$c
        has=1
        ;;
      '`')
        capture_backtick || return 1
        tok+='$SUB'
        has=1
        continue
        ;;
      ' ' | $'\t')
        push_tok
        ;;
      $'\n')
        push_tok
        ((i++))
        ((${#pending_heredocs[@]})) && read_heredocs
        LEX_TOKENS+=("$SEP")
        continue
        ;;
      ';' | '(' | ')')
        push_tok
        LEX_TOKENS+=("$SEP")
        ;;
      '&' | '|')
        if [[ $c == '&' && ${s:i+1:1} == '>' ]]; then
          push_tok
          ((i += 2))
          [[ ${s:i:1} == '>' ]] && ((i++))
          LEX_TOKENS+=("$REDIR")
          continue
        fi
        push_tok
        LEX_TOKENS+=("$SEP")
        [[ ${s:i+1:1} == "$c" || ${s:i+1:1} == '&' ]] && ((i++))
        ;;
      '<' | '>')
        # A token made only of digits right before is a file descriptor (2>&1).
        if ((has)) && [[ $tok =~ ^[0-9]+$ ]]; then
          tok=""
          has=0
        fi
        push_tok
        if [[ ${s:i:3} == '<<<' ]]; then
          ((i += 3))
          LEX_TOKENS+=("$REDIR")
          continue
        fi
        if [[ ${s:i:2} == '<<' ]]; then
          ((i += 2))
          local dash=""
          if [[ ${s:i:1} == '-' ]]; then
            dash="-"
            ((i++))
          fi
          while [[ ${s:i:1} == ' ' || ${s:i:1} == $'\t' ]]; do ((i++)); done
          local d=""
          while ((i < n)); do
            c=${s:i:1}
            case $c in
              ' ' | $'\t' | $'\n' | ';' | '&' | '|' | '<' | '>' | '(' | ')') break ;;
              "'" | '"' | '\') ;;
              *) d+=$c ;;
            esac
            ((i++))
          done
          [[ -n $d ]] || return 1
          pending_heredocs+=("$dash$d")
          continue
        fi
        ((i++))
        while [[ ${s:i:1} == '>' || ${s:i:1} == '&' || ${s:i:1} == '|' ]]; do ((i++)); done
        LEX_TOKENS+=("$REDIR")
        continue
        ;;
      '#')
        if ((has)); then
          tok+=$c
        else
          while ((i < n)) && [[ ${s:i:1} != $'\n' ]]; do ((i++)); done
          continue
        fi
        ;;
      *)
        tok+=$c
        has=1
        ;;
    esac
    ((i++))
  done
  push_tok
  ((${#pending_heredocs[@]})) && return 1 # heredoc never terminated by a newline
  return 0
}

# ---------- classification ----------

CATS=()         # categories found, one entry per hit
CAT_WHAT=()     # the command text for each hit
UNVERIFIABLE=() # reasons the command could not be checked

hit() {
  CATS+=("$1")
  CAT_WHAT+=("$2")
}

# Branch names: the remote's default branch, or the configured one, or main and master.
default_branches() {
  local dir=$1 remote=$2 ref
  if [[ -n $DEFAULT_BRANCH_CONF ]]; then
    printf '%s\n' "$DEFAULT_BRANCH_CONF"
    return
  fi
  if ref=$(git -C "$dir" symbolic-ref --quiet --short "refs/remotes/$remote/HEAD" 2>/dev/null) && [[ -n $ref ]]; then
    printf '%s\n' "${ref#"$remote"/}"
    return
  fi
  printf 'main\nmaster\n'
}

is_short_cluster() { [[ $1 =~ ^-[A-Za-z]+$ ]]; }

check_git_push() {
  local dir=$1 what=$2
  shift 2
  local -a pos=()
  local t rewrite=0 all=0 dry=0 noverify=0
  while (($#)); do
    t=$1
    shift
    case $t in
      --force | --force-with-lease* | --force-if-includes | --mirror | --prune | --delete) rewrite=1 ;;
      --no-verify) noverify=1 ;;
      --all | --branches) all=1 ;;
      --dry-run) dry=1 ;;
      -o | --push-option | --repo | --receive-pack | --exec) shift ;;
      --*) ;;
      -*)
        if is_short_cluster "$t"; then
          [[ $t == *f* || $t == *d* ]] && rewrite=1
          [[ $t == *n* ]] && dry=1
        fi
        ;;
      *) pos+=("$t") ;;
    esac
  done
  ((dry)) && return
  ((noverify)) && hit no-verify "$what"
  local remote=${pos[0]-origin}
  local -a specs=("${pos[@]:1}")
  local s
  for s in "${specs[@]}"; do
    [[ $s == +* || $s == :* ]] && rewrite=1
  done
  ((rewrite)) && hit history-rewrite "$what"

  local -a targets=()
  local cur up dst
  cur=$(git -C "$dir" symbolic-ref --quiet --short HEAD 2>/dev/null) || cur=""
  if ((all)); then
    hit push-default "$what"
    return
  fi
  if ((${#specs[@]} == 0)); then
    if [[ -z $cur ]]; then
      hit push-default "$what" # detached HEAD or not a repo: cannot tell the target
      return
    fi
    targets+=("$cur")
    up=$(git -C "$dir" rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null) && targets+=("${up#*/}")
  else
    for s in "${specs[@]}"; do
      s=${s#+}
      if [[ $s == *:* ]]; then dst=${s#*:}; else dst=$s; fi
      [[ -z $dst ]] && continue
      if [[ $dst == HEAD ]]; then
        if [[ -z $cur ]]; then
          hit push-default "$what"
          return
        fi
        dst=$cur
      fi
      dst=${dst#refs/heads/}
      targets+=("$dst")
    done
  fi
  local b tgt
  while IFS= read -r b; do
    for tgt in "${targets[@]}"; do
      if [[ $tgt == "$b" ]]; then
        hit push-default "$what"
        return
      fi
    done
  done < <(default_branches "$dir" "$remote")
  hit push-branch "$what"
}

check_git_commit() {
  local dir=$1 what=$2
  shift 2
  local t amend=0 noverify=0
  while (($#)); do
    t=$1
    shift
    case $t in
      --amend) amend=1 ;;
      --no-verify) noverify=1 ;;
      -m | -F | -C | -c | -t | --author | --date | --fixup | --squash | --template | --trailer | --cleanup | --file | --message) shift ;;
      --*) ;;
      -*)
        if is_short_cluster "$t"; then
          [[ $t == *n* ]] && noverify=1
          [[ $t =~ [mFCct]$ ]] && shift
        fi
        ;;
    esac
  done
  hit commit "$what"
  ((noverify)) && hit no-verify "$what"
  if ((amend)); then
    local remotes
    if ! remotes=$(git -C "$dir" branch -r --contains HEAD 2>/dev/null); then
      hit history-rewrite "$what" # cannot tell whether HEAD was pushed: assume it was
    elif [[ -n $remotes ]]; then
      hit history-rewrite "$what"
    fi
  fi
}

check_git() {
  local dir=$1 what=$2 depth=$3
  shift 3
  local t kv
  # Global options between "git" and the subcommand.
  while (($#)); do
    t=$1
    case $t in
      -C)
        [[ ${2-} == /* ]] && dir=${2-} || dir="$dir/${2-}"
        shift 2 || return
        ;;
      -c)
        kv=${2-}
        shift 2 || return
        case ${kv,,} in
          core.hookspath*) hit no-verify "$what" ;;
          alias.*) UNVERIFIABLE+=("git alias defined inline with -c ($what)") ;;
        esac
        ;;
      --git-dir | --work-tree | --namespace | --config-env | --super-prefix) shift 2 || return ;;
      -*) shift ;;
      *) break ;;
    esac
  done
  (($#)) || return
  local sub=$1
  shift
  local a has_ddash=0 after_ddash=0 staged=0 worktree=0 del=0 force=0 abort=0
  case $sub in
    reset)
      for a in "$@"; do [[ $a == --hard ]] && hit destructive "$what"; done
      ;;
    clean)
      for a in "$@"; do
        [[ $a == --force ]] && force=1
        is_short_cluster "$a" && [[ $a == *f* ]] && force=1
      done
      ((force)) && hit destructive "$what"
      ;;
    checkout)
      for a in "$@"; do
        if ((has_ddash)); then
          after_ddash=1
          continue
        fi
        case $a in
          --) has_ddash=1 ;;
          --force | . | ./ | :/ | ':(top)' | --ours | --theirs) force=1 ;;
          -*) is_short_cluster "$a" && [[ $a == *f* ]] && force=1 ;;
        esac
      done
      ((force || after_ddash)) && hit destructive "$what"
      ;;
    restore)
      for a in "$@"; do
        case $a in
          --staged) staged=1 ;;
          --worktree) worktree=1 ;;
          --*) ;;
          -*)
            if is_short_cluster "$a"; then
              [[ $a == *S* ]] && staged=1
              [[ $a == *W* ]] && worktree=1
            fi
            ;;
        esac
      done
      ((staged && !worktree)) || hit destructive "$what"
      ;;
    branch)
      for a in "$@"; do
        case $a in
          --delete) del=1 ;;
          --force) force=1 ;;
          --*) ;;
          -*)
            if is_short_cluster "$a"; then
              [[ $a == *D* ]] && del=1 force=1
              [[ $a == *d* ]] && del=1
              [[ $a == *f* ]] && force=1
            fi
            ;;
        esac
      done
      ((del && force)) && hit destructive "$what"
      ;;
    stash)
      for a in "$@"; do
        [[ $a == -* ]] && continue
        [[ $a == drop || $a == clear ]] && hit destructive "$what"
        break
      done
      ;;
    switch)
      for a in "$@"; do
        case $a in
          --force | --discard-changes) force=1 ;;
          --*) ;;
          -*) is_short_cluster "$a" && [[ $a == *f* ]] && force=1 ;;
        esac
      done
      ((force)) && hit destructive "$what"
      ;;
    push) check_git_push "$dir" "$what" "$@" ;;
    commit) check_git_commit "$dir" "$what" "$@" ;;
    rebase)
      for a in "$@"; do
        [[ $a == --abort || $a == --quit ]] && abort=1
        [[ $a == --no-verify ]] && hit no-verify "$what"
      done
      ((abort)) || hit history-rewrite "$what"
      ;;
    update-ref | filter-branch | filter-repo) hit history-rewrite "$what" ;;
    reflog)
      [[ ${1-} == expire || ${1-} == delete ]] && hit history-rewrite "$what"
      ;;
    merge | am | cherry-pick | revert)
      for a in "$@"; do [[ $a == --no-verify ]] && hit no-verify "$what"; done
      ;;
    config)
      for a in "$@"; do [[ ${a,,} == core.hookspath ]] && hit no-verify "$what"; done
      ;;
    *)
      # A repo or user alias: expand it once and check the result.
      local alias
      if ((depth < 4)) && alias=$(git -C "$dir" config --get "alias.$sub" 2>/dev/null) && [[ -n $alias ]]; then
        local -a rest=()
        local x
        for x in "$@"; do rest+=("$(printf '%q' "$x")"); done
        if [[ $alias == '!'* ]]; then
          check_string "${alias:1} ${rest[*]}" "$dir" $((depth + 1))
        else
          check_string "git $alias ${rest[*]}" "$dir" $((depth + 1))
        fi
      fi
      ;;
  esac
}

check_gh() {
  local what=$1
  shift
  local -a pos=()
  local a merge_api=0 put=0
  for a in "$@"; do
    [[ $a == -* ]] || pos+=("$a")
  done
  if [[ ${pos[0]-} == pr ]]; then
    case ${pos[1]-} in
      create | new) hit pr-create "$what" ;;
      merge) hit pr-merge "$what" ;;
    esac
  elif [[ ${pos[0]-} == api ]]; then
    for a in "$@"; do
      [[ $a == */merge ]] && merge_api=1
      [[ ${a^^} == PUT || $a == -XPUT || $a == --method=PUT ]] && put=1
    done
    ((merge_api && put)) && hit pr-merge "$what"
  fi
}

SHELLS=" sh bash zsh dash ksh "
# Words that make a segment with a dynamic command name worth blocking.
RISKY_WORDS=" push reset clean checkout restore branch stash switch rebase update-ref commit merge filter-branch "

check_segment() {
  local dir=$1 depth=$2
  shift 2
  local -a argv=()
  local -a heredocs=()
  local t skip_next=0
  for t in "$@"; do
    if ((skip_next)); then
      skip_next=0
      continue
    fi
    if [[ $t == "$REDIR" ]]; then
      skip_next=1
      continue
    fi
    if [[ $t == "$HEREDOC_MARK"* ]]; then
      heredocs+=("${t#"$HEREDOC_MARK"}")
      continue
    fi
    argv+=("$t")
  done
  ((${#argv[@]})) || return

  # Leading assignments and wrappers.
  local noverify_env=0 i=0 name
  while ((i < ${#argv[@]})); do
    t=${argv[i]}
    if [[ $t =~ ^[A-Za-z_][A-Za-z0-9_]*= ]]; then
      case $t in HUSKY=0 | LEFTHOOK=0 | HUSKY_SKIP_HOOKS=*) noverify_env=1 ;; esac
      ((i++))
      continue
    fi
    name=${t##*/}
    case $name in
      sudo | env | command | builtin | exec | nohup | time | nice | stdbuf | '{' | '!' | if | then | else | elif | do | while | until)
        ((i++))
        while ((i < ${#argv[@]})) && [[ ${argv[i]} == -* ]]; do
          # Options of sudo, env and nice that take a separate value.
          case $name:${argv[i]} in
            sudo:-u | sudo:-g | sudo:-h | sudo:-p | sudo:-C | sudo:-U | sudo:-r | sudo:-t | sudo:-D | env:-u | env:-C | env:-S | nice:-n) ((i++)) ;;
          esac
          ((i++))
        done
        ;;
      timeout)
        ((i++))
        while ((i < ${#argv[@]})) && [[ ${argv[i]} == -* ]]; do ((i++)); done
        ((i++)) # the duration
        ;;
      xargs)
        ((i++))
        while ((i < ${#argv[@]})) && [[ ${argv[i]} == -* ]]; do
          case ${argv[i]} in -I | -n | -L | -P | -d | -s | -E | -a) ((i++)) ;; esac
          ((i++))
        done
        ;;
      *) break ;;
    esac
  done
  ((i < ${#argv[@]})) || return
  argv=("${argv[@]:i}")
  local cmd0=${argv[0]}
  local base=${cmd0##*/}
  local what="${argv[*]}"

  if [[ $cmd0 == *'$'* ]]; then
    local w
    for w in "${argv[@]:1}"; do
      if [[ $RISKY_WORDS == *" $w "* ]]; then
        UNVERIFIABLE+=("command name comes from a variable or substitution ($what)")
        return
      fi
    done
    return
  fi

  if [[ $SHELLS == *" $base "* ]]; then
    local j=1 a found=0
    while ((j < ${#argv[@]})); do
      a=${argv[j]}
      if [[ $a == -*c* && $a != --* ]]; then
        ((j + 1 < ${#argv[@]})) && check_string "${argv[j + 1]}" "$dir" $((depth + 1))
        found=1
        break
      fi
      [[ $a == -* ]] || break
      ((j++))
    done
    if ((!found)); then
      local h
      for h in "${heredocs[@]}"; do
        check_string "${LEX_HEREDOCS_SAVED[h]}" "$dir" $((depth + 1))
        found=1
      done
    fi
    if ((!found)) && ((j >= ${#argv[@]})); then
      UNVERIFIABLE+=("a shell reads commands from a pipe or stdin ($what)")
    fi
    return
  fi

  case $base in
    eval) check_string "${argv[*]:1}" "$dir" $((depth + 1)) ;;
    git)
      if ((noverify_env)); then
        case " ${argv[*]} " in *" commit "* | *" push "* | *" merge "*) hit no-verify "$what" ;; esac
      fi
      check_git "$dir" "$what" "$depth" "${argv[@]:1}"
      ;;
    gh) check_gh "$what" "${argv[@]:1}" ;;
    rm)
      local a rec=0 gitdir=0
      for a in "${argv[@]:1}"; do
        case $a in
          --recursive) rec=1 ;;
          --*) ;;
          -*) [[ $a == *r* || $a == *R* ]] && rec=1 ;;
          *) [[ $a =~ (^|/)\.git/?$ ]] && gitdir=1 ;;
        esac
      done
      ((rec && gitdir)) && hit destructive "$what"
      ;;
  esac
}

LEX_HEREDOCS_SAVED=()

check_string() {
  local str=$1 dir=$2 depth=$3
  if ((depth > 6)); then
    UNVERIFIABLE+=("too many nested shells")
    return
  fi
  if ! lex "$str"; then
    UNVERIFIABLE+=("unbalanced quotes or an unterminated substitution or heredoc")
    return
  fi
  local -a toks=("${LEX_TOKENS[@]}")
  local -a subs=("${LEX_SUBS[@]}")
  local -a docs=("${LEX_HEREDOCS[@]}")
  local s
  for s in "${subs[@]}"; do check_string "$s" "$dir" $((depth + 1)); done

  local -a seg=()
  local t
  local -a saved_outer=("${LEX_HEREDOCS_SAVED[@]}")
  LEX_HEREDOCS_SAVED=("${docs[@]}")
  for t in "${toks[@]}" "$SEP"; do
    if [[ $t == "$SEP" ]]; then
      ((${#seg[@]})) && check_segment "$dir" "$depth" "${seg[@]}"
      LEX_HEREDOCS_SAVED=("${docs[@]}")
      seg=()
    else
      seg+=("$t")
    fi
  done
  LEX_HEREDOCS_SAVED=("${saved_outer[@]}")
}

# ---------- decide ----------

check_string "$CMD" "$CWD" 0

if ((${#UNVERIFIABLE[@]})); then
  block "could not verify this command: ${UNVERIFIABLE[0]}. Rewrite it as a plain git command, or ask the user to run it."
fi

if ((!CONF_OK)) && ((${#CATS[@]})); then
  block "config file $CONF is missing or unreadable, so every git write is blocked. Ask the user to restore it."
fi

FINAL=allow
REASON=""
CONF_FILE_HINT=$CONF
for idx in "${!CATS[@]}"; do
  d=$(decision_for "${CATS[idx]}")
  if [[ $d == block ]]; then
    FINAL=block
    REASON="'${CAT_WHAT[idx]}' is in category ${CATS[idx]}, which profile $PROFILE blocks"
    break
  elif [[ $d == ask && $FINAL == allow ]]; then
    FINAL=ask
    REASON="'${CAT_WHAT[idx]}' is in category ${CATS[idx]}, which profile $PROFILE sends to the user"
  fi
done

case $FINAL in
  allow) finish 0 ;;
  block)
    block "$REASON. The user set this rule in $CONF_FILE_HINT; do not try another way to run it. If it is needed, stop and ask the user to run it."
    ;;
  ask)
    if [[ $AGENT == claude ]]; then
      jq -cn --arg r "git-guardrails: $REASON." \
        '{hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: "ask", permissionDecisionReason: $r}}'
      finish 0
    fi
    block "$REASON. This agent cannot ask for approval from a hook, so stop and ask the user to run it."
    ;;
esac
