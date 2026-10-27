# Sources

What backs each rule of the skill. **Observed**: seen in an eval run in a miniature of the author's machine. **Official**: stated by a primary source. Research notes are in `docs/research/skills-de-setup.md`.

| Rule | Source | Strength |
|---|---|---|
| Write the paths into a Paths block of the style file, never into `~/.claude/CLAUDE.md` | Both baselines (2026-10-19) found the paths and then tried to write them into the global `~/.claude/CLAUDE.md`, which the sandbox blocked, so nothing was set up; a global file would load in every session of every project. eusouosalmo chose the style file (#11, 2026-10-19) | Observed; preference for the place |
| The style file at the root of the reels folder, with a link left at its old place | The reel skills look for `estilo.md` one level above the reel folder (`reel-motion`, "Files"); the author's lived in the repo's scratch folder, where they could not find it. eusouosalmo (2026-10-19): "na raiz da pasta dos reels" | Observed |
| Keys in English, values as paths | The repo's language rule: structure in English, content in pt-BR (ADR 0003); eusouosalmo (2026-10-19) | Preference |
| A file the user writes, not the plugin's `userConfig` | The plugin manifest's `userConfig` holds paths for the plugin's own skills only, and `npx skills` has no equivalent, so it misses the draft skills and the other install channel (Claude Code plugins reference) | Official |
| Explore first, one question per key with the recommended answer, show the block before writing, replace only the block on a second run | mattpocock/skills, `setup-matt-pocock-skills` | Anecdotal (one community repo) |
| Optional, every key may be `none`; a path given in the request is not asked | A message from the author relayed from another session (2026-10-19): the video skills serve first-time creators and technical ones, so the setup must work through the conversation with defaults and let a technical user pass files directly. The layperson baseline wrote a how-to file and tried the global `CLAUDE.md` instead | Preference, observed |
| Never write into a skill folder | `npx skills update` rewrites the installed folder, and here `scripts/link-skills.sh` links it to this public repository | Official (vercel-labs/skills README); observed |
