# THEMIS — Transaction Monitoring Effectiveness & Threshold-Tuning Analytics
### Solution Blueprint v1.1 — Locked

*Named for the goddess of order, law, and sound counsel.*

*Changelog v1.0 → v1.1: added Module 6 (Interactive Tuning Console, Streamlit) and Module 7 (Periodic Reporting & Effectiveness Cockpit, Power BI/Tableau); Streamlit declared as an interaction layer in §4; honesty statement extended in §22; build phases extended to P9. Now 22 sections.*

Author: Surojit — AML/CFT, Fraud Risk Management Cell, Indian Overseas Bank
Portfolio track: European FinCrime analytics (ING, Rabobank, ABN AMRO, Deutsche Bank, Lloyds, Wise, Revolut; AMLA Frankfurt; Ireland)
Toolset: IIT Kanpur Professional Certificate (Data Analytics & Generative AI)

---

## 1. Executive Summary & Positioning

THEMIS is the **governance and optimization layer that sits over a transaction-monitoring rulebook**. Where detection projects ask *"did we catch it?"*, THEMIS asks two harder, supervisor-facing questions: *is the estate calibrated to the risk it faces (effectiveness),* and *does it do so without drowning operations in noise (efficiency)* — and it produces the evidence to answer both.

It measures coverage against a typology taxonomy, simulates the alert-volume-versus-detection tradeoff for every scenario, tests below the line, exposes where a single global threshold breaks across customer segments, drafts the regulator-facing calibration rationale, and — via an interactive console — lets a tuning analyst enter a candidate scenario and see its overlap and effectiveness live. It is the discipline the author already exercises on a live Clari5 rulebook, generalized into a reusable, defensible analytics toolkit.

**Why this piece, for this market:** most detection-heavy portfolios carry nothing on the effectiveness / model-risk side. AMLA and the EBA are pressing banks precisely here — *provable* calibration, not set-and-forget rules. THEMIS differentiates the portfolio and is the fastest to defend because it is demonstrably the author's own domain. The interactive console adds the operational-analyst dimension: not just analysis, but a tool the first line can use.

---

## 2. Problem Statement & Supervisory Context

Supervisors no longer accept a rulebook that merely "runs." They expect documented evidence that each scenario is risk-calibrated, tested above and below the line, differentiated by customer risk, and governed under a controlled model-change process. In practice, most monitoring estates carry three chronic defects:

- **Redundancy** — overlapping scenarios that fire on the same population, inflating cost without adding coverage.
- **Mono-thresholding** — a single global threshold per scenario that over-fires on low-risk cohorts and under-fires on high-risk ones.
- **Blind spots below the line** — no defensible estimate of what activity sitting just under threshold is being missed.

THEMIS produces the evidence pack that closes these gaps. This is the exact discipline behind the author's live Coverage-and-Gap Matrix work (25 case accounts mapped to a live rulebook, SCN 301–313 proposals) — abstracted away from any real institution's rulebook into a synthetic, shareable form.

---

## 3. Objectives & Scope

**In scope**
- Coverage & gap analysis of a synthetic rulebook against a typology taxonomy.
- Per-scenario threshold-sensitivity simulation and below-the-line (BTL) risk estimation.
- Segment-differentiated threshold analysis.
- A tiered effectiveness-metrics framework framed as cost-of-detection versus cost-of-miss.
- GenAI-drafted calibration rationale and model-change memo.
- An **interactive tuning console** (Streamlit) for live scenario entry, overlap testing, and effectiveness scoring.
- A **periodic reporting layer** (Power BI / Tableau) producing monthly / quarterly total-scenario-analysis packs and a standing effectiveness cockpit.

**Out of scope**
- Real-time alert triage and ML alert scoring — that is TYPHON's remit (see §5).
- Graph / network syndicate mapping — that is ARGUS's remit.
- Any production deployment. THEMIS is an **analytics toolkit with an analyst console, not a deployed platform** (honesty statement carried throughout; see §22).
- Any use of real customer or real rulebook data (see §7, §19, §22).

---

## 4. Toolset Declaration & Exclusions

**Build stack (IIT Kanpur course + one declared interaction layer):** Excel; PostgreSQL / SQL; Python (Pandas, NumPy, scikit-learn, NetworkX); Tableau; Power BI; GenAI integration; **Streamlit (interactive analyst console)**.

**On the Streamlit addition — stated honestly:** Streamlit is declared as an *interaction layer*, not a new analytical capability. It is a thin skin over the Python rule engine, which remains the single source of truth (see §16). It is included because it signals *"I built an analyst decision-support tool"* — which is exactly true — whereas the excluded frameworks below signal a production platform this project deliberately is not.

**Explicitly excluded and substituted:**

| Excluded | THEMIS substitution / reason |
|---|---|
| XGBoost / LightGBM | scikit-learn LogisticRegression / RandomForest |
| SHAP | scikit-learn native feature importance + `permutation_importance` |
| HDBSCAN | scikit-learn KMeans (segment clustering) |
| ARIMA / Prophet | rolling windows / EWMA on plain Pandas (used sparingly; THEMIS is not time-series-led) |
| Neo4j | NetworkX — **optional, scenario-overlap clustering only** |
| React, FastAPI, Docker, Azure, R | still excluded — they would signal a served production platform THEMIS is not; Streamlit fills the interaction need as a local analyst tool instead |

---

## 5. Portfolio Fit & Boundary Discipline

THEMIS sits inside a coherent synthetic AML "world" shared across the portfolio:

- **ARGUS** — detection / network (multi-hop mule tracing, syndicate emergence from NCRP data). *Graph.*
- **TYPHON** — alert triage + SAR drafting (rules + ML + GenAI). *Operations.*
- **NEMESIS** — adversarial robustness testing of TYPHON. *Assurance.*
- **THEMIS** — TM effectiveness & threshold tuning, with an interactive console. *Calibration / model governance.*

**Hard boundary with TYPHON:** THEMIS *tunes the rule layer* and outputs calibrated thresholds, coverage findings, and effectiveness evidence. TYPHON *triages alerts with ML*. THEMIS may reference an ML score as an input signal but its deliverable is calibration evidence, never a triage engine. The console tests *scenarios*, not *alerts*. Stating and holding this boundary is itself an interview asset.

---

## 6. Domain Decisions (Blessed — Locked)

These four calls are the author's own and are fixed for this build. An interviewer will probe them; they are answered here in the author's voice.

1. **Typology coverage.** Structuring; rapid movement / pass-through; mule inflow; dormant-account reactivation; threshold-hugging. Chosen because these five best exercise tuning logic across volume, velocity, and threshold-proximity behaviours.
2. **Segment definitions.** Retail; SME; high-risk occupation; new-to-bank. Chosen because these are the cohorts where a single global threshold visibly breaks.
3. **BTL sampling margin.** The **70–100% band** — activity at 0.7× to 1.0× of each scenario's threshold, i.e. within 30% below the line.
4. **Effectiveness thresholds.** Expressed as **tiers**, not a single cutoff, framed as cost-of-detection versus cost-of-miss (see §14).

**Division of labour (portfolio-integrity principle):** every consequential analytical call above is the author's; Claude executes all code.

---

## 7. Data Architecture

**Strategy (locked): extend the TYPHON generator, not the TYPHON file.** THEMIS gets its own purpose-shaped dataset, produced from the *same schema and generator architecture* already built for TYPHON. This gives a consistent synthetic-data lineage across the portfolio while avoiding concentration risk (three projects coupled to one file — a flaw in it would discredit all three at once) and while sizing the population for THEMIS's own statistical needs.

**Two synthetic inputs — no real data:**
- A **synthetic rulebook** of 10–15 scenarios with realistic condition logic, modeled on the *structure* of a real rulebook, never any institution's actual conditions.
- A **labelled synthetic transaction dataset**, scaled to **~500–1,000 accounts** across the four explicit segments, with typology injection **plus engineered threshold-band populations** so the sensitivity curves and BTL estimates are meaningful rather than decorative.

**Reusable defence line:** *"Same generator, purpose-shaped dataset — coherent portfolio, but each project stands on data fit for its own question."*

---

## 8. Synthetic Rulebook Specification

10–15 scenarios covering the five blessed typologies, each expressed as explicit, inspectable conditions (mirroring the *"live rulebook before tuning"* discipline — recommendations are grounded in the rulebook's actual stated conditions, never inferred). Illustrative set:

- **Structuring** — cumulative cash/transfers ≥ threshold T over N days, each below a reporting ceiling.
- **Rapid movement / pass-through** — credit followed by debit ≥ P% of credit within H hours.
- **Mule inflow** — many-to-one inbound fan-in above a count/value threshold within a window.
- **Dormant reactivation** — account inactive ≥ D days, then activity ≥ V within a short window.
- **Threshold-hugging** — repeated transactions clustered in the just-below-limit band.

Each scenario is stored with its parameters as tunable fields (see §10), so threshold sweeps and console entry operate on data, not code.

---

## 9. Synthetic Dataset Specification

- **Population:** ~500–1,000 accounts, distributed across retail / SME / high-risk-occupation / new-to-bank with realistic segment proportions.
- **Behavioural baselines per segment** — distinct volume/velocity profiles, so a global threshold demonstrably mis-fits some segments.
- **Typology injection** — labelled positive cases for each of the five typologies at controlled prevalence.
- **Engineered threshold-band populations** — deliberate density in the 70–100% band of each scenario so BTL sampling has signal.
- **Ground-truth labels** — present in the synthetic build to *validate the method*. Critical honesty point (see §19, §22): production has **no** ground truth, so production effectiveness figures become **probability-tier estimates**, not verified miss counts.

---

## 10. Data Model (PostgreSQL)

Core tables (illustrative):

- `accounts` — `account_id`, `segment`, `open_date`, `kyc_flags`, baseline behavioural attributes.
- `transactions` — `txn_id`, `account_id`, `counterparty_id`, `amount`, `direction`, `timestamp`, `channel`.
- `scenarios` — `scenario_id`, `typology`, condition parameters (threshold `T`, window `N`, ratio `P`, etc.) as columns so sweeps and console entry are data-driven.
- `alerts` — `alert_id`, `scenario_id`, `account_id`, `fired_at`, `threshold_value_at_fire`.
- `labels` — `account_id` / `txn_id`, `typology`, `is_true_positive` (synthetic ground truth only).
- `report_periods` — period key (month/quarter) support for the periodic reporting layer (see §17).

SQL executes the rulebook against `transactions`; parameter columns in `scenarios` are what the sensitivity engine and the console sweep.

---

## 11. Module 1 — Coverage & Gap Analysis

- Map every scenario to the typology taxonomy; surface **uncovered typologies** (gaps) and **redundant / overlapping scenarios** (SQL fire-overlap analysis — which scenarios fire on the same accounts).
- Optional NetworkX use: cluster scenarios by population overlap to visualize redundancy. This is the generalized, reusable form of the author's live Coverage-and-Gap Matrix.
- **Output:** a coverage-and-gap matrix (typology × scenario) with gap and redundancy findings. This overlap engine is reused live by the console (§16).

---

## 12. Module 2 — Threshold Sensitivity & BTL Testing

- For each scenario, **sweep the threshold** across a range and plot **alert volume against detection** — the tradeoff curve that exposes where tightening buys little and where loosening floods operations.
- **Above-the-line:** measure detection/false-positive behaviour at and above the current threshold.
- **Below-the-line (70–100% band):** sample activity at 0.7×–1.0× of threshold and estimate a **raised miss probability**. Language discipline is absolute here: *"raised miss probability"* and *"detection degraded"*, never *"confirmed misses"* or *"the model failed."*
- **Output:** per-scenario tradeoff curves; a BTL risk estimate per scenario with explicit probability-tier framing.

---

## 13. Module 3 — Segmentation Analytics

- scikit-learn **KMeans** clustering on account behavioural features, reconciled to the four blessed segments.
- Demonstrate how one global threshold **under-fires on one segment and over-fires on another**; produce **per-segment threshold recommendations**.
- Where any supervised scoring is used, explainability is via scikit-learn native feature importance and `permutation_importance` (no SHAP).
- **Output:** segment-differentiated threshold recommendations with the mis-fit evidence behind each.

---

## 14. Module 4 — Effectiveness Metrics (Tiered)

Metrics per scenario and per segment:

- **False-positive rate.**
- **Alert-to-SAR yield** (SAR-conversion proxy on synthetic labels).
- **Alert-to-yield / productivity** — alerts raised versus true positives surfaced.

**Tiered framing (blessed decision 4), cost-of-detection vs cost-of-miss:**

| Tier | Reading | Action |
|---|---|---|
| Green | Efficient and effective | Retain |
| Amber | Efficient but weak yield, or effective but noisy | Review / retune candidate |
| Red | Poor yield and high noise, or material BTL miss probability | Retune / redesign |

The tiering deliberately avoids a single cutoff so trade-offs are argued, not asserted. This scoring engine is reused live by the console (§16).

---

## 15. Module 5 — GenAI Calibration Rationale & Model-Change Memo

- GenAI layer auto-drafts the **calibration rationale** (why each threshold/segment recommendation was made) and a **regulator-facing model-change memo**, mirroring the author's board-note practice.
- **Honesty control:** GenAI *drafts*; the author *validates*. No recommendation reaches the memo without human sign-off. Prompts are logged so the drafting process is itself auditable.
- **Output:** a draft calibration-rationale pack and a model-change memo template populated from the analytics.

---

## 16. Module 6 — Interactive Tuning Console (Streamlit)

A single-user, local, interactive **decision-support tool** over the Python rule engine — the analyst-facing surface of THEMIS.

**Features**
- **Scenario entry.** A parameter-entry form (threshold, window, ratio, typology) writing to a staging copy of the `scenarios` parameters — never overwriting the locked baseline without an explicit save.
- **Live overlap test.** Runs the Module 1 fire-overlap engine for the candidate scenario against the existing estate; returns the overlapping account population, the % overlap, and which existing scenarios it duplicates.
- **Live effectiveness.** Runs the Module 4 scoring engine on the candidate; returns the tiered score (Green / Amber / Red), false-positive rate, and alert-to-yield.
- **Threshold slider.** Recomputes the Module 2 tradeoff curve and the BTL raised-miss-probability interactively as the analyst moves the threshold.

**Architecture — single source of truth.** Streamlit is a thin interaction skin. Every button calls the *same Python functions* the batch modules use; no rule logic is duplicated in the UI. The console reads and writes PostgreSQL directly.

**Guardrails.** All on-screen outputs enforce probability-tier language (*"raised miss probability"*, never *"confirmed miss"*). A persistent banner states: *analyst decision-support tool — not a production platform.*

**Honesty (see §22).** Single-user, local, session-based; no authentication, concurrency handling, or deployment hardening — by design.

---

## 17. Module 7 — Periodic Reporting & Effectiveness Cockpit (Power BI / Tableau)

The governance-facing surface of THEMIS: standing dashboards plus monthly / quarterly report packs on **total scenario analysis**.

**Standing effectiveness cockpit**
- Coverage-and-gap matrix; per-scenario tradeoff curves; BTL risk heat; segment mis-fit; the tiered effectiveness scorecard — the single view that answers *"is this estate calibrated?"*

**Periodic report pack (monthly / quarterly)**
- Total scenario analysis: alert volumes, false-positive trends, and **tier movements** (which scenarios shifted Green ↔ Amber ↔ Red period-over-period).
- Coverage changes, top redundancy and gap findings, and tuning recommendations actioned versus pending.
- Period parameter (month / quarter) drives the pack; exported as a PDF governance pack, reusing the author's board-note discipline.

**Data source.** The same PostgreSQL analytical tables the batch modules populate; Power BI / Tableau connect and refresh. Two audiences, two tools by design: the Streamlit console is the live analyst surface (§16); this layer is the periodic governance surface.

---

## 18. EU Regulatory Framing

Each module maps to a live supervisory driver, so the output *is* the evidence those regimes expect:

- **Coverage & gap** → EBA risk-based-approach expectations; AMLR ongoing-monitoring obligation.
- **Threshold sensitivity & BTL** → EBA TM guidelines; AMLA supervisory focus on TM *effectiveness*; the "below-the-line" testing supervisors increasingly expect.
- **Segmentation** → EBA ML/TF risk-factor guidelines (differentiated, risk-sensitive treatment).
- **Effectiveness metrics** → AMLA effectiveness expectations; model-risk discipline.
- **GenAI / model change** → EU AI Act model-risk documentation and robustness (where ML is used); controlled model-change governance.
- **Periodic reporting** → evidences the documented, recurring review cadence supervisors expect of a governed monitoring estate.
- **DORA** → operational resilience of the monitoring capability (referenced, not central).

---

## 19. Fact–Inference Boundary & Probability-Tier Language

Carried from ARGUS. Every output — batch or console — explicitly separates:

- **Verified** — a rule fired; a transaction had value X; an account sits in the 70–100% band. *Facts.*
- **Inferred** — that below-the-line activity represents laundering; that an account is a mule; that a threshold change would have "caught" a case. *Probability-tier estimates.*

Mandatory language: *raised miss probability*, *detection degraded*, *elevated risk cohort* — never *confirmed miss*, *model failed*, or *confirmed mule* from monitoring data alone. The console enforces this on-screen.

---

## 20. Build Phases

| Phase | Content | Deliverable | Suggested duration |
|---|---|---|---|
| P1 | Synthetic rulebook + derivative dataset (from TYPHON generator) + PostgreSQL load | Data foundation | ~1 week |
| P2 | SQL rule-execution engine → `alerts` | Working rulebook | ~1 week |
| P3 | Coverage & gap (Module 1) | Coverage-and-gap matrix | ~1 week |
| P4 | Threshold sensitivity + BTL (Module 2) | Tradeoff curves + BTL estimates | ~1.5 weeks |
| P5 | Segmentation (Module 3) | Segment threshold recommendations | ~1 week |
| P6 | Effectiveness metrics (Module 4) | Tiered scorecard | ~1 week |
| P7 | GenAI rationale + memo (Module 5) | Calibration pack | ~0.5 week |
| P8 | Interactive Tuning Console (Module 6, Streamlit) | Live analyst console | ~1.5 weeks |
| P9 | Periodic Reporting + Effectiveness Cockpit (Module 7) + final defence pack | Governance layer + defence pack | ~1.5 weeks |

**Calendar placement is the author's decision.** Live constraints to place around: ARGUS submission (December 2026); CAMS prep from October 2026; CV in market 1 March 2027. THEMIS reuses the existing generator, so it is deliberately lighter to stand up than ARGUS and can slot into gaps around those commitments. The console and reporting phases (P8–P9) are the newest work and carry the most defence-preparation weight.

---

## 21. Defence Sheets (Defence-Before-Advance Protocol)

Each phase ships with a one-page defence sheet, and reading-and-defending fluency on each phase is required before the next begins. Each sheet answers: what this phase proves in one sentence; the three questions an interviewer is most likely to ask, with answers; the one methodological weakness of this phase, stated plainly and bounded; and the probability-tier language required when presenting it.

**Console-specific defence questions (Phase 8), pre-answered:**
- *"Is this deployed?"* → No. It is a single-user, local analyst decision-support tool by design.
- *"How is it different from a platform?"* → No authentication, concurrency handling, or deployment hardening; in a bank it would feed the existing case-management and model-governance estate, not replace it.
- *"Does the UI duplicate your rule logic?"* → No. The console calls the same Python functions as the batch modules — a single source of truth, no logic fork.

Weekly defence drills apply, consistent with the portfolio protocol.

---

## 22. Risks, Limitations & Honesty Statement

- **THEMIS is an analytics toolkit with an analyst console, not a deployed platform.** Stated openly and repeatedly.
- **The interactive console is single-user, local, and session-based** — deliberately no authentication, concurrency handling, or deployment hardening, and it makes no claim to any. It is a decision-support tool; in production it would feed the existing case-management and model-governance estate, not replace it. Streamlit is an interaction skin over the Python engine, which remains the source of truth.
- **The rulebook is synthetic and structurally modeled** — it is not any institution's rulebook, and no real conditions or customer data are used, consistent with DPDP Act 2023 and IOB information-security policy. De-identified / synthetic data is analytically equivalent for every intended purpose here.
- **Synthetic labels validate the method, not the world.** In production there is no ground truth; effectiveness figures become probability-tier estimates. This limitation is a feature of the honesty framing, not a gap to hide.
- **Segmentation is a model, not a truth.** KMeans segments are decision aids; they carry their own misclassification risk, surfaced rather than suppressed.
- **GenAI drafts are unvalidated until the author signs off.** No memo content is authoritative without human review.

---

*End of Blueprint v1.1. Domain decisions §6 locked by the author; all code execution by Claude.*
