# Reels

The reel skills work inside a reel folder and read the author's style file, `estilo.md`, at the root of the reels folder, one level above every reel. So the paths go into that file, and the file has to be there.

## Keys

| Key | What it is (ask in these words) | Evidence |
|---|---|---|
| `reels` | the folder holding one subfolder per reel | subfolders with `brutos/`, `timeline.md`, `legenda.srt` or `exports/` |
| `scripts` | where the author keeps video scripts | Markdown files with a `## Teleprompter` or `# Roteiro:` heading, often in a notes vault |
| `style_file` | the current `estilo.md`, the author's editing taste | a file named `estilo.md`; a `timeline.md` line "Estilo:" pointing to it |
| `design_system` | the colours, fonts and components scenes are drawn with | a folder with `tokens.css` or a `project/` export; a `timeline.md` line "Design system:" |
| `capcut_drafts` | CapCut desktop's projects folder | `<user>/AppData/Local/CapCut/User Data/Projects/com.lveditor.draft/`, under `/mnt/<drive>/Users/` in WSL |
| `capcut_reference_project` | the author's project whose editing style the finished reel copies | a project the style file or a `timeline.md` names as "Referência" or "molde" |

## Put the style file at the root of the reels folder

- **It lives elsewhere:** move it to `<reels>/estilo.md` and leave a symbolic link at the old place, so whatever pointed there (a script, an eval) still finds it. Say both paths.
- **There is none:** create `<reels>/estilo.md` with a title and the Paths block only; the skills fill in the author's taste from their verdicts.
- **It is already there:** leave it.

## The block

Right after the style file's title:

```markdown
## Paths

Written by setup-eusouosalmo-skills on <date>. Run it again after moving a folder or on a new machine.

- reels: <path>
- scripts: <path or "none">
- design_system: <path or "none">
- capcut_drafts: <path or "none">
- capcut_reference_project: <project name or "none">
```

A block written by the skill's earlier name, `setting-up-reel-skills`, is the same block: replace it.
