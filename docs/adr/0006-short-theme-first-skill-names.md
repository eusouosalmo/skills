# Skill names are short noun phrases, theme first

The skills were named in gerund form (`writing-short-video-scripts`, `cutting-raw-takes`), the form Anthropic's best practices prefer. In use, the names were long and hard to recall when typing a slash command, and the five reel skills, steps of one pipeline, were scattered through the list.

The same best practices accept noun phrases (`pdf-processing`) and ask above all to avoid inconsistent patterns within a collection ("Naming conventions", https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices). So every skill moved at once to a short noun phrase with the theme first: `reel-script`, `reel-cut`, `reel-motion`, `reel-finish`, `reel-edit`, `post-caption`, `eusouosalmo-voice`, `skill-forge`, `git-guardrails`. Typing `/reel` lists the whole pipeline. The setup skill keeps `setup-eusouosalmo-skills`, the form users know from other kits' setup skills.

## Consequences

- Renaming released skills breaks whoever installed them: the plugin's skill names change, and `npx skills` leaves the old folder in place. The rename went out as a breaking change, with the old names in the changelog.
- The description still carries the triggers; the name only has to be recognisable and typeable.
