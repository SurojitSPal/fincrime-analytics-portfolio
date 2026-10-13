# NEMESIS — recovery status

Searched past chat sessions for the NEMESIS Unit 1 Excel workbook's actual formulas/structure and found the **design spec**, but not the workbook's cell-level content as recoverable text — like TYPHON's generator, it was built as a file inside a past session's temporary container, which no longer exists.

## What is confirmed from past sessions

A four-tab workbook was built and delivered:

- **README** tab — scope and how to read the workbook
- **Threshold Parameter Library (R01–R06)** — the rule parameters under test
- **Scenario Design Matrix** — the adversarial scenarios run against each rule
- **Results Cockpit** — formula-driven, recalculates live as parameters change

Built around the portfolio's **cost-of-evasion framing** — every finding expressed as what it would cost a motivated adversary to evade a given rule configuration, not just "detection degraded." Also recorded: a confirmation-bias correction episode where over-labelling was challenged mid-session, leading to permanent recalibration — the honesty discipline ("false positives surfaced honestly, not smoothed over") that NEMESIS is built to embody.

## What's not recoverable

The workbook's actual cell formulas, the six R01–R06 parameter definitions, and the specific scenarios in the Design Matrix. These lived only in the delivered `.xlsx` file from a past session, not as visible text in the conversation transcript.

## Next step

Unit 1 needs to be **rebuilt** to the same four-tab spec, with R01–R06 and the scenario matrix re-specified deliberately (the author's own domain calls, consistent with this portfolio's division of labour — see [`../../docs/PORTFOLIO-OVERVIEW.md`](../../docs/PORTFOLIO-OVERVIEW.md)) rather than guessed at. Units 2–6 (behavioural mimicry through the regulatory-framed validation pack) remain scoped but not built, per the original plan.
