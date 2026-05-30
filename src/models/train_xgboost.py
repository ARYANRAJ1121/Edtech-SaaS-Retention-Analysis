import pickle
from pathlib import Path
import sys

import numpy as np
import pandas as pd
import shap
import xgboost as xgb
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.project_paths import artifacts_path, data_path


FEATURE_COLUMNS = [
    "active_days",
    "days_since_last_activity",
    "avg_sessions_per_day",
    "total_sessions",
]


def train_and_evaluate():
    print("Loading classic churn dataset...")
    dataset_path = data_path("churn_ml_dataset.csv")
    df = pd.read_csv(dataset_path)

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

    print("Training XGBoost classifier...")
    scale_pos_weight = (len(y_train) - sum(y_train)) / sum(y_train)

    model = xgb.XGBClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=4,
        scale_pos_weight=scale_pos_weight,
        eval_metric="auc",
        random_state=42,
    )
    model.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    y_pred = model.predict(X_test)

    auc = roc_auc_score(y_test, y_pred_proba)
    print(f"ROC-AUC Score: {auc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    print("Computing SHAP values...")
    explainer = shap.TreeExplainer(model)

    artifacts_path().mkdir(parents=True, exist_ok=True)
    print("Saving model artifacts...")
    with artifacts_path("xgboost_model.pkl").open("wb") as model_file:
        pickle.dump(model, model_file)
    with artifacts_path("shap_explainer.pkl").open("wb") as explainer_file:
        pickle.dump(explainer, explainer_file)

    print("Generating scored classic dataset...")
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

    canonical_output = data_path("churn_risk_scored_users.csv")
    compatibility_output = data_path("churn_risk_scored_users_v2.csv")
    df.to_csv(canonical_output, index=False)
    df.to_csv(compatibility_output, index=False)

    print(
        "Training complete. Saved artifacts and refreshed "
        "data/churn_risk_scored_users.csv."
    )


if __name__ == "__main__":
    train_and_evaluate()
