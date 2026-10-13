# Data Governance Policy

This policy applies to every project in this repository without exception.

## The rule

**No real customer, complaint, account, or transaction data — de-identified or otherwise — is ever committed to this repository.**

All real NCRP/CFCFRMS complaint data and any other production-sourced banking data used during development stays strictly local, under India's DPDP Act 2023 and the author's employer information-security policy. It is never uploaded to any third-party AI tool and never leaves the local machine.

## What goes in the public repo instead

- Every dataset published here is **synthetically generated** — built by purpose-written generators that reproduce the *statistical shape and typology patterns* of real financial-crime data without containing a single real account, complaint, or individual.
- Where a real dataset informed design decisions (e.g. rulebook thresholds, schema shape), only the **de-identified structural learnings** are reflected in code and documentation — never the underlying records.
- Geographic references in any dashboard or map view are limited to **district-level names only**; no finer-grained location data is published.

## Enforcement

- A `.gitignore` guard (see repository root) has been in place from the first commit of every project folder, excluding common raw-data paths and file patterns by default.
- Before any commit touching a `data/` folder, the real-vs-synthetic status of every file must be verified.
- If a real-data file is ever found to have been committed in error, it must be purged from the full git history (not just deleted in a new commit) before the repository is next pushed.

## Why this matters for this portfolio specifically

This isn't just a legal/compliance formality — it's part of the portfolio's own argument: a financial-crime analytics practitioner who treats data governance as an afterthought has no credibility discussing AML/CFT controls. The same discipline applied to production transaction-monitoring data governs every file published here.
