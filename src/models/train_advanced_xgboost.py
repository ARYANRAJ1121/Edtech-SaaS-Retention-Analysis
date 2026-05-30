import pickle
from pathlib import Path
import sqlite3
import sys

import numpy as np
import pandas as pd
import shap
import xgboost as xgb
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.project_paths import advanced_data_path, artifacts_path


FEATURE_COLUMNS = [
    "days_since_last_activity",
    "engagement_velocity",
    "frustration_index",
    "completion_ratio",
    "total_events",
    "mrr",
]


def train_advanced_model():
    print("Initializing MAARS AI engine...")

    data_file = advanced_data_path("advanced_features.csv")
    if not data_file.exists():
        print(f"Error: {data_file} not found. Run src/data/generate_telemetry.py first.")
        return

    df = pd.read_csv(data_file)
    X = df[FEATURE_COLUMNS]
    y = df["churned"]

    print("Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    print("Training XGBoost classifier on advanced telemetry...")
    scale_pos_weight = (len(y_train) - sum(y_train)) / sum(y_train)
    model = xgb.XGBClassifier(
        n_estimators=300,
        learning_rate=0.03,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=scale_pos_weight,
        eval_metric="auc",
        random_state=42,
    )
    model.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_pred_proba)
    print(f"ROC-AUC Score: {auc:.4f}")

    print("Computing SHAP values...")
    explainer = shap.TreeExplainer(model)

    artifacts_path().mkdir(parents=True, exist_ok=True)
    with artifacts_path("maars_model.pkl").open("wb") as model_file:
        pickle.dump(model, model_file)
    with artifacts_path("maars_explainer.pkl").open("wb") as explainer_file:
        pickle.dump(explainer, explainer_file)

    print("Generating scored MAARS dataset...")
    df["risk_score"] = model.predict_proba(X)[:, 1]
    shap_values = explainer.shap_values(X)

    top_reasons = []
    for row in shap_values:
        top_feature_index = int(np.argmax(row))
        if row[top_feature_index] > 0:
            top_reasons.append(FEATURE_COLUMNS[top_feature_index])
        else:
            top_reasons.append("Stable Activity")

    df["primary_churn_driver"] = top_reasons

    scored_output = advanced_data_path("scored_users.csv")
    df.to_csv(scored_output, index=False)

    db_path = advanced_data_path("telemetry.db")
    with sqlite3.connect(db_path) as conn:
        df.to_sql("scored_users", conn, if_exists="replace", index=False)

    print("MAARS engine training complete.")


if __name__ == "__main__":
    train_advanced_model()
