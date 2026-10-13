-- TYPHON — SQL rules-based monitoring layer.
-- Each query implements one scenario from the `scenarios` table and inserts
-- any accounts it fires on into `alerts`. Run after loading data with
-- ../generator/generate_dataset.py --load-db.
--
-- These are deliberately simple, inspectable rules (matching the synthetic
-- typology-injection logic in the generator) — the point is a working,
-- defensible rules layer that the ML layer (src/) scores on top of, not a
-- production-grade rulebook.

-- R01 — Structuring: 4+ credits in a 10-day window, each within 18% of the
-- reporting ceiling (50,000), summing well above it.
INSERT INTO alerts (scenario_id, account_id, evidence_txn_ids)
SELECT 'R01', account_id, array_agg(txn_id)
FROM (
    SELECT txn_id, account_id, txn_timestamp,
           count(*) OVER (PARTITION BY account_id ORDER BY txn_timestamp
                           RANGE BETWEEN INTERVAL '10 days' PRECEDING AND CURRENT ROW) AS cluster_count
    FROM transactions
    WHERE direction = 'credit'
      AND amount BETWEEN 50000 * 0.80 AND 50000 * 0.995
) t
WHERE cluster_count >= 4
GROUP BY account_id;

-- R02 — Rapid movement / pass-through: a credit >= 80,000 followed within 36
-- hours by a debit that returns at least 85% of the credited value.
INSERT INTO alerts (scenario_id, account_id, evidence_txn_ids)
SELECT 'R02', c.account_id, ARRAY[c.txn_id, d.txn_id]
FROM transactions c
JOIN transactions d
  ON d.account_id = c.account_id
 AND d.direction = 'debit'
 AND d.txn_timestamp BETWEEN c.txn_timestamp AND c.txn_timestamp + INTERVAL '36 hours'
 AND d.amount >= c.amount * 0.85
WHERE c.direction = 'credit'
  AND c.amount >= 80000;

-- R03 — Mule inflow / fan-in: 12+ distinct counterparties crediting the same
-- account within any 30-day window. (Postgres doesn't support COUNT(DISTINCT
-- ...) as a window function, so this uses a per-row correlated subquery
-- instead of a window clause.)
INSERT INTO alerts (scenario_id, account_id, evidence_txn_ids)
SELECT 'R03', account_id, array_agg(txn_id)
FROM (
    SELECT t.txn_id, t.account_id,
           (SELECT count(DISTINCT t2.counterparty_id)
            FROM transactions t2
            WHERE t2.account_id = t.account_id
              AND t2.direction = 'credit'
              AND t2.counterparty_id IS NOT NULL
              AND t2.txn_timestamp BETWEEN t.txn_timestamp - INTERVAL '30 days' AND t.txn_timestamp
           ) AS distinct_senders
    FROM transactions t
    WHERE t.direction = 'credit' AND t.counterparty_id IS NOT NULL
) t
WHERE distinct_senders >= 12
GROUP BY account_id;

-- R04 — Dormant reactivation: an account open well before the observation
-- window, whose *entire* visible transaction history is a tight burst of
-- 5+ transactions inside a 10-day span — i.e. it shows no activity at all
-- until a sudden recent cluster. (A simple LAG-based "gap since previous
-- transaction" version over-fires: every account's very first transaction
-- in the window trivially has no predecessor, so busy accounts with an
-- unrelated 5-transaction cluster anywhere in 180 days false-positive.
-- Anchoring to the account's full history and its open_date, rather than
-- a single consecutive-pair gap, is what makes this rule precise.)
INSERT INTO alerts (scenario_id, account_id, evidence_txn_ids)
SELECT 'R04', t.account_id, array_agg(t.txn_id)
FROM transactions t
JOIN accounts a ON a.account_id = t.account_id
WHERE a.open_date <= (SELECT min(txn_timestamp)::date - INTERVAL '60 days' FROM transactions t2 WHERE t2.account_id = t.account_id)
GROUP BY t.account_id
HAVING count(*) >= 5
   AND max(t.txn_timestamp) - min(t.txn_timestamp) <= INTERVAL '10 days';

-- R05 — Threshold-hugging: 8+ credits clustered between 90% and 99.5% of a
-- round-number threshold (100,000).
INSERT INTO alerts (scenario_id, account_id, evidence_txn_ids)
SELECT 'R05', account_id, array_agg(txn_id)
FROM transactions
WHERE direction = 'credit'
  AND amount BETWEEN 100000 * 0.90 AND 100000 * 0.995
GROUP BY account_id
HAVING count(*) >= 8;
