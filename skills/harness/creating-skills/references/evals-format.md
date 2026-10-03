# Evals format

## evals/evals.json

One file per skill, inside the skill folder, in the agentskills.io format plus two fields: `setup` and `human_feedback`.

```json
{
  "skill_name": "exporting-invoices",
  "evals": [
    {
      "id": 1,
      "name": "export-month-to-csv",
      "prompt": "exporta as notas de setembro pra planilha que o contador pediu",
      "setup": "Run from a copy of evals/files/billing with the sample database loaded.",
      "files": ["evals/files/billing"],
      "expected_output": "A CSV with one row per September invoice, amounts in cents, in the column order the accountant template uses.",
      "assertions": [
        "The output is a CSV file with the template's header row",
        "Every September invoice in the sample database appears once",
        "Amounts are integers in cents"
      ],
      "human_feedback": ""
    }
  ]
}
```

- `prompt`: what a user would actually type, in their language, with real paths and context.
- `setup` (optional): how to prepare the environment before the run, when the files alone are not enough.
- `files` (optional): input files under `evals/files/`. Name a fixture skill's main file `SKILL.fixture.md`, so installers and link scripts do not pick it up as a real skill.
- `assertions`: objective statements checked with evidence from the output: format, size, language, file order, content rules. Write them after seeing the baseline run, and keep the ones that tell the two runs apart.
- `human_feedback`: the user's verdict on the latest run with the skill. An empty string means the output was good. Style lives here, never in an assertion.

## evals/trigger-queries.json

Only for model-invoked skills: 3 prompts that should trigger the skill and 3 near-misses that share its keywords but ask for something else.

```json
[
  { "query": "exporta as notas de setembro pro contador", "should_trigger": true },
  { "query": "importa o extrato do banco pro sistema de notas", "should_trigger": false }
]
```

A query passes when the agent loads the skill exactly when `should_trigger` is true. Run it on the model in use, from a project that has what the query refers to: a query about fixing an existing skill needs that skill in the project, or the agent spends the run looking for it and never loads this one.

## Workspace

Run outputs go to `<skill-name>-workspace/` next to the skill folder, outside version control (add it to `.gitignore`, or use the repo's scratch folder). Only `evals/` is committed.

```
<skill-name>-workspace/
  skill-snapshot/                 # when changing a skill: copy of the current version
  iteration-1/
    eval-<name>/
      without_skill/              # or old_skill/ when changing a skill
        outputs/
        report.md                 # the subagent's report
        grading.json
      with_skill/
        outputs/
        report.md
        grading.json
```

## One run

Each run is a fresh subagent (or a separate session when there are no subagents), so nothing from the authoring conversation leaks in. Give it:

- the project root to work in, prepared as `setup` says;
- for `with_skill` or `old_skill`, the skill folder path and the instruction to read its `SKILL.md` first; for `without_skill`, no skill;
- the prompt, verbatim;
- sandbox rules: stay inside the root, no commits, the user is away (write down the questions you would ask, then continue or stop where you would wait);
- the report to return: actions in order, files created in order, questions, final content of the files.

## grading.json

```json
{
  "assertion_results": [
    { "text": "Amounts are integers in cents", "passed": false, "evidence": "Row 3 has 1234.5" }
  ],
  "summary": { "passed": 2, "failed": 1, "total": 3 }
}
```

A PASS needs evidence quoted from the output or the report. An assertion with no evidence either way is a FAIL.
