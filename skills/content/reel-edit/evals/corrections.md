# Corrections

## 2026-11-28: edicao.md written by the agent (#118)

- Prompt: any edit that stops at a gate and resumes later.
- What happened: the agent wrote `edicao.md` freely, in whatever shape it chose, so the next session had to guess where the edit stopped and whose word cleared each gate.
- What should have happened: the state file written only by a CLI verb, in a fixed header plus history format checked on read, with each stop recorded by `hold` and each answer by `approve` with the door and the author's words, so a fresh session resumes from `status` alone.
- Lesson (confirmed by the author in #118): a job that can stop records its stops through a CLI in a state file; the agent never writes that file by hand.
- Scenario: added as id 3.
