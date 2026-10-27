# Agents

How to register the hook, run the proof session and finish the setup in each supported agent. Every agent here reads the Claude Code hook input (`tool_name`, `tool_input.command`) and blocks on exit 2. Formats checked against each agent's docs on 2026-10-02; confirm the page before changing a registration.

## Contents

- [Detection](#detection)
- [Claude Code](#claude-code) (also Cursor and Copilot CLI)
- [Codex](#codex)
- [Gemini CLI](#gemini-cli)
- [Unsupported agents](#unsupported-agents)
- [Adding an agent](#adding-an-agent)

## Detection

| Folder or file in the project | Agent |
| :- | :- |
| `.claude/`, `CLAUDE.md` | Claude Code |
| `.codex/`, `AGENTS.md` | Codex (`AGENTS.md` alone is shared by many agents: confirm) |
| `.gemini/`, `GEMINI.md` | Gemini CLI |
| `.cursor/` | Cursor: covered by the Claude Code registration |
| `.github/copilot-instructions.md`, `.github/hooks/` | Copilot CLI: covered by the Claude Code registration |
| `.clinerules/`, `.windsurf/`, `.devin/`, `opencode.json`, `.amp/`, `.kiro/` | Unsupported in v1 |

## Claude Code

Docs: https://code.claude.com/docs/en/hooks, https://code.claude.com/docs/en/permissions

Merge into `.claude/settings.json`, keeping every existing key:

```json
{
  "permissions": {
    "deny": [
      "Bash(git reset --hard*)",
      "Bash(git clean -f*)",
      "Bash(git checkout -- *)",
      "Bash(git restore .*)",
      "Bash(git branch -D *)",
      "Bash(git stash drop*)",
      "Bash(git stash clear*)",
      "Bash(git push --force*)",
      "Bash(git push -f*)",
      "Bash(git update-ref *)",
      "Bash(rm -rf .git*)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/git-guardrails.sh --agent claude --profile interactive"
          }
        ]
      }
    ]
  }
}
```

The deny rules are the native layer: they catch the usual spelling even if the hook fails open. They cover only `destructive` and `history-rewrite`; when the user sets one of those categories to `ask` or `allow`, remove its deny rules too, or they keep blocking.

Cursor and Copilot CLI read this same file, so they need no registration of their own. Do not also register the hook in `.cursor/hooks.json` or `.github/hooks/`: it would run twice.

- **AFK profile:** `.claude/git-guardrails-afk.json` holds only the `hooks` block above with `--profile afk`, plus the same deny rules. The loop passes it with `--setting-sources "" --settings`, never with `--bare`: bare mode skips hooks from `--settings` too (Claude Code 2.1.288). The deny rules are the only layer left if someone runs the loop with `--bare` anyway.
- **Proof session:** see SKILL.md step 6. `claude -p` in a throwaway copy, with `--allowedTools "Bash"` so that only the hook can stop the command.
- **Human step:** none for the hook. In `-p` the project's `permissions.allow` rules are ignored until the folder is trusted interactively once; deny rules and hooks apply anyway.

## Codex

Docs: https://learn.chatgpt.com/docs/hooks

Codex has no variable with the project path and may start in a subfolder, so the command finds the repo root with git. Create or merge `.codex/hooks.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "^Bash$",
        "hooks": [
          {
            "type": "command",
            "command": "\"$(git rev-parse --show-toplevel)/.claude/hooks/git-guardrails.sh\" --agent codex --profile interactive",
            "statusMessage": "Checking git command",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

- **No ask:** Codex does not support `permissionDecision: "ask"`. With `--agent codex` every `ask` becomes a block that tells the agent to ask the user.
- **No native deny:** Codex rules (`.codex/rules/*.rules`) are experimental; v1 does not use them.
- **Human step (required):** project hooks load only when the project's `.codex/` layer is trusted, and each hook is trusted by hash. The user opens Codex in the project, runs `/hooks` and trusts the git-guardrails hook. Any edit to `.codex/hooks.json` needs the review again. Until then the guardrail is off and nothing warns.
- **Proof session:** after the human step, in the project itself, ask Codex to run the harmless canary `git -C /nonexistent-git-guardrails-canary reset --hard` and check that the answer quotes `git-guardrails: blocked`. A throwaway copy would be an untrusted project and prove nothing.
- **AFK:** not covered in v1. Tell the user that only the server protects an unattended Codex run.

## Gemini CLI

Docs: https://geminicli.com/docs/hooks/, https://geminicli.com/docs/hooks/reference/

Merge into `.gemini/settings.json`. Timeouts are in milliseconds:

```json
{
  "hooks": {
    "BeforeTool": [
      {
        "matcher": "run_shell_command",
        "hooks": [
          {
            "name": "git-guardrails",
            "type": "command",
            "command": "\"$GEMINI_PROJECT_DIR\"/.claude/hooks/git-guardrails.sh --agent gemini --profile interactive",
            "timeout": 30000
          }
        ]
      }
    ]
  }
}
```

- **No ask:** Gemini decisions are `allow` and `deny` only; `--agent gemini` turns `ask` into a block.
- **No native deny:** workspace policies (`.gemini/policies/`) are disabled; only the hook protects.
- **Human step (required):** Gemini fingerprints project hooks and warns before running a new or changed one. The user opens Gemini in the project and accepts the git-guardrails hook.
- **Proof session:** after the human step, same canary as Codex, in the project.
- **AFK:** not covered in v1.

## Unsupported agents

Cline, Windsurf (Devin Desktop), OpenCode, Amp, Kiro and the rest are not covered in v1: their hook input or block signal differs. Tell the user plainly that, for those agents, only branch protection on the server stops a bad push, and nothing stops local destructive commands.

## Adding an agent

Add a section here with: where its project hook config lives, the shell tool name (add it to the `case` on `TOOL_NAME` in `git-guardrails.sh` if new), how it reads the hook's stdin and exit code, whether it supports ask, the human step that turns the hook on, and the proof session. Then add a row to the test table in `test-guardrails.sh` with the new input shape.
