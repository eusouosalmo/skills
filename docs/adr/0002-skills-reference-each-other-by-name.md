# A skill calls another by name, never by path

Only the skill folder gets installed (Agent Skills spec; `npx skills` copies or symlinks one folder per skill). So a skill cannot read another skill's file, such as `../applying-voice/examples.md`: after install that path does not exist. When `writing-scripts` needs the voice, it tells the agent to use the `applying-voice` skill. This duplicates a little content but keeps every skill installable on its own.
