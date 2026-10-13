# TYPHON — recovery status

Searched past chat sessions for the TYPHON synthetic dataset generator script and found the **design spec**, but not the generator's actual source code as recoverable text — it was written and run as a file inside a past session's temporary container, which no longer exists. Chat history preserves conversation text, not files that were only ever written to disk in an earlier, now-closed session.

## What is confirmed from past sessions

- A **5,000-row labelled synthetic AML dataset** was generated, covering **98 accounts**, loaded into a **PostgreSQL schema**, with a **reproducible generator** (i.e. built to be re-run, not a one-off script)
- Typology injection was built into the generator (labelled positive cases per typology, at controlled prevalence — the same pattern later extended for THEMIS, see [`../../themis/docs/THEMIS_Solution_Blueprint_v1.1.md`](../../themis/docs/THEMIS_Solution_Blueprint_v1.1.md) §7–9)
- The generator is the **shared foundation** for the portfolio's synthetic data lineage: THEMIS extends it into a larger, purpose-shaped derivative dataset (~500–1,000 accounts), and NEMESIS red-teams the detection logic trained on it

## What's not recoverable

The generator's actual Python source and the 5,000-row dataset file itself. Both were artifacts of a past session's working directory, not stored in the conversation transcript as visible code.

## Next step

The generator needs to be **rebuilt** — to the same documented spec (98 accounts, 5,000 rows, PostgreSQL schema, typology injection) rather than reconstructed from memory, so the resulting code is verifiably correct rather than a guess at what the original did. This is real build work, not a recovery task, and belongs in this project's own four-beat rhythm (build → run → defence sheet → confirm fluency) once TYPHON's build phase starts.
