# Sources

What backs each rule of the skill. **Observed**: seen in an eval run on the author's own raw clips. **Official**: stated by a primary source. Research notes are in `docs/research/orquestracao-de-skills.md`.

| Rule | Source | Strength |
|---|---|---|
| Ask for a missing script before the cut, and wait | Celular reel baseline (2026-10-18): run with no script, never asked for one; the hook came out as words on screen, where the author's script asked for the comment print over the face, and the facts on screen went unchecked | Observed |
| The cut's form is the chain's call, not a question | Both baselines (2026-10-18) asked the author "vídeo do corte ou arquivos soltos", a choice with no use when the cut feeds the next two steps | Observed |
| The output form asked once, for the whole chain | `reel-cut` and `reel-finish` each have their own output question; the author asked for the output form to be asked before the heavy work (#76, notes) | Observed |
| Stop at each gate; a request for the finished reel is not a delegation | Whatsapp baseline (2026-10-18): "tratei o teu pedido como delegação" and rendered with no plan or stills shown, though `reel-motion` renders only after approval "also when the request asks for the finished file" and the author's style notes allow delegation only when asked ("decide por mim"). Gates between steps of a chain: "Building effective agents" (Anthropic), prompt chaining with programmatic gates and checkpoints for human feedback | Observed; the pattern is official, the human checkpoint is a recommendation |
| With an mp4, ask at the stills gate for what the scenes leave to CapCut | Whatsapp baseline (2026-10-18): the impact screen shipped silent in the "ready to post" mp4, with "ficou contigo" in the handover | Observed |
| `edicao.md` with the step and the gate answers; re-invoke the current skill on resume | Claude Code skills docs: after compaction, each invoked skill is re-attached only up to its first 5,000 tokens (25,000 in all), and the fix is to invoke it again. Explicit state files for resuming a chain are community practice (superpowers' progress ledger), not an official rule | Official (compaction); anecdotal (state file) |
| Call the other skills by name; list them in `compatibility` | No spec field declares a dependency between skills and no installer resolves one (agentskills.io specification; vercel-labs/skills README); a skill folder is installed alone (repo ADR 0002) | Official |
