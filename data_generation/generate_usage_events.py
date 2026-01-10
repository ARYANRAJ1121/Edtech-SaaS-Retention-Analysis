import pandas as pd
import numpy as np

from config import RANDOM_SEED

np.random.seed(RANDOM_SEED)

# Load users
users = pd.read_csv("../data/users.csv", parse_dates=["signup_date"])

END_DATE = users["signup_date"].max() + pd.Timedelta(days=90)

# Assign hidden engagement archetypes
archetypes = np.random.choice(
    ["low", "medium", "power"],
    size=len(users),
    p=[0.4, 0.4, 0.2]
)

users["archetype"] = archetypes

usage_rows = []

for _, row in users.iterrows():
    user_id = row["user_id"]
    signup_date = row["signup_date"]
    archetype = row["archetype"]

    days_active = (END_DATE - signup_date).days

    if archetype == "low":
        base_lambda = 0.8
        decay = 0.015
    elif archetype == "medium":
        base_lambda = 1.8
        decay = 0.007
    else:  # power
        base_lambda = 3.0
        decay = 0.003

    for day in range(days_active):
        event_date = signup_date + pd.Timedelta(days=day)

        effective_lambda = base_lambda * np.exp(-decay * day)

        sessions = np.random.poisson(effective_lambda)

        if sessions > 0:
            usage_rows.append({
                "user_id": user_id,
                "event_date": event_date,
                "sessions": sessions
            })

usage_df = pd.DataFrame(usage_rows)

usage_df.to_csv("../data/usage_events.csv", index=False)

print("Usage events generated:", usage_df.shape)
