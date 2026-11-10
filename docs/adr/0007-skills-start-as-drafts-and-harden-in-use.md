# Skills start as drafts and harden in use

`skill-forge` asked for an observed failure, three eval scenarios and a baseline run before a skill's first line. In practice the cost of that experiment blocked skills from being started, and the repo's own history shows where improvement came from: of 45 behaviour changes after creation, about 12 cite a real use and about 8 a reference gap, and none credits an eval for finding something new. The evals worked as a regression lock and as proof for promotion.

The research in `docs/research/skills-que-evoluem-com-uso.md` points the same way. Criteria for judging outputs only appear once outputs exist (Shankar et al., criteria drift). A draft refined from real failures beat a hand-curated skill in SkillEvolver, while skills written without running the task gave no gain in SkillsBench. Anthropic's best practices ask for evaluations before extensive documentation, and in the same page describe building a skill from a task done for real and refining it "based on usage"; `skill-creator` writes the draft before its tests. Three scenarios carry no statistical power, so they serve as a smoke test, not a measure.

So rigour now grows with `metadata.status` (see `docs/adr/0001`):

- **draft**: born from a seed case (one or two real runs of a task that repeats), with a side-by-side smoke run and a trigger check. No assertions yet.
- **in use**: each correction goes into `evals/corrections.md`; one that could come back becomes a scenario; edits are small deltas, consolidated when several are pending.
- **beta and stable**: promotion runs the full baseline over every scenario collected in use, with position-swapped model judging and the user's verdict on what decides.
- **pruning**: lessons are consolidated and lines no lesson explains are cut.

The gates stay: a one-off task gets no skill, a task that already works gets no skill, and a mechanical rule goes to a hook.

## Consequences

- A draft can ship without evals beyond the trigger queries, so `draft` keeps `metadata.internal: true`: nobody installs it by accident.
- `evals/corrections.md` ships with the skill (see `docs/adr/0004`), so its entries follow the same publishing rules as the rest of the repo.
- Promotion to beta now needs logged uses; the skills promoted in bulk on 2026-11-02 start their logs from now on.
- Corrections without a scenario are not re-checked automatically; the promotion's full run is where they are caught.
