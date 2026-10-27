# Sources

This skill describes its method in its own words. No text is copied from the sources below. The research behind it is in the repo's `docs/research/guardrails-e-modo-afk.md`.

- **git-guardrails-claude-code** (Matt Pocock, MIT): https://github.com/mattpocock/skills/tree/main/skills/misc/git-guardrails-claude-code. The idea of a PreToolUse hook that blocks risky git with exit 2 and tells the agent not to insist. `git-guardrails.sh` is a rewrite that parses the command instead of matching regexes; the bypasses that the original lets through are rows of `test-guardrails.sh`.
- **Claude Code docs**: https://code.claude.com/docs/en/hooks (input, exit 2, `ask`, `disableAllHooks`), https://code.claude.com/docs/en/permissions (deny rules and what a Bash rule does not match), https://code.claude.com/docs/en/headless and https://code.claude.com/docs/en/cli-reference (`-p`, `--bare`, `--settings`, `--setting-sources`).
- **Codex hooks**: https://learn.chatgpt.com/docs/hooks. `.codex/hooks.json`, no project-dir variable, no `ask`, trust per hash in `/hooks`.
- **Gemini CLI hooks**: https://geminicli.com/docs/hooks/ and https://geminicli.com/docs/hooks/reference/. `BeforeTool`, `run_shell_command`, `GEMINI_PROJECT_DIR`, decisions `allow` and `deny` only.
- **GitHub rulesets and branch protection**: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets. What `check-server.sh` reads.
- **destructive_command_guard** and **CC Safety Net**: https://github.com/Dicklesworthstone/destructive_command_guard, https://github.com/kenryu42/cc-safety-net. Ideas only: parse and normalise before deciding, look inside `sh -c`, fail closed, one core with thin adapters per agent.

Checked by running, not found in the docs (Claude Code 2.1.288): `--bare` skips hooks passed with `--settings` too, while `--setting-sources "" --settings <file>` runs the file's hooks and skips the project's.
