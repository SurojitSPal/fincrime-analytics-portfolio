# ARGUS — Advanced Risk & Graph Unified System

**Status: in build** (target submission late Nov / early Dec 2026)

## What it is

A cyber-fraud network intelligence application. ARGUS ingests cybercrime-complaint data hop by hop, reconstructs multi-layer mule networks by stitching complaints together on shared accounts, identifies mule hubs and probable syndicates, validates findings statistically, and presents the intelligence through dashboards, a natural-language query box, and generated reports.

Built against a **persistent PostgreSQL store** (not in-memory) that accepts repeatable batch ingestion and accumulates intelligence across everything it has seen — a dynamic application, not a one-off analysis script.

## Architecture (as scoped)

- **Ingestion** — repeatable, appending batch ingestion from day one; the analyst provides data batches, ARGUS does not pull live from any portal
- **Store** — PostgreSQL, persistent and accumulating
- **Analysis layer** — Python (Pandas, NumPy, NetworkX) for network reconstruction, hub/syndicate identification, and statistical validation (including Benford's Law)
- **Interaction layer** — Streamlit app with dashboards, an ingestion screen, a Level-1 natural-language query box, and a what-if threshold slider
- **Reporting** — generated reports, district-level map view (district names only — see [data governance](../docs/DATA-GOVERNANCE.md))

## Governance features built in

Hash-chained audit log · maker-checker fields · data-quality / confidence-completeness score · run manifest · periodic reporting — four of these were adapted directly from a real internal EFRM tender's requirements, incorporated here as portfolio-appropriate analytics features (production integrations are named only as roadmap, never claimed as built).

## What's deliberately out of scope

Predictive future-hotspot forecasting and a standalone false-positive register were considered and explicitly cut to keep the build honest and within the course toolset.

## Dataset

Developed and defended against real NCRP complaint data (11,165 transaction rows, 4,016 complaints) kept strictly local. **Nothing in this repository is or derives directly from that real data** — see [`docs/DATA-GOVERNANCE.md`](../docs/DATA-GOVERNANCE.md). A synthetic generator stands in for the public build.

## Repository layout (filling in as phases clear defence)

```
argus/
├── README.md          this file
├── docs/               blueprint, defence sheets, phase notes
├── sql/                schema + rules layer
├── src/                ingestion, graph analytics, scoring
├── streamlit_app/       interaction layer
└── data/                synthetic data + generator (never real data — see .gitignore)
```

## Sibling project

[THEMIS](../themis) shares ARGUS's ingestion/ETL foundation and ingests the same engine, diverging into transaction-monitoring threshold effectiveness rather than network reconstruction.
