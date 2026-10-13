-- TYPHON — PostgreSQL schema
-- Hybrid rules + ML + GenAI alert-triage and SAR-drafting framework.
-- Synthetic data only. See ../../docs/DATA-GOVERNANCE.md.

DROP TABLE IF EXISTS labels CASCADE;
DROP TABLE IF EXISTS alerts CASCADE;
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS accounts CASCADE;
DROP TABLE IF EXISTS scenarios CASCADE;

-- Accounts: the population the rulebook and ML layer score.
CREATE TABLE accounts (
    account_id          VARCHAR(12) PRIMARY KEY,
    segment             VARCHAR(30) NOT NULL,       -- retail / sme / high_risk_occupation / new_to_bank
    open_date           DATE NOT NULL,
    baseline_monthly_txn_count   INTEGER NOT NULL,  -- expected "normal" activity level for this account
    baseline_monthly_txn_value   NUMERIC(14,2) NOT NULL,
    is_dormant_at_open  BOOLEAN NOT NULL DEFAULT FALSE
);

-- Scenarios: the rulebook. Parameters are columns, not hard-coded logic,
-- so sweeps and tuning operate on data (mirrors the THEMIS design).
CREATE TABLE scenarios (
    scenario_id         VARCHAR(10) PRIMARY KEY,
    typology             VARCHAR(40) NOT NULL,
    description           TEXT NOT NULL,
    threshold_amount      NUMERIC(14,2),
    window_days            INTEGER,
    ratio_param             NUMERIC(5,2),   -- e.g. pass-through ratio
    count_param            INTEGER          -- e.g. fan-in count threshold
);

-- Transactions: the core ledger. One row per transaction leg.
CREATE TABLE transactions (
    txn_id              BIGSERIAL PRIMARY KEY,
    account_id           VARCHAR(12) NOT NULL REFERENCES accounts(account_id),
    counterparty_id       VARCHAR(12),            -- another account_id, or NULL for external counterparty
    direction              VARCHAR(6) NOT NULL CHECK (direction IN ('credit','debit')),
    amount                  NUMERIC(14,2) NOT NULL CHECK (amount > 0),
    channel                  VARCHAR(20) NOT NULL,  -- upi / neft / imps / cash / card
    txn_timestamp            TIMESTAMP NOT NULL,
    batch_id                  VARCHAR(20) NOT NULL DEFAULT 'SEED_BATCH_001',
    loaded_at                  TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_txn_account ON transactions(account_id);
CREATE INDEX idx_txn_timestamp ON transactions(txn_timestamp);
CREATE INDEX idx_txn_counterparty ON transactions(counterparty_id);

-- Alerts: what fired when the rulebook (sql/rules.sql) is run.
CREATE TABLE alerts (
    alert_id             BIGSERIAL PRIMARY KEY,
    scenario_id            VARCHAR(10) NOT NULL REFERENCES scenarios(scenario_id),
    account_id              VARCHAR(12) NOT NULL REFERENCES accounts(account_id),
    fired_at                  TIMESTAMP NOT NULL DEFAULT now(),
    evidence_txn_ids           BIGINT[]   -- the transactions that triggered this alert
);

-- Labels: SYNTHETIC ground truth only, used to validate the method.
-- Never available in production — see honesty statement in docs.
CREATE TABLE labels (
    account_id            VARCHAR(12) PRIMARY KEY REFERENCES accounts(account_id),
    typology                VARCHAR(40),            -- NULL = normal / no injected typology
    is_true_positive          BOOLEAN NOT NULL DEFAULT FALSE
);
