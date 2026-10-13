#!/usr/bin/env python3
"""
TYPHON synthetic dataset generator.

Produces a labelled, reproducible synthetic AML dataset matching TYPHON's
documented spec: ~98 accounts, ~5,000 transaction rows, typology injection,
loadable into the PostgreSQL schema at ../sql/schema.sql.

This generator is the shared foundation for the portfolio's synthetic data
lineage: THEMIS extends it into a larger, purpose-shaped derivative dataset
(see themis/docs/THEMIS_Solution_Blueprint_v1.1.md §7-9), and NEMESIS
red-teams the detection logic trained on it.

NO REAL DATA. Every account, transaction, and typology label here is
synthetically generated. See ../../docs/DATA-GOVERNANCE.md.

Usage:
    python generate_dataset.py                  # writes CSVs to ../data/
    python generate_dataset.py --load-db         # also loads into Postgres
    python generate_dataset.py --seed 7          # change the reproducible seed

Domain calls below (typology set, account population, segment mix,
injection rate) are build-default choices made to match the documented
spec and the portfolio's established typology taxonomy (the same five
typologies THEMIS later extends). They are flagged here for the author's
review/sign-off per the project's division of labour — change the
CONFIG block and re-run to adjust any of them.
"""

import argparse
import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# CONFIG — the domain calls. Review and adjust before treating this as final.
# ---------------------------------------------------------------------------

N_ACCOUNTS = 98
TARGET_TXN_ROWS = 5000

SEGMENTS = {
    # segment: (share of population, baseline monthly txn count range, baseline monthly value range)
    "retail":               (0.55, (4, 15),  (5_000, 60_000)),
    "sme":                   (0.20, (15, 60), (50_000, 800_000)),
    "high_risk_occupation":   (0.15, (5, 25),  (10_000, 300_000)),
    "new_to_bank":             (0.10, (1, 8),   (1_000, 40_000)),
}

# Five typologies, consistent across the TYPHON -> THEMIS -> NEMESIS lineage.
TYPOLOGIES = [
    "structuring",
    "rapid_movement_passthrough",
    "mule_inflow_fanin",
    "dormant_reactivation",
    "threshold_hugging",
]

# Share of accounts carrying an injected typology (the rest are "normal").
TYPOLOGY_INJECTION_RATE = 0.22  # ~22% of accounts, consistent with a labelled-dataset design

CHANNELS = ["upi", "neft", "imps", "cash", "card"]

DATE_WINDOW_DAYS = 180  # all transactions fall within a 6-month synthetic window
WINDOW_END = datetime(2026, 9, 30)
WINDOW_START = WINDOW_END - timedelta(days=DATE_WINDOW_DAYS)

REPORTING_CEILING = 50_000  # synthetic structuring reporting ceiling

# ---------------------------------------------------------------------------


def make_account_ids(n):
    return [f"ACC{str(i).zfill(5)}" for i in range(1, n + 1)]


def assign_segments(account_ids, rng):
    segments = list(SEGMENTS.keys())
    weights = [SEGMENTS[s][0] for s in segments]
    return rng.choice(segments, size=len(account_ids), p=weights)


def build_accounts(rng):
    account_ids = make_account_ids(N_ACCOUNTS)
    seg_assignment = assign_segments(account_ids, rng)

    rows = []
    for acc_id, seg in zip(account_ids, seg_assignment):
        _, count_range, value_range = SEGMENTS[seg]
        open_date = WINDOW_START - timedelta(days=int(rng.integers(30, 2000)))
        baseline_count = int(rng.integers(count_range[0], count_range[1] + 1))
        baseline_value = float(rng.uniform(*value_range))
        rows.append({
            "account_id": acc_id,
            "segment": seg,
            "open_date": open_date.date(),
            "baseline_monthly_txn_count": baseline_count,
            "baseline_monthly_txn_value": round(baseline_value, 2),
            "is_dormant_at_open": False,
        })
    return pd.DataFrame(rows)


def assign_typologies(accounts_df, rng):
    """Assign each account either a typology label or 'normal'.

    Injected accounts are spread as evenly as possible across the five
    typologies (stratified, not pure random choice) so every typology has
    enough accounts to be a usable demonstration/detection sample even at
    this small population size — a handful of structuring accounts out of
    98 would be too thin to say anything about detection performance.
    """
    n_injected = int(round(len(accounts_df) * TYPOLOGY_INJECTION_RATE))
    injected_idx = rng.choice(accounts_df.index, size=n_injected, replace=False)

    # Round-robin allocation across typologies, then shuffle which specific
    # account gets which typology.
    base = n_injected // len(TYPOLOGIES)
    remainder = n_injected % len(TYPOLOGIES)
    typology_pool = []
    for i, t in enumerate(TYPOLOGIES):
        count = base + (1 if i < remainder else 0)
        typology_pool.extend([t] * count)
    rng.shuffle(typology_pool)

    labels = pd.Series("normal", index=accounts_df.index, dtype=object)
    labels.loc[injected_idx] = typology_pool
    return labels


def random_timestamp(rng, start=WINDOW_START, end=WINDOW_END):
    delta = end - start
    seconds = int(rng.integers(0, int(delta.total_seconds())))
    return start + timedelta(seconds=seconds)


def gen_normal_txns(acc_id, account_row, rng, n_txns):
    """Baseline, unremarkable activity for an account with no injected typology."""
    rows = []
    for _ in range(n_txns):
        direction = rng.choice(["credit", "debit"], p=[0.48, 0.52])
        amount = max(100.0, float(rng.normal(
            account_row["baseline_monthly_txn_value"] / max(account_row["baseline_monthly_txn_count"], 1),
            account_row["baseline_monthly_txn_value"] / max(account_row["baseline_monthly_txn_count"], 1) * 0.4,
        )))
        rows.append({
            "account_id": acc_id,
            "counterparty_id": None,
            "direction": direction,
            "amount": round(amount, 2),
            "channel": rng.choice(CHANNELS),
            "txn_timestamp": random_timestamp(rng),
        })
    return rows


def gen_structuring_txns(acc_id, rng):
    """Multiple transactions just below the reporting ceiling, clustered in a short window."""
    rows = []
    n_structured = int(rng.integers(4, 9))
    cluster_start = random_timestamp(rng, end=WINDOW_END - timedelta(days=10))
    for i in range(n_structured):
        amount = REPORTING_CEILING * float(rng.uniform(0.82, 0.98))
        ts = cluster_start + timedelta(days=int(rng.integers(0, 7)), hours=int(rng.integers(0, 23)))
        rows.append({
            "account_id": acc_id,
            "counterparty_id": None,
            "direction": "credit",
            "amount": round(amount, 2),
            "channel": rng.choice(["cash", "neft", "imps"]),
            "txn_timestamp": ts,
        })
    return rows


def gen_rapid_movement_txns(acc_id, rng):
    """A large credit followed quickly by a near-equal debit (pass-through)."""
    rows = []
    n_cycles = int(rng.integers(3, 7))
    for _ in range(n_cycles):
        credit_amt = float(rng.uniform(80_000, 600_000))
        ts_in = random_timestamp(rng, end=WINDOW_END - timedelta(days=1))
        ts_out = ts_in + timedelta(hours=float(rng.uniform(0.5, 36)))
        rows.append({
            "account_id": acc_id, "counterparty_id": None, "direction": "credit",
            "amount": round(credit_amt, 2), "channel": rng.choice(["neft", "imps", "upi"]),
            "txn_timestamp": ts_in,
        })
        rows.append({
            "account_id": acc_id, "counterparty_id": None, "direction": "debit",
            "amount": round(credit_amt * float(rng.uniform(0.85, 0.99)), 2),
            "channel": rng.choice(["neft", "imps", "upi"]), "txn_timestamp": ts_out,
        })
    return rows


def gen_mule_inflow_txns(acc_id, other_account_ids, rng):
    """Many small inbound transfers from distinct counterparties (fan-in),
    clustered inside a 20-day window — fan-in is a *burst* pattern, not
    senders trickling in evenly over six months, and the detection rule
    (R03) looks for 12+ distinct senders within a 30-day window."""
    rows = []
    n_inflows = int(rng.integers(12, 30))
    senders = rng.choice(other_account_ids, size=min(n_inflows, len(other_account_ids)), replace=False)
    cluster_start = random_timestamp(rng, end=WINDOW_END - timedelta(days=20))
    for sender in senders:
        amount = float(rng.uniform(2_000, 40_000))
        ts = cluster_start + timedelta(days=float(rng.uniform(0, 20)), hours=float(rng.uniform(0, 23)))
        rows.append({
            "account_id": acc_id, "counterparty_id": sender, "direction": "credit",
            "amount": round(amount, 2), "channel": rng.choice(["upi", "imps"]),
            "txn_timestamp": ts,
        })
    return rows


def gen_dormant_reactivation_txns(acc_id, rng):
    """Long quiet period, then a short burst of activity."""
    rows = []
    burst_start = WINDOW_END - timedelta(days=int(rng.integers(5, 20)))
    n_burst = int(rng.integers(5, 12))
    for _ in range(n_burst):
        ts = burst_start + timedelta(days=int(rng.integers(0, 10)), hours=int(rng.integers(0, 23)))
        amount = float(rng.uniform(15_000, 250_000))
        rows.append({
            "account_id": acc_id, "counterparty_id": None,
            "direction": rng.choice(["credit", "debit"], p=[0.6, 0.4]),
            "amount": round(amount, 2), "channel": rng.choice(CHANNELS),
            "txn_timestamp": ts,
        })
    return rows


def gen_threshold_hugging_txns(acc_id, rng):
    """Repeated transactions clustered just under a round-number threshold."""
    rows = []
    n_txns = int(rng.integers(8, 16))
    threshold = 100_000
    for _ in range(n_txns):
        amount = threshold * float(rng.uniform(0.90, 0.995))
        rows.append({
            "account_id": acc_id, "counterparty_id": None, "direction": "credit",
            "amount": round(amount, 2), "channel": rng.choice(["neft", "imps"]),
            "txn_timestamp": random_timestamp(rng),
        })
    return rows


def build_transactions(accounts_df, typology_labels, rng):
    all_rows = []
    account_ids = accounts_df["account_id"].tolist()

    for _, acc in accounts_df.iterrows():
        acc_id = acc["account_id"]
        typology = typology_labels[acc.name]

        if typology == "normal":
            months_active = DATE_WINDOW_DAYS / 30
            n_txns = max(2, int(round(acc["baseline_monthly_txn_count"] * months_active * rng.uniform(0.7, 1.3))))
            all_rows.extend(gen_normal_txns(acc_id, acc, rng, n_txns))
        elif typology == "structuring":
            all_rows.extend(gen_structuring_txns(acc_id, rng))
            all_rows.extend(gen_normal_txns(acc_id, acc, rng, int(rng.integers(5, 15))))
        elif typology == "rapid_movement_passthrough":
            all_rows.extend(gen_rapid_movement_txns(acc_id, rng))
            all_rows.extend(gen_normal_txns(acc_id, acc, rng, int(rng.integers(3, 10))))
        elif typology == "mule_inflow_fanin":
            others = [a for a in account_ids if a != acc_id]
            all_rows.extend(gen_mule_inflow_txns(acc_id, others, rng))
            all_rows.extend(gen_normal_txns(acc_id, acc, rng, int(rng.integers(2, 8))))
        elif typology == "dormant_reactivation":
            all_rows.extend(gen_dormant_reactivation_txns(acc_id, rng))
        elif typology == "threshold_hugging":
            all_rows.extend(gen_threshold_hugging_txns(acc_id, rng))
            all_rows.extend(gen_normal_txns(acc_id, acc, rng, int(rng.integers(3, 10))))

    txns_df = pd.DataFrame(all_rows)
    txns_df = txns_df.sort_values("txn_timestamp").reset_index(drop=True)
    txns_df.insert(0, "txn_id", range(1, len(txns_df) + 1))
    txns_df["batch_id"] = "SEED_BATCH_001"
    return txns_df


def rescale_to_target(txns_df, accounts_df, typology_labels, rng, target=TARGET_TXN_ROWS, tolerance=0.08):
    """Nudge total row count toward the target spec by trimming or topping up
    'normal' accounts' transaction counts, without touching injected-typology
    accounts (their counts are typology-defining, not incidental)."""
    current = len(txns_df)
    if abs(current - target) / target <= tolerance:
        return txns_df

    normal_accounts = [acc_id for acc_id, lab in zip(accounts_df["account_id"], typology_labels) if lab == "normal"]

    if current < target:
        deficit = target - current
        extra_rows = []
        while deficit > 0 and normal_accounts:
            acc_id = rng.choice(normal_accounts)
            acc_row = accounts_df.set_index("account_id").loc[acc_id]
            batch = gen_normal_txns(acc_id, acc_row, rng, min(deficit, 5))
            extra_rows.extend(batch)
            deficit -= len(batch)
        if extra_rows:
            extra_df = pd.DataFrame(extra_rows)
            txns_df = pd.concat([txns_df.drop(columns=["txn_id", "batch_id"]), extra_df], ignore_index=True)
    else:
        surplus = current - target
        normal_mask = txns_df["account_id"].isin(normal_accounts)
        drop_candidates = txns_df[normal_mask].sample(n=min(surplus, normal_mask.sum()), random_state=int(rng.integers(0, 1_000_000))).index
        txns_df = txns_df.drop(index=drop_candidates)

    txns_df = txns_df.sort_values("txn_timestamp").reset_index(drop=True)
    txns_df.insert(0, "txn_id", range(1, len(txns_df) + 1)) if "txn_id" not in txns_df.columns else None
    txns_df["txn_id"] = range(1, len(txns_df) + 1)
    txns_df["batch_id"] = "SEED_BATCH_001"
    return txns_df


def build_scenarios():
    rows = [
        {"scenario_id": "R01", "typology": "structuring", "description": "Cumulative credits near reporting ceiling, clustered within a short window",
         "threshold_amount": REPORTING_CEILING, "window_days": 10, "ratio_param": None, "count_param": 4},
        {"scenario_id": "R02", "typology": "rapid_movement_passthrough", "description": "Large credit followed by a near-equal debit within 36 hours",
         "threshold_amount": 80_000, "window_days": None, "ratio_param": 0.85, "count_param": None},
        {"scenario_id": "R03", "typology": "mule_inflow_fanin", "description": "Many-to-one inbound fan-in from distinct counterparties within a window",
         "threshold_amount": 2_000, "window_days": 30, "ratio_param": None, "count_param": 12},
        {"scenario_id": "R04", "typology": "dormant_reactivation", "description": "Account inactive, then a short burst of activity",
         "threshold_amount": 15_000, "window_days": 10, "ratio_param": None, "count_param": 5},
        {"scenario_id": "R05", "typology": "threshold_hugging", "description": "Repeated transactions clustered just under a round-number threshold",
         "threshold_amount": 100_000, "window_days": None, "ratio_param": 0.90, "count_param": 8},
    ]
    return pd.DataFrame(rows)


def build_labels(accounts_df, typology_labels):
    rows = []
    for _, acc in accounts_df.iterrows():
        typology = typology_labels[acc.name]
        rows.append({
            "account_id": acc["account_id"],
            "typology": None if typology == "normal" else typology,
            "is_true_positive": typology != "normal",
        })
    return pd.DataFrame(rows)


def _rows(df, cols):
    """DataFrame -> list of row-tuples with NaN replaced by None, and numpy
    scalar types converted to native Python types (psycopg2 chokes on both)."""
    clean = df[cols].astype(object).where(pd.notnull(df[cols]), None)
    rows = []
    for row in clean.itertuples(index=False, name=None):
        converted = []
        for v in row:
            if isinstance(v, (np.integer,)):
                converted.append(int(v))
            elif isinstance(v, (np.floating,)):
                converted.append(None if np.isnan(v) else float(v))
            elif isinstance(v, (np.bool_,)):
                converted.append(bool(v))
            else:
                converted.append(v)
        rows.append(tuple(converted))
    return rows


def load_to_postgres(accounts_df, scenarios_df, txns_df, labels_df, dsn):
    import psycopg2
    from psycopg2.extras import execute_values

    conn = psycopg2.connect(dsn)
    cur = conn.cursor()

    schema_path = os.path.join(os.path.dirname(__file__), "..", "sql", "schema.sql")
    with open(schema_path) as f:
        cur.execute(f.read())

    execute_values(cur,
        "INSERT INTO accounts (account_id, segment, open_date, baseline_monthly_txn_count, baseline_monthly_txn_value, is_dormant_at_open) VALUES %s",
        _rows(accounts_df, ["account_id", "segment", "open_date", "baseline_monthly_txn_count", "baseline_monthly_txn_value", "is_dormant_at_open"]))

    execute_values(cur,
        "INSERT INTO scenarios (scenario_id, typology, description, threshold_amount, window_days, ratio_param, count_param) VALUES %s",
        _rows(scenarios_df, ["scenario_id", "typology", "description", "threshold_amount", "window_days", "ratio_param", "count_param"]))

    txn_cols = ["account_id", "counterparty_id", "direction", "amount", "channel", "txn_timestamp", "batch_id"]
    execute_values(cur,
        f"INSERT INTO transactions ({', '.join(txn_cols)}) VALUES %s",
        _rows(txns_df, txn_cols))

    execute_values(cur,
        "INSERT INTO labels (account_id, typology, is_true_positive) VALUES %s",
        _rows(labels_df, ["account_id", "typology", "is_true_positive"]))

    conn.commit()
    cur.close()
    conn.close()


def main():
    parser = argparse.ArgumentParser(description="Generate the TYPHON synthetic dataset.")
    parser.add_argument("--seed", type=int, default=42, help="Reproducible random seed (default 42)")
    parser.add_argument("--load-db", action="store_true", help="Also load the generated data into PostgreSQL")
    parser.add_argument("--dsn", type=str, default="dbname=typhon_dev user=postgres password=typhon_dev host=localhost",
                         help="PostgreSQL connection string, used only with --load-db")
    parser.add_argument("--out-dir", type=str, default=os.path.join(os.path.dirname(__file__), "..", "data"),
                         help="Directory to write the generated CSVs")
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    random.seed(args.seed)

    accounts_df = build_accounts(rng)
    typology_labels = assign_typologies(accounts_df, rng)
    scenarios_df = build_scenarios()
    txns_df = build_transactions(accounts_df, typology_labels, rng)
    txns_df = rescale_to_target(txns_df, accounts_df, typology_labels, rng)
    labels_df = build_labels(accounts_df, typology_labels)

    os.makedirs(args.out_dir, exist_ok=True)
    accounts_df.to_csv(os.path.join(args.out_dir, "accounts.csv"), index=False)
    scenarios_df.to_csv(os.path.join(args.out_dir, "scenarios.csv"), index=False)
    txns_df.to_csv(os.path.join(args.out_dir, "transactions.csv"), index=False)
    labels_df.to_csv(os.path.join(args.out_dir, "labels.csv"), index=False)

    print(f"Accounts:      {len(accounts_df):>6}")
    print(f"Transactions:  {len(txns_df):>6}")
    print(f"Scenarios:     {len(scenarios_df):>6}")
    print(f"Typology distribution:")
    print(typology_labels.value_counts().to_string())
    print(f"\nCSV files written to {os.path.abspath(args.out_dir)}")

    if args.load_db:
        load_to_postgres(accounts_df, scenarios_df, txns_df, labels_df, args.dsn)
        print("Loaded into PostgreSQL.")


if __name__ == "__main__":
    main()
