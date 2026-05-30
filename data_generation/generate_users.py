from pathlib import Path

import numpy as np
import pandas as pd

from config import (
    ACQUISITION_CHANNELS,
    COUNTRIES,
    DAYS_SPAN,
    NUM_USERS,
    RANDOM_SEED,
    START_DATE,
)


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = BASE_DIR.parent / "data" / "users.csv"

np.random.seed(RANDOM_SEED)
start_date = pd.to_datetime(START_DATE)

user_ids = np.arange(1, NUM_USERS + 1)
signup_dates = start_date + pd.to_timedelta(np.random.randint(0, DAYS_SPAN, size=NUM_USERS), unit="D")

acquisition_channel = np.random.choice(
    list(ACQUISITION_CHANNELS.keys()),
    size=NUM_USERS,
    p=list(ACQUISITION_CHANNELS.values()),
)

country = np.random.choice(
    list(COUNTRIES.keys()),
    size=NUM_USERS,
    p=list(COUNTRIES.values()),
)

users_df = pd.DataFrame(
    {
        "user_id": user_ids,
        "signup_date": signup_dates,
        "acquisition_channel": acquisition_channel,
        "country": country,
    }
)

users_df = users_df.sort_values("signup_date").reset_index(drop=True)
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
users_df.to_csv(OUTPUT_PATH, index=False)

print(f"Users generated: {users_df.shape}")
