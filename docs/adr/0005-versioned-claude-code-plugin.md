# The repo is also a versioned Claude Code plugin, released by release-please

Besides `npx skills`, which installs from the latest commit on `main`, the repo is a Claude Code marketplace (`eusouosalmo`) with one plugin (`eusouosalmo-skills`) at its root. The plugin pins `version` in `.claude-plugin/plugin.json`, so users stay on a release until they update; without it every push would count as an update (Claude Code plugin loading reference, "Versions and updates").

The plugin loads every skill path listed in `plugin.json`, and `metadata.internal` means nothing to it. So the list holds only `beta` and `stable` skills, generated from `metadata.status` by `scripts/sync-plugin-skills.sh`; CI runs it with `--check` and fails when the list drifts, together with `claude plugin validate --strict` at a pinned Claude Code version.

Releases come from release-please rather than Changesets: it reads the Conventional Commits the repo already writes (`fix` patch, `feat` minor), needs no Node in the repo, and bumps `plugin.json` through `extra-files`. Versions start at `0.1.0` and stay in `0.x` (`bump-minor-pre-major`) until the first skill is `stable`. Plugins for Codex, Copilot or Gemini CLI are left out; `npx skills` already covers those agents. Decided in issue #13 of the distribution map (#12).
