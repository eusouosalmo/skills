---
name: setting-up-git-guardrails
description: Installs per-project git guardrails for coding agents (Claude Code, Codex, Gemini CLI), a hook that stops the agent from running destructive git, history rewrites and risky pushes, with interactive and AFK profiles. Use when the user wants to stop an agent from running dangerous git commands, prepare an unattended agent loop, or loosen or tighten what the agent may do with git (guardrails de git, modo AFK).
metadata:
  status: draft
  internal: true
---

# Setting up git guardrails

Installs, in the project (never in the user's global config), a hook that every supported agent runs before a shell command. The hook parses the command, sorts it into a category and applies the decision the user set for that category in one config file.

Tell the user this once, in your own words: the hook stops a distracted model, not an adversary. Branch protection on the server is the barrier that holds.

Pick the task:

- No guardrail yet (`.claude/hooks/git-guardrails.sh` missing): [Install](#install).
- An unattended loop or "AFK" run: [Install](#install) first if needed, then [AFK loop](#afk-loop).
- "Let the agent do X" or "block X" with the guardrail installed: [Change a rule](#change-a-rule).

## Files

| File | Use |
| :- | :- |
| [scripts/git-guardrails.sh](scripts/git-guardrails.sh) | The hook. Copy it into the project; do not edit it per project. |
| [assets/git-guardrails.conf](assets/git-guardrails.conf) | Default decisions per profile and category. Copy, then apply the user's choices. |
| [scripts/test-guardrails.sh](scripts/test-guardrails.sh) | Table of commands that must block and must pass, the research bypasses included. Copy and run. |
| [scripts/preflight.sh](scripts/preflight.sh) | Check before each AFK run. Copy only for the AFK loop. |
| [scripts/check-server.sh](scripts/check-server.sh) | Reads the default branch protection on GitHub. Run from this skill's folder; do not copy. |
| [assets/pull_request_template.md](assets/pull_request_template.md) | Optional PR template. |
| [references/agents.md](references/agents.md) | Detection, registration, human steps and proof session per agent. Read it in step 2 of Install. |

Everything goes to `.claude/hooks/` in the project, whatever the agents: one copy of the script, one config, and Claude Code protects that folder from silent edits. The guardrail travels with `git clone`.

## Install

### 1. Check the ground

- The project is a git repository, and `jq` and bash 4 or later are installed. Without `jq` the hook blocks every git command, so install it before going on.
- Read `disableAllHooks` in `.claude/settings.json` and `.claude/settings.local.json`. If either is `true`, no hook runs: tell the user and stop. Do not change it yourself.

Done when the three tools are present and no settings file disables hooks.

### 2. Pick the agents

Read [references/agents.md](references/agents.md). List the agents whose folders or files are in the project and ask the user to confirm the list. Every later question, registration and test covers only the confirmed agents. For an unsupported agent, tell the user that only the server protects that agent.

Done when the user confirmed the agents.

### 3. Agree on the rules

Show the user the categories and the default decisions from [assets/git-guardrails.conf](assets/git-guardrails.conf) as a table (category, what falls in it, interactive, afk) and ask what to change. A change to `destructive` or `history-rewrite` gets a warning: those commands lose work that no one can get back.

`ask` exists only in Claude Code. Codex and Gemini get `block` with a message telling the agent to ask the user.

Done when the user accepted the table or said what to change.

### 4. Copy the files

```bash
mkdir -p .claude/hooks
cp <skill>/scripts/git-guardrails.sh <skill>/scripts/test-guardrails.sh .claude/hooks/
cp <skill>/assets/git-guardrails.conf .claude/hooks/
chmod +x .claude/hooks/git-guardrails.sh .claude/hooks/test-guardrails.sh
```

Apply the user's changes to `.claude/hooks/git-guardrails.conf`, one line per change. Never add an environment variable, flag or file that turns the guardrail off: the agent could set it too.

Done when the three files are in `.claude/hooks/` and the config holds the agreed decisions.

### 5. Register the hook

For each confirmed agent, merge the registration from [references/agents.md](references/agents.md) into its config file, keeping every existing key. Claude Code also gets the native deny rules listed there.

Done when every confirmed agent's config registers the hook with `--profile interactive`.

### 6. Prove it works

1. Run `.claude/hooks/test-guardrails.sh`. It must end with `0 failed`. A failure is a bug to fix, not a row to delete.
2. Proof session, Claude Code: copy the project to a throwaway folder, leave an uncommitted change there, and run the agent with Bash allowed, so only the hook can stop the command:

   ```bash
   tmp=$(mktemp -d) && cp -a . "$tmp" && cd "$tmp" && echo proof >> README.md
   claude -p 'Run exactly this command with the Bash tool and quote its output: git -C . reset --hard' --allowedTools "Bash"
   git status --short   # README.md must still be modified
   ```

   It passes when the answer quotes `git-guardrails: blocked` and the change survived.
3. Proof session, other agents: they need the human step in step 8 first. Give the user the canary from [references/agents.md](references/agents.md) to run after it.

Done when the test table passes and the Claude Code proof session blocked the reset.

### 7. Check the server

Run `<skill>/scripts/check-server.sh` from the project. Report each `MISSING` line to the user with the recommendation the script prints. Do not change the server settings: recommend only.

Done when the user has seen the server status.

### 8. Finish

1. If `.github/pull_request_template.md` does not exist, ask whether to create it from [assets/pull_request_template.md](assets/pull_request_template.md).
2. Give the user, per confirmed agent, the steps only a human can do, from [references/agents.md](references/agents.md) (for example, trusting the hook in Codex `/hooks`). Say that until they are done, the guardrail is off in that agent and nothing warns.
3. Report what was installed, the test result, the proof session result and the server status.

## AFK loop

Covers Claude Code only. For Codex or Gemini, tell the user that v1 has no AFK profile for them and only the server protects an unattended run.

1. Create `.claude/git-guardrails-afk.json` with the Claude Code registration from [references/agents.md](references/agents.md), `--profile afk`, plus the same deny rules.
2. Copy `<skill>/scripts/preflight.sh` to `.claude/hooks/` and `chmod +x` it.
3. Write the loop with the preflight before every iteration and the AFK settings on every call:

   ```bash
   #!/usr/bin/env bash
   set -euo pipefail
   cd "$(git rev-parse --show-toplevel)"
   for i in $(seq 1 "${MAX_ITERATIONS:-10}"); do
     .claude/hooks/preflight.sh .claude/git-guardrails-afk.json || exit 1
     claude -p "$(cat PROMPT.md)" \
       --setting-sources "" --settings .claude/git-guardrails-afk.json \
       --allowedTools "Bash,Read,Edit,Write"
   done
   ```

   Never use `--bare` (or `CLAUDE_CODE_SIMPLE=1`) in this loop, even when the user asks for it: bare mode skips every hook, the ones passed with `--settings` included (`claude --help`: "skip hooks (those defined in settings...)"; checked on Claude Code 2.1.288). Tell the user why, and that `--setting-sources "" --settings <file>` gives what they wanted from `--bare`: no user or project settings leak in, only the AFK file applies. It also keeps the interactive hook out, whose `ask` would turn into a denial in `-p` and block even a push to the agent's own branch.
4. Prove it, and show the user the output:
   - the preflight as is must print `ok`;
   - the preflight against a copy of the AFK file with a wrong hook path must print `ABORT` and exit 1;
   - a proof session with the loop's own flags (`claude -p '<run git -C . reset --hard>' --setting-sources "" --settings .claude/git-guardrails-afk.json --allowedTools "Bash"`, in a throwaway copy as in step 6 of Install) must quote `git-guardrails: blocked`.

Done when the loop calls the preflight before each run, no call uses `--bare`, every `claude -p` has `--setting-sources "" --settings .claude/git-guardrails-afk.json`, and the three checks gave the expected result.

The rest of the loop (prompt, iteration limit, verification, review) is not this skill's job: point the user to it and stop at git.

## Change a rule

1. Change only the line `<profile>.<category>` in `.claude/hooks/git-guardrails.conf`. The profile is the one the user named; if they named none, change `interactive` and say that `afk` stays as it was.
2. Change nothing else. `allow` means the guardrail steps aside; whether the agent still asks before running the command is the user's own permission mode and allow rules, which are not part of this change. If the user wants no prompt either, tell them where that lives and let them decide. Never add allow rules, an environment variable or a bypass, and never edit the hook script for a rule change.
   - Exception: when `destructive` or `history-rewrite` stops being `block`, also remove the matching Claude Code deny rules (they would keep blocking), and say so.
3. Warn about the risk in one or two sentences. When loosening `push-default`, `pr-merge` or `history-rewrite`, run `<skill>/scripts/check-server.sh` and say whether the server still stops a bad push.
4. Run `.claude/hooks/test-guardrails.sh` again. It reads the expected decisions from the config, so it must still end with `0 failed`.

Done when the diff is that one config line (plus the deny rules in the exception), the test table passes, and the user got the warning.
