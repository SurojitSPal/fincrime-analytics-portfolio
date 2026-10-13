# ARGUS — Advanced Risk & Graph Unified System

## Project overview, defence pack, and architecture notes

*Compiled from the locked Solution Blueprint, the Round 1 Foundational Defence Sheet, and the ARGUS Study Guide produced across the project's planning sessions. This document consolidates the real decisions, rationale, and defence answers already locked for ARGUS — the full 21-section Solution Blueprint and Study Guide exist as separate Word/PDF documents produced earlier in the project and are being re-created as the build proceeds.*

Author: Surojit S Pal — AML/CFT, Fraud Risk Management Cell, Indian Overseas Bank

---

## 1. What ARGUS is

**The 60-second opening** (the one to have ready cold for any interview):

> "ARGUS reconstructs cyber-fraud mule networks from NCRP complaint data. Each complaint shows only one victim's money trail, but the same mule accounts recur across many complaints — so by stitching thousands of complaints together on their shared accounts, ARGUS reveals the mule hubs, the syndicates, and the geographic hotspots that no single complaint shows. On my real dataset of 4,000 complaints, one account turned out to sit behind 113 separate victims. It scores accounts as investigative leads — never verdicts — validates its findings statistically, and presents them through dashboards, a query box, and generated intelligence reports."

**Core problem solved, in one sentence:** cyber-fraud proceeds fragment across many accounts and banks within hours, and each victim complaint captures only one thread of the trail; ARGUS aggregates thousands of complaints into a network view that surfaces the shared mule hubs, syndicates, and hotspots that no single complaint reveals.

**The central insight the design rests on:** the same mule account appears across many unrelated victim complaints. That shared node is the linkage key — it stitches isolated victim threads into a network and lights up the syndicate. An account touching thirty unrelated complaints isn't thirty coincidences; it's a hub.

## 2. Why the name

ARGUS is a backronym — **A**dvanced **R**isk & **G**raph **U**nified **S**ystem — naming what the system does on every axis: advanced analytics, financial-crime risk, graph-based network analysis, unifying multiple datasets into one end-to-end system. It's also the hundred-eyed watchman of Greek myth who never fully sleeps — the right metaphor, since the whole point is to see the network that individual complaints hide. It follows the mythological naming convention used across the portfolio (THEMIS, TYPHON, NEMESIS).

## 3. Real dataset — development basis (kept strictly local)

ARGUS was designed and validated against a real NCRP complaint dataset:

- **11,165** transaction rows across **4,016** complaints
- **317** accounts appearing as both sender and receiver
- **151** shared mule hubs identified
- **Flagship finding:** one account linked to **113 distinct complaints**

This real dataset informed the design (schema shape, realistic typology distribution, the fan-in linkage mechanism) but — per the portfolio's data governance policy (see [`../../docs/DATA-GOVERNANCE.md`](../../docs/DATA-GOVERNANCE.md)) — never leaves the local machine and is never committed here. The public build runs on a synthetic generator that reproduces the same statistical shape.

## 4. Persistent, accumulating architecture

ARGUS is a **dynamic application backed by PostgreSQL**, not a one-shot analysis script:

- **Persistent** — on disk, survives sessions, explicitly not in-memory
- **Accumulating** — batches append, never replace
- **Safe to re-ingest** — deduplicates and validates per batch
- **Recompute-on-ingest** — the full network intelligence recomputes across everything ARGUS has seen after each load, so an old mule hub can resurface linking new complaints to an existing syndicate

**The honest boundary:** ARGUS ingests what the analyst supplies — it does not pull live from NCRP (that requires an authority the author doesn't hold as a portfolio builder). Every row is traceable to its batch via `batch_id` and load-timestamp columns.

## 5. Toolset and substitutions

Locked toolset: Excel, SQL/PostgreSQL, Python (Pandas, NumPy, scikit-learn, NetworkX), Tableau, Power BI, GenAI, Streamlit.

| Excluded (signals a production platform ARGUS isn't) | Substitution and reason |
|---|---|
| Neo4j / Cypher | Python NetworkX — right-sized for the data; identical centrality/community metrics with no infrastructure overhead; Neo4j documented as the production migration path at million-node scale |
| FastAPI / React / Docker | Streamlit — single-user, local, interactive; no claim to a served platform |
| XGBoost / LightGBM | scikit-learn logistic regression / random forest |
| SHAP | Transparent coefficient / feature-weight explanation |
| ARIMA / SARIMA / Prophet | Moving averages and time-series decomposition |
| HDBSCAN | K-Means / DBSCAN foundations |
| R, Azure | Not used — stays inside the course-certified toolset |

## 6. Dashboard visual target

Dark navy theme, KPI strip on top with bright accent numbers, balanced grid below — ARGUS-appropriate chart choices (ranked hub bars, network graph, district map) replacing generic donut charts.

## 7. Committed enhancements (locked)

Benford's Law · network-growth-over-time · what-if threshold slider · district-level map (district names only — no finer geography, per data governance) · natural-language query box (Level 1 query-library) · data quality score · maker-checker fields · hash-chained audit log · confidence/completeness flag · run manifest.

Four enhancements were adapted directly from IOB's own EFRM tender requirements (RFP-derived): maker-checker, hash-chained audit log, data quality score, periodic reporting.

**Explicitly cut** (over-ambition deliberately stripped back): predictive future-hotspot forecasting, a standalone false-positive register.

## 8. Demonstration order (for interviews)

Tell it in the order that tells a story, not the order it was built:

1. Command-centre dashboard — the headline numbers
2. Drill into the network graph — let the 113-complaint hub speak for itself
3. A traced fund-flow from victim to exit
4. The hotspot map
5. Type a question into the natural-language query box and let it answer live
6. Generate a report

The arc: *here is the scale, here is the hub, here is how money moved, here is where, ask it anything, here is the fileable output.*

## 9. Defence Q&A (pre-answered)

| They will ask | The answer |
|---|---|
| Did you build this yourself? | "I designed it and made every analytical decision; I used AI for implementation, as your team does — and I can defend every part." |
| Why should a score not be a verdict? | A statement-level pattern is evidence, not proof; without KYC and counterparty resolution the honest output is a lead. |
| How do you know the GenAI isn't inventing facts? | It can't — it only reports what a real database query returns; the model picks the query, never the answer. |
| Why synthetic / de-identified data? | Legal and ethical necessity, and it lets the method be validated against known ground truth. |
| What doesn't it do? | Real-time detection, device/KYC linkage, live feeds — all documented as the production roadmap, deliberately not claimed. |
| Why NetworkX not Neo4j? | Right-sized for the data; identical metrics with no infrastructure overhead; Neo4j documented as the production migration path. |
| Why PostgreSQL not SQL Server? | PostgreSQL is free, matches the course toolset, and the persistent/accumulating design doesn't depend on the specific RDBMS — the T-SQL migration is a documented, low-cost path if a target employer's stack calls for it. |

## 10. The honesty thread

Every strong defence answer traces back to one habit: refusing to overclaim. The synthetic-data framing, the lead-not-verdict language, the documented boundaries, the verified (never-inventing) GenAI layer — all of it is the same discipline. It is also, not coincidentally, exactly the discipline a financial-crime employer is screening for. The thing that makes ARGUS defensible is the same thing that makes its author employable in this field.

## 11. Build rhythm

Four-beat rhythm per phase: **build → run yourself → defence sheet → confirm fluency → advance.** Running the code and seeing it break (and fixing it) is where real fluency forms — watching is not understanding. One chat/session per phase with a handoff note between sessions, to manage context and keep each phase genuinely defended before the next begins.

## 12. What to reread before any interview

Section 1 (what it is), Section 10 (the honesty thread), and Section 9 (the Q&A table). If the 60-second opening can be delivered cleanly and the Q&A answered without hesitation, ARGUS is ready to defend to anyone.

---

*Companion documents referenced in this project's history: the full ARGUS Solution Blueprint (21 sections — architecture, data model, persistent-ingestion design, statistical methods, toolset, roadmap), the Round 1 Foundational Defence Sheet (12 Q&A across foundation / design-choices / hard-questions), and the ARGUS Study Guide (8 parts). These were produced as Word/PDF documents in earlier planning sessions; this markdown file consolidates their substance for the public repo and will be extended as each build phase is completed and defended.*
