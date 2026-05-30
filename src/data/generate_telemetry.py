import random
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import sys

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.project_paths import advanced_data_path


def generate_data():
    print("Initializing advanced telemetry generation...")
    np.random.seed(42)
    random.seed(42)

    num_users = 2500
    user_ids = range(1, num_users + 1)
    signup_dates = [datetime(2025, 1, 1) + timedelta(days=random.randint(0, 180)) for _ in range(num_users)]
    cohorts = np.random.choice(["Power", "Struggling", "Casual"], size=num_users, p=[0.2, 0.3, 0.5])

    users_df = pd.DataFrame(
        {
            "user_id": user_ids,
            "signup_date": signup_dates,
            "cohort": cohorts,
            "mrr": np.random.choice([29, 99, 299], size=num_users, p=[0.6, 0.3, 0.1]),
        }
    )

    print("Simulating detailed event streams...")
    events = []

    for _, user in users_df.iterrows():
        uid = user["user_id"]
        cohort = user["cohort"]
        start_date = user["signup_date"]

        if cohort == "Struggling":
            will_churn = np.random.choice([True, False], p=[0.7, 0.3])
        elif cohort == "Casual":
            will_churn = np.random.choice([True, False], p=[0.4, 0.6])
        else:
            will_churn = np.random.choice([True, False], p=[0.1, 0.9])

        users_df.loc[users_df["user_id"] == uid, "will_churn"] = will_churn

        max_days = (datetime(2025, 12, 31) - start_date).days
        if will_churn:
            active_days = random.randint(5, max_days // 2)
        else:
            active_days = random.randint(max_days // 2, max_days)

        current_date = start_date

        for day in range(active_days):
            current_date += timedelta(days=1)
            login_prob = 0.8 if cohort == "Power" else (0.4 if cohort == "Casual" else 0.5)

            if will_churn and day > (active_days - 14):
                login_prob *= 0.2

            if random.random() < login_prob:
                events.append(
                    {
                        "user_id": uid,
                        "timestamp": current_date + timedelta(hours=random.randint(8, 20)),
                        "event_type": "login",
                        "metadata": "",
                    }
                )

                num_sessions = random.randint(2, 10) if cohort == "Power" else random.randint(1, 4)

                for _ in range(num_sessions):
                    event_type = random.choice(["video_play", "quiz_start"])
                    events.append(
                        {
                            "user_id": uid,
                            "timestamp": current_date
                            + timedelta(hours=random.randint(8, 20), minutes=random.randint(0, 59)),
                            "event_type": event_type,
                            "metadata": "",
                        }
                    )

                    if event_type == "video_play" and random.random() < 0.2:
                        events.append(
                            {
                                "user_id": uid,
                                "timestamp": current_date
                                + timedelta(hours=random.randint(8, 20), minutes=random.randint(0, 59)),
                                "event_type": "video_pause",
                                "metadata": "complex_topic",
                            }
                        )

                    if event_type == "quiz_start":
                        fail_prob = 0.6 if cohort == "Struggling" else 0.1
                        if random.random() < fail_prob:
                            events.append(
                                {
                                    "user_id": uid,
                                    "timestamp": current_date
                                    + timedelta(hours=random.randint(8, 20), minutes=random.randint(0, 59)),
                                    "event_type": "quiz_failed",
                                    "metadata": "score < 50",
                                }
                            )
                            if random.random() < 0.3:
                                events.append(
                                    {
                                        "user_id": uid,
                                        "timestamp": current_date
                                        + timedelta(hours=random.randint(8, 20), minutes=random.randint(0, 59)),
                                        "event_type": "rage_click",
                                        "metadata": "submit_button",
                                    }
                                )
                        else:
                            events.append(
                                {
                                    "user_id": uid,
                                    "timestamp": current_date
                                    + timedelta(hours=random.randint(8, 20), minutes=random.randint(0, 59)),
                                    "event_type": "quiz_passed",
                                    "metadata": "score > 80",
                                }
                            )

    events_df = pd.DataFrame(events)

    print("Engineering advanced behavioral features...")
    features = []
    analysis_date = datetime(2025, 12, 31)
    user_mrr = users_df.set_index("user_id")["mrr"].to_dict()
    user_churn = users_df.set_index("user_id")["will_churn"].to_dict()

    for uid in user_ids:
        user_events = events_df[events_df["user_id"] == uid]
        if user_events.empty:
            continue

        last_active = user_events["timestamp"].max()
        days_since_last = (analysis_date - last_active).days

        last_14_days = user_events[user_events["timestamp"] > (last_active - timedelta(days=14))]
        prior_14_days = user_events[
            (user_events["timestamp"] <= (last_active - timedelta(days=14)))
            & (user_events["timestamp"] > (last_active - timedelta(days=28)))
        ]

        events_last_14 = len(last_14_days)
        events_prior_14 = len(prior_14_days)
        engagement_velocity = (events_last_14 + 1) / (events_prior_14 + 1)

        rage_clicks = len(user_events[user_events["event_type"] == "rage_click"])
        quiz_fails = len(user_events[user_events["event_type"] == "quiz_failed"])
        frustration_index = (rage_clicks * 2) + quiz_fails

        videos = len(user_events[user_events["event_type"] == "video_play"])
        quizzes = len(user_events[user_events["event_type"] == "quiz_passed"])
        completion_ratio = quizzes / (videos + 1)

        features.append(
            {
                "user_id": uid,
                "days_since_last_activity": days_since_last,
                "engagement_velocity": engagement_velocity,
                "frustration_index": frustration_index,
                "completion_ratio": completion_ratio,
                "total_events": len(user_events),
                "mrr": user_mrr[uid],
                "churned": 1 if user_churn[uid] else 0,
            }
        )

    features_df = pd.DataFrame(features)

    print("Saving advanced telemetry assets...")
    advanced_data_path().mkdir(parents=True, exist_ok=True)
    features_df.to_csv(advanced_data_path("advanced_features.csv"), index=False)

    with sqlite3.connect(advanced_data_path("telemetry.db")) as conn:
        users_df.to_sql("users", conn, if_exists="replace", index=False)
        events_df.to_sql("events", conn, if_exists="replace", index=False)
        features_df.to_sql("features", conn, if_exists="replace", index=False)

    print("Advanced telemetry generation complete.")


if __name__ == "__main__":
    generate_data()
