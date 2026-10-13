# TYPHON — generator and rules-layer build notes

## Status

**Built and verified**, not reconstructed from memory. The synthetic dataset generator and the SQL rules layer in this repo were written fresh against TYPHON's documented spec (see [`RECOVERY-STATUS.md`](./RECOVERY-STATUS.md) for why the original script wasn't recoverable), then actually run end-to-end: generated, loaded into a local PostgreSQL 16 instance, queried, and checked against the dataset's own synthetic ground truth before being committed.

## What was verified, not just written

- `generator/generate_dataset.py` produces exactly **98 accounts** and (after a target-rescaling pass) exactly **5,000 transaction rows** — matching the documented spec.
- The output loads cleanly into the schema at `sql/schema.sql` with no errors.
- `sql/rules.sql` — a five-rule SQL monitoring layer, one rule per injected typology — was run against the loaded data and checked against the labels table (synthetic ground truth, present only because this is a demonstration dataset — see the honesty statement in `themis/docs/THEMIS_Solution_Blueprint_v1.1.md` §19/§22, which applies here too).

**Result: 100% precision and 100% recall** across all five rules on this synthetic dataset — every injected account was caught by its matching rule, with zero false positives from other typologies or normal accounts.

This number is a demonstration-dataset diagnostic, not a production detection-rate claim. Two bugs were caught and fixed during this verification pass specifically because the result was checked against ground truth rather than assumed correct:

1. **Mule-inflow (R03) false negative** — the generator originally scattered a mule-inflow account's inbound transfers randomly across the full 180-day window, so no 30-day rolling window ever saw 12+ distinct senders. Fixed by clustering those transfers into a 20-day burst, which is also the more realistic shape for a fan-in pattern.
2. **Dormant-reactivation (R04) over-firing** — a first draft of the rule flagged *any* account's first transaction as a potential "reactivation," which falsely caught busy accounts with an incidental 5-transaction cluster somewhere in six months. Rewritten to anchor on the account's `open_date` and its *entire* visible transaction history being a tight recent burst, which brought false positives to zero.

## Design choices made (flagged for author review)

Per the portfolio's division of labour, these are build-default choices made to match the documented spec and the portfolio's established typology taxonomy — not domain decisions blessed by the author the way THEMIS's four locked calls were. Review and adjust the `CONFIG` block in `generator/generate_dataset.py` if any of these should change:

- **Typology set**: the same five typologies THEMIS later extends (structuring, rapid-movement/pass-through, mule-inflow fan-in, dormant-reactivation, threshold-hugging) — chosen for lineage consistency across TYPHON → THEMIS → NEMESIS.
- **Segment mix**: retail 55% / SME 20% / high-risk-occupation 15% / new-to-bank 10% — mirrors THEMIS's four segments.
- **Typology injection rate**: ~22% of accounts, spread evenly across the five typologies (4–5 accounts each) rather than pure-random allocation, so every typology has a usable sample at this population size.
- **Reporting ceiling / thresholds**: synthetic round numbers (₹50,000 structuring ceiling, ₹100,000 threshold-hugging line) — illustrative, not any real institution's actual limits.

## What's still to build

- Python ML scoring layer (scikit-learn classification + NetworkX graph analytics + autoencoder anomaly detection) over the alerts this rules layer produces
- GenAI layer for SAR drafting and typology classification
- Tableau risk-operations dashboard

## Reproducing this build

```bash
cd typhon/generator
python3 generate_dataset.py --load-db   # writes CSVs to ../data/ and loads PostgreSQL
psql -d typhon_dev -f ../sql/rules.sql   # runs the five-rule monitoring layer
```

Requires a local PostgreSQL instance (`CREATE DATABASE typhon_dev;` first) and `pandas`, `numpy`, `psycopg2-binary`. Connection string is configurable via `--dsn`.
