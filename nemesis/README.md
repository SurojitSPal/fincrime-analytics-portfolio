# NEMESIS — Adversarial Robustness Testing Suite

**Status: Unit 1 (Excel) delivered.** Units 2–6 scoped, awaiting build.

## What it is

A red-teaming suite that stress-tests [TYPHON](../typhon)'s detection logic against an adaptive adversary, across six stages:

| Unit | Stage | Status |
|---|---|---|
| A | Threshold evasion | Scoped |
| B | Behavioural mimicry | Scoped |
| C | Feature gaming | Scoped |
| D | Red-team / blue-team loop | Scoped |
| E | Adaptive adversary, multi-cycle retraining | Scoped |
| F | Regulatory-framed model validation pack | Scoped |

## Unit 1 — delivered

A four-tab Excel workbook:

- **README** tab — scope and how to read the workbook
- **Threshold Parameter Library (R01–R06)** — the rule parameters under test
- **Scenario Design Matrix** — the adversarial scenarios run against each rule
- **Results Cockpit** — formula-driven, recalculates live as parameters change

## Design principle: cost-of-evasion framing

The senior-practitioner differentiator for this project is framing every finding in terms of **cost of evasion** for an adversary — not just "detection degraded," but what it would cost a motivated actor to evade a given rule configuration. This is treated as a required analytical standard across all of NEMESIS, consistent with the portfolio-wide rule that gradient, probability-tiered language is used throughout ("detection degraded," never "the model failed").

## Honesty discipline

Over-labelling risk is actively guarded against: false positives in adversarial-testing results are surfaced honestly rather than smoothed over, including recalibrating earlier classifications when a later finding calls them into question.

## Repository layout (fills in as further units are built and defended)

```
nemesis/
├── README.md
├── docs/                     defence sheets per unit
└── unit-1-excel/             the four-tab workbook (synthetic parameters only — see docs/DATA-GOVERNANCE.md)
```
