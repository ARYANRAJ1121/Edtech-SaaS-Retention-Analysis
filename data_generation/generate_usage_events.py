from pathlib import Path

import numpy as np
import pandas as pd

from config import RANDOM_SEED


BASE_DIR = Path(__file__).resolve().parent
USERS_PATH = BASE_DIR.parent / "data" / "users.csv"
OUTPUT_PATH = BASE_DIR.parent / "data" / "usage_events.csv"

np.random.seed(RANDOM_SEED)

users = pd.read_csv(USERS_PATH, parse_dates=["signup_date"])
end_date = users["signup_date"].max() + pd.Timedelta(days=90)

archetypes = np.random.choice(["low", "medium", "power"], size=len(users), p=[0.4, 0.4, 0.2])
users["archetype"] = archetypes

usage_rows = []

for _, row in users.iterrows():
    user_id = row["user_id"]
    signup_date = row["signup_date"]
    archetype = row["archetype"]

    days_active = (end_date - signup_date).days

    if archetype == "low":
        base_lambda = 0.8
        decay = 0.015
    elif archetype == "medium":
        base_lambda = 1.8
        decay = 0.007
    else:
        base_lambda = 3.0
        decay = 0.003

    for day in range(days_active):
        event_date = signup_date + pd.Timedelta(days=day)
        effective_lambda = base_lambda * np.exp(-decay * day)
        sessions = np.random.poisson(effective_lambda)

        if sessions > 0:
            usage_rows.append(
                {
                    "user_id": user_id,
                    "event_date": event_date,
                    "sessions": sessions,
                }
            )

usage_df = pd.DataFrame(usage_rows)
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
usage_df.to_csv(OUTPUT_PATH, index=False)

print("Usage events generated:", usage_df.shape)
