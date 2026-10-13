# FinCrime Analytics Portfolio

A portfolio of financial-crime analytics projects built on real-world AML/CFT and fraud-investigation experience, targeting transaction-monitoring and financial-crime analytics roles in European markets.

**Author:** Surojit S Pal — CAMS, NISM Series XXIV, CAIIB, ECBA (IIBA), IFSCA Certified Business Analyst. ~13 years in banking, including hands-on work in fraud risk management covering mule-account detection, cyber-enabled fraud response, and transaction-monitoring investigation under India's AML/CFT and PMLA framework.

> **Status note:** this portfolio is under active, disciplined build — see each project's own README for its honest current status. Nothing here is represented as production-deployed or regulator-certified; everything is framed, as stated throughout, as **investigative leads and analyst tooling, never criminal verdicts or production systems.**

---

## Why this portfolio exists

Built as the hands-on capstone work for the IIT Kanpur Professional Certificate in Data Analytics and Generative AI, and extended into a standing body of work supporting a transition into European financial-crime roles (transaction monitoring, fraud analytics, financial-crime data science) at institutions such as banks, payment firms, and fintechs operating under EU AMLR, DORA, and the EU AI Act.

Indian banking fraud-ops experience — NCRP/I4C complaint handling, mule-network detection on production transaction-monitoring platforms, cyber-fraud response — is treated here as a differentiating asset, not a gap: the typologies, investigative discipline, and regulatory literacy transfer directly to the European AML/CFT context.

## Portfolio structure

Each project follows a mythological naming convention and is built end-to-end — problem framing, data, method, EU regulatory alignment, and deliverables — using one locked toolset, so the portfolio reads as one coherent body of work rather than disconnected exercises.

| Project | Focus | Status |
|---|---|---|
| [`argus/`](./argus) | Cyber-fraud network intelligence — mule-network reconstruction from complaint data, graph analytics, syndicate detection | In build |
| [`themis/`](./themis) | Transaction-monitoring threshold effectiveness and tuning — calibration evidence, coverage/gap analysis, interactive tuning console | Blueprint locked |
| [`typhon/`](./typhon) | Hybrid rules + ML + GenAI alert triage and SAR-drafting framework | Scoped, dataset generated |
| [`nemesis/`](./nemesis) | Adversarial robustness red-teaming of TYPHON's detection logic | Unit 1 delivered |

See [`docs/PORTFOLIO-OVERVIEW.md`](./docs/PORTFOLIO-OVERVIEW.md) for the full narrative, toolset rationale, and the division of labour behind how this portfolio is built.

## Locked toolset

Excel · PostgreSQL / SQL (T-SQL where project-specific) · Python (Pandas, NumPy, scikit-learn, NetworkX) · Tableau · Power BI · Streamlit (declared interaction layer) · GenAI integration

Deliberately **excluded**: Neo4j, FastAPI, React, Docker, XGBoost, LightGBM, SHAP, HDBSCAN, ARIMA/Prophet, R, Azure — kept out to stay honestly scoped to what is built and defensible, not to signal a production platform this isn't.

Reference frameworks drawn on throughout: FATF, Europol, FinCEN, EBA, Chainalysis, Elliptic, TRM Labs typology taxonomies; EU AMLR, DORA, EU AI Act, AMLA supervisory architecture.

## Data governance — read before touching any project folder

**No real customer, complaint, or transaction data is ever committed to this repository.** Every dataset in this portfolio is synthetic or fully de-identified. See [`docs/DATA-GOVERNANCE.md`](./docs/DATA-GOVERNANCE.md) for the full policy and the `.gitignore` guard that enforces it.

## Analytical language standards

Throughout this portfolio: confirmed fact, observed pattern, statistical association, and model inference are kept strictly separate. Outputs are framed as probability-tiered investigative leads, not verdicts. Honesty about limitations — including false positives and incomplete coverage — is treated as a deliverable in its own right, not a weakness to hide.

---

*This repository is updated as each project phase is built and defended. A phase is only marked complete here once it has been built, independently re-run, and defended against its own defence sheet.*
