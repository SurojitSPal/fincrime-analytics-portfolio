# Portfolio Overview

## Purpose

This portfolio exists to demonstrate hands-on financial-crime analytics capability — not coursework completion — to support a transition from Indian banking fraud-risk operations into European AML/CFT, transaction-monitoring, and financial-crime analytics roles.

Target institutions span traditional banks, payment/fintech firms, and the emerging EU supervisory architecture (e.g. AMLA, Frankfurt).

## The person behind it

Built by an AML/CFT practitioner with hands-on experience in:
- NCRP (National Cybercrime Reporting Portal) complaint handling and I4C/CFCFRMS coordination
- Mule-account detection on a production transaction-monitoring platform (Clari5), across UPI and other rails
- Cyber-enabled fraud investigation and response
- Prior branch-banking and risk-based compliance audit experience (KYC, AML, PMLA)

That production exposure is treated throughout this portfolio as a **differentiation asset**: the typology knowledge, investigative instincts, and regulatory literacy are real and transferable — this portfolio is where they're translated into an analytics engineering body of work built against European frameworks.

## Naming convention

Projects follow a mythological naming convention (ARGUS, THEMIS, TYPHON, NEMESIS, and scoped-but-unbuilt names such as ARGOS, PNIDORA, CERBERUS, JANUS, HELIOS) — a deliberate, consistent identity across the portfolio rather than ad hoc project titles.

## Toolset discipline

One locked toolset is used across every project (see root README). Tools are added to the declared set only when there's a genuine, defensible reason — for example Streamlit was added explicitly for THEMIS's interactive tuning console, framed honestly as *"an analyst decision-support tool, not a deployed platform."* Production-signalling tools (Docker, Kubernetes-adjacent stacks, a full web framework) are deliberately excluded so the portfolio never overstates what was actually built.

## How work is built: the four-beat rhythm

Every project phase follows the same disciplined rhythm:

1. **Build** — the artifact (code, dataset, dashboard, document) is produced
2. **Run it yourself** — independently re-executed, not just reviewed
3. **Defence sheet** — a structured set of questions an expert interviewer would ask, answered in writing
4. **Confirm fluency** — able to explain and defend the artifact from memory, not from notes
5. **Advance** — only then does the next phase begin

Phase defence is **never skipped**, and is shared across sibling projects where they share a foundation (e.g. ARGUS and THEMIS share ingestion/ETL groundwork).

## Division of labour

- **Domain decisions** — typology selection, rule thresholds, feature justification, SAR narrative voice, dashboard audience design, ethical guardrails — are owned entirely by the practitioner.
- **Build execution** — code structure, implementation, build-strategy decisions once domain calls are made — is executed collaboratively with Claude, under the practitioner's direction and sign-off.
- **The test**: the portfolio must withstand expert scrutiny in interviews, meaning every domain call must be one the practitioner can defend as genuinely their own, independent of who typed the code.

## Dataset lineage

TYPHON's synthetic generator is the shared foundation: THEMIS extends it (a purpose-shaped derivative dataset, not a reused file) and NEMESIS red-teams the detection logic trained on it. This gives the portfolio one coherent synthetic "world" underneath triage, tuning, and adversarial testing — read as deliberate architecture rather than disconnected exercises — while avoiding the concentration risk of three projects standing on one identical file.

## Status discipline

A project phase is marked complete in this repository only once it has cleared the full four-beat rhythm above. Where a phase is still in blueprint or build, that is stated plainly — this portfolio's credibility depends on never overclaiming completion.
