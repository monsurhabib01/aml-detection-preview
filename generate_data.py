import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
import argparse

from reg_profile import RegProfile

SEED = 42
np.random.seed(SEED)
random.seed(SEED)

N_NORMAL        = 9_500
N_STRUCTURING   = 150
N_VELOCITY      = 80
N_LATE_NIGHT    = 120
N_ROUND_AMOUNT  = 100
N_DORMANT_SPIKE = 50

DORMANT_SEED_START = datetime(2023, 10, 1)
START_DATE = datetime(2024, 1, 1)
END_DATE   = datetime(2024, 3, 31)
DATE_RANGE_DAYS = (END_DATE - START_DATE).days

N_CUSTOMERS = 300


def random_account(profile: RegProfile):
    if profile.country.lower() == 'bangladesh':
        return f"01{random.randint(3, 9)}{random.randint(10_000_000, 99_999_999)}"
    elif profile.country.lower() == 'pakistan':
        return f"03{random.randint(0, 9)}{random.randint(10_000_000, 99_999_999)}"
    elif profile.country.lower() == 'india':
        return f"91{random.randint(600_000_000, 999_999_999)}"
    elif profile.country.lower() == 'nigeria':
        return f"234{random.randint(700_000_000, 999_999_999)}"
    elif profile.country.lower() == 'kenya':
        return f"254{random.randint(700_000_000, 999_999_999)}"
    else:
        return f"ACCT{random.randint(10_000_000, 99_999_999)}"


def random_timestamp(start=START_DATE, days=DATE_RANGE_DAYS, late_night=False):
    if late_night:
        offset = timedelta(
            days=random.randint(0, days),
            hours=random.randint(1, 3),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )
    else:
        offset = timedelta(
            days=random.randint(0, days),
            hours=random.randint(7, 22),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )
    return start + offset


def make_row(sender, receiver, amount, tx_type, ts, anomaly_flag="NORMAL", currency="BDT"):
    return {
        "transaction_id": f"TXN{random.randint(100_000_000, 999_999_999)}",
        "timestamp":      ts,
        "sender_id":      sender,
        "receiver_id":    receiver,
        "tx_type":        tx_type,
        f"amount_{currency.lower()}": int(round(amount)),
        "currency":       currency,
        "anomaly_flag":   anomaly_flag,
    }


def generate_data(profile_name="bangladesh"):
    print(f"\n{'='*55}")
    print(f"  Generating synthetic MFS data for: {profile_name.title()}")
    print(f"{'='*55}")

    profile = RegProfile.load(profile_name)
    currency = profile.currency.lower()
    amt_field = f"amount_{currency}"
    tx_types = profile.tx_types
    tx_type_weights = [1.0 / len(tx_types)] * len(tx_types)

    a_cfg = profile.amounts
    t_cfg = profile.thresholds
    r_amt = profile._rule_amounts

    normal_mu = a_cfg.mu
    normal_sigma = a_cfg.sigma
    anomaly_mu = a_cfg.anomaly_mu
    anomaly_sigma = a_cfg.anomaly_sigma

    struct_lower    = r_amt['structuring_lower']
    struct_upper    = r_amt['structuring_upper']
    struct_min_txns = r_amt['structuring_min_txns']
    vel_txns_ph     = r_amt['velocity_txns_per_hour']
    vel_window_mins = r_amt['velocity_window_mins']
    unusual_hours   = r_amt['unusual_hours']
    dormant_days    = r_amt['dormant_days']
    dormant_min_amt = r_amt['dormant_min_amount']
    round_min_amt   = r_amt['round_min_amount']
    round_divisor   = r_amt['round_divisor']

    struct_spacing_minutes = max(5, int(24 * 60 / struct_min_txns / 2))

    customers = [random_account(profile) for _ in range(N_CUSTOMERS)]
    dormant_pool = [random_account(profile) for _ in range(N_DORMANT_SPIKE)]

    rows = []

    for _ in range(N_NORMAL):
        sender   = random.choice(customers)
        receiver = random.choice([c for c in customers if c != sender])
        tx_type  = np.random.choice(tx_types, p=tx_type_weights)
        amount = np.random.lognormal(mean=normal_mu, sigma=normal_sigma)
        amount = min(amount, t_cfg.ctr_amount * 0.5)
        amount = round(amount)
        ts = random_timestamp()
        rows.append(make_row(sender, receiver, amount, tx_type, ts, "NORMAL", currency))

    structuring_senders = random.choices(customers, k=35)
    for sender in structuring_senders:
        cluster_size = random.randint(struct_min_txns, struct_min_txns + 2)
        base_ts = random_timestamp()
        for i in range(cluster_size):
            amount   = random.randint(int(struct_lower), int(struct_upper))
            receiver = random.choice([c for c in customers if c != sender])
            ts       = base_ts + timedelta(minutes=random.randint(
                struct_spacing_minutes - 10, struct_spacing_minutes + 10))
            rows.append(make_row(sender, receiver, amount, 'send_money', ts, "STRUCTURING", currency))

    velocity_senders = random.choices(customers, k=10)
    for sender in velocity_senders:
        burst_count = random.randint(vel_txns_ph + 1, vel_txns_ph + 6)
        base_ts = random_timestamp()
        for i in range(burst_count):
            amount   = random.randint(500, int(t_cfg.str_amount * 0.05))
            receiver = random.choice([c for c in customers if c != sender])
            ts       = base_ts + timedelta(minutes=random.randint(0, vel_window_mins - 1))
            rows.append(make_row(sender, receiver, amount, random.choice(tx_types), ts, "VELOCITY", currency))

    for _ in range(N_LATE_NIGHT):
        sender   = random.choice(customers)
        receiver = random.choice([c for c in customers if c != sender])
        amount   = random.randint(1_000, int(t_cfg.str_amount * 0.05))
        tx_type  = np.random.choice(tx_types, p=tx_type_weights)
        ts       = random_timestamp(late_night=True)
        rows.append(make_row(sender, receiver, amount, tx_type, ts, "LATE_NIGHT", currency))

    round_amounts = [round_min_amt * m for m in [1, 2, 5, 10]]
    round_amounts = [int(a) for a in round_amounts]
    for _ in range(N_ROUND_AMOUNT):
        sender   = random.choice(customers)
        receiver = random.choice([c for c in customers if c != sender])
        amount = random.choice(round_amounts)
        ts       = random_timestamp()
        rows.append(make_row(sender, receiver, amount, 'send_money', ts, "ROUND_AMOUNT", currency))
    for acc in dormant_pool:
        seed_ts = DORMANT_SEED_START + timedelta(days=random.randint(0, 60))
        receiver = random.choice(customers)
        seed_amount = random.randint(200, 1000)
        rows.append(make_row(acc, receiver, seed_amount, random.choice(tx_types), seed_ts, "NORMAL", currency))

        spike_day = random.randint(10, DATE_RANGE_DAYS - 5)
        spike_ts  = START_DATE + timedelta(days=spike_day)
        receiver  = random.choice(customers)
        amount    = random.randint(int(dormant_min_amt), int(dormant_min_amt * 2))
        rows.append(make_row(acc, receiver, amount, random.choice(tx_types), spike_ts, "DORMANT_SPIKE", currency))

    df = pd.DataFrame(rows)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    os.makedirs("outputs", exist_ok=True)
    path = f"outputs/raw_transactions_{profile_name}.csv"
    df.to_csv(path, index=False)

    print(f"\n  Generated {len(df):,} transactions for {profile.country}")
    print(df["anomaly_flag"].value_counts().to_string())
    print(f"\n  Date range: {df['timestamp'].min().date()} -> {df['timestamp'].max().date()}")
    print(f"  Saved to: {path}\n")

    return df, profile


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic MFS transaction data")
    parser.add_argument("--profile", default="bangladesh",
                        help="Country profile (bangladesh, pakistan, india, nigeria, kenya)")
    args = parser.parse_args()
    generate_data(args.profile)

