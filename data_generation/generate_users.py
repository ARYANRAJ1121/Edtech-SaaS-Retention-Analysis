import pandas as pd
import numpy as np
from datetime import timedelta

from config import (
    NUM_USERS,
    START_DATE,
    DAYS_SPAN,
    RANDOM_SEED,
    ACQUISITION_CHANNELS,
    COUNTRIES
)

# Reproducibility
np.random.seed(RANDOM_SEED)

start_date = pd.to_datetime(START_DATE)

# User IDs
user_ids = np.arange(1, NUM_USERS + 1)

# Signup dates
signup_dates = start_date + pd.to_timedelta(
    np.random.randint(0, DAYS_SPAN, size=NUM_USERS), unit="D"
)

# Acquisition channels
acquisition_channel = np.random.choice(
    list(ACQUISITION_CHANNELS.keys()),
    size=NUM_USERS,
    p=list(ACQUISITION_CHANNELS.values())
)

# Countries
country = np.random.choice(
    list(COUNTRIES.keys()),
    size=NUM_USERS,
    p=list(COUNTRIES.values())
)

users_df = pd.DataFrame({
    "user_id": user_ids,
    "signup_date": signup_dates,
    "acquisition_channel": acquisition_channel,
    "country": country
})

# Sort for realism
users_df = users_df.sort_values("signup_date").reset_index(drop=True)

# Save CSV
users_df.to_csv("../data/users.csv", index=False)

print(f"Users generated: {users_df.shape}")
