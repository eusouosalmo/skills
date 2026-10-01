# Skill maturity lives in frontmatter, not in folders

Each skill's maturity is `metadata.status` (`draft | beta | stable | deprecated`) and the folders under `skills/` split by domain only. Matt Pocock's repo, our main reference, uses folders such as `in-progress/` and `deprecated/`, but then promoting a skill changes its path, breaks links and muddles history. The Agent Skills spec allows free-form `metadata`, and `npx skills` already offers `metadata.internal: true` to hide drafts and deprecated skills from install (tested with `npx skills add ./ --list`).
