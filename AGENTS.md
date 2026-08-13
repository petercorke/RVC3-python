# RVC3-python — Agent Instructions

Part of the RVC ecosystem. **Read [rvc-ecosystem/AGENTS.md](https://github.com/petercorke/rvc-ecosystem/blob/main/AGENTS.md) first** — it defines shared conventions: repo ownership, math invariants, dependency boundaries, git/PR workflow, code standards, tech-debt tracking. This file only adds what's specific to this repo.

| | |
|---|---|
| PyPI package | `rvc3python` |
| Nickname | RVC3-python |
| Owner | Peter Corke (`petercorke`) |
| Default branch | `main` |
| Contribution model | Branch → PR; direct push to `main` at Peter's discretion |

## Notes specific to this repo

- Companion code for *Robotics, Vision & Control*, 3rd ed. — worked examples tied to the
  book's chapters, not a general-purpose library. Changes here should track the book's
  content, not add unrelated functionality.
- The ultimate regression test: every example in the book must run against the *shipped*
  (released) versions of RTB, MVTB, and bdsim — not their dev/main branches. Any behavioural
  variation from what the book shows requires a book errata entry, not just a silent code fix
  here.
- Colab and JupyterLite support matter more here than in the other repos — notebooks should
  use `%pip` magic (not `!pip`) and have output cleared at commit time.
