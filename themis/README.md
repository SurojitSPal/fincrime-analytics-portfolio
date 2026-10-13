# THEMIS — Transaction Monitoring Threshold Effectiveness and Tuning

**Status: Solution Blueprint v1.1 locked (22 sections)** — build scheduled to begin after ARGUS submission, sharing ARGUS's ingestion/ETL foundation.

Full blueprint: [`docs/THEMIS_Solution_Blueprint_v1.1.md`](./docs/THEMIS_Solution_Blueprint_v1.1.md).

## What it is

An analytics toolkit for **tuning and evidencing the effectiveness of transaction-monitoring rule thresholds** — not a triage engine (that's [TYPHON](../typhon)'s job) and not a deployed platform. THEMIS tunes the rule layer and outputs calibrated thresholds and coverage evidence; it may reference an ML score, but its deliverable is calibration evidence, regulator-facing by design.

## Core question it answers

For a given rule threshold: what does it catch, what does it miss, and what would changing it cost — framed as alerts-to-yield and cost-of-miss, not a single pass/fail cutoff.

## Modules (per locked blueprint)

| Module | What it does |
|---|---|
| Rule execution engine | SQL-based, runs the synthetic rulebook against the dataset |
| Tuning / effectiveness scripts | Python — threshold trade-off curves, below-the-line (BTL) miss estimation |
| Coverage-and-gap matrix | Segment-based view of where a global threshold over- or under-fires |
| **Module 6 — Interactive Tuning Console** | Streamlit: type scenario parameters, get live overlap and effectiveness recompute against the rule engine — explicitly an analyst decision-support tool, not a production platform |
| **Module 7 — Periodic Reporting / Effectiveness Cockpit** | Tableau / Power BI: monthly/quarterly scenario-analysis reporting |
| GenAI layer | Drafts the calibration rationale and the regulator-facing model-change memo |

## Domain calls locked for this project

- **Typology coverage**: structuring, rapid movement/pass-through, mule inflow, dormant-reactivation, threshold-hugging
- **Segments**: retail / SME / high-risk-occupation / new-to-bank
- **BTL sampling margin**: within 30% below threshold (the 70–100% band)
- **Effectiveness thresholds**: tiered, not a single cutoff — framed as cost-of-detection vs. cost-of-miss

## Dataset strategy

THEMIS does **not** reuse the TYPHON dataset file. It extends the **same generator architecture** TYPHON was built on, scaled to ~500–1,000 accounts across the segments above, with typology injection plus engineered threshold-band density so sensitivity curves and BTL estimates are statistically meaningful rather than decorative. This gives the portfolio one coherent synthetic data lineage (TYPHON → THEMIS → NEMESIS) without concentration risk from three projects standing on one identical file.

## EU regulatory framing

EBA guidelines on AML/CFT policies and the compliance-officer role; EBA ML/TF risk-factor guidelines (risk-based calibration); AMLR ongoing-monitoring obligation; AMLA's supervisory direction on TM effectiveness and model governance; EU AI Act model-risk documentation where scoring touches ML. THEMIS's output is designed to *be* the evidence pack those regimes ask for.

## Repository layout (fills in as build phases clear defence)

```
themis/
├── README.md
├── docs/                 the locked 21-section blueprint, defence sheets
├── sql/                  rule execution engine
├── src/                  tuning/effectiveness scripts
├── streamlit_app/        Module 6 — interactive tuning console
└── data/                 derivative synthetic dataset + generator extension
```
