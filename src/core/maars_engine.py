from __future__ import annotations

import pickle
from typing import Dict, Tuple

import numpy as np
import pandas as pd

from src.utils.project_paths import advanced_data_path, artifacts_path


FEATURE_COLUMNS = [
    "days_since_last_activity",
    "engagement_velocity",
    "frustration_index",
    "completion_ratio",
    "total_events",
    "mrr",
]


def load_model_bundle() -> Tuple[object | None, object | None]:
    model_path = artifacts_path("maars_model.pkl")
    explainer_path = artifacts_path("maars_explainer.pkl")

    if not model_path.exists() or not explainer_path.exists():
        return None, None

    with model_path.open("rb") as model_file:
        model = pickle.load(model_file)
    with explainer_path.open("rb") as explainer_file:
        explainer = pickle.load(explainer_file)

    return model, explainer


def load_feature_store() -> Dict[int, Dict[str, float]]:
    features_path = advanced_data_path("advanced_features.csv")
    if not features_path.exists():
        return {}

    feature_store_df = pd.read_csv(features_path)
    return feature_store_df.set_index("user_id").to_dict(orient="index")


def apply_event_update(user_features: Dict[str, float], event_type: str) -> Dict[str, float]:
    updated_features = dict(user_features)

    if event_type == "quiz_failed":
        updated_features["frustration_index"] += 1
        updated_features["total_events"] += 1

        # Approximate the post-failure completion ratio in the simulation.
        videos = updated_features["total_events"] / 2
        quizzes = max(0, (updated_features["completion_ratio"] * videos) - 1)
        updated_features["completion_ratio"] = quizzes / (videos + 1)
    elif event_type == "rage_click":
        updated_features["frustration_index"] += 2
    elif event_type == "video_pause":
        updated_features["engagement_velocity"] *= 0.95

    updated_features["days_since_last_activity"] = 0
    return updated_features


def score_user(model: object, explainer: object, user_features: Dict[str, float]) -> Tuple[float, str]:
    x_input = pd.DataFrame([user_features])[FEATURE_COLUMNS]
    risk_score = float(model.predict_proba(x_input)[0][1])

    shap_values = explainer.shap_values(x_input)
    shap_row = shap_values[0] if getattr(shap_values, "ndim", 1) > 1 else shap_values
    top_feature_index = int(np.argmax(shap_row))
    primary_driver = FEATURE_COLUMNS[top_feature_index] if shap_row[top_feature_index] > 0 else "Stable"

    return risk_score, primary_driver


def process_event(
    *,
    feature_store: Dict[int, Dict[str, float]],
    model: object | None,
    explainer: object | None,
    user_id: int,
    event_type: str,
    metadata: str = "",
    rag_agent=None,
    threshold: float = 0.65,
) -> Dict[str, object]:
    if user_id not in feature_store:
        raise KeyError(user_id)

    updated_features = apply_event_update(feature_store[user_id], event_type)
    feature_store[user_id] = updated_features

    if model is None or explainer is None:
        return {
            "user_id": user_id,
            "new_risk_score": 0.0,
            "primary_driver": "Model Offline",
            "action_taken": "None",
            "interventionable_content": "Train the advanced model first.",
        }

    risk_score, primary_driver = score_user(model, explainer, updated_features)

    action_taken = "Logged event. No immediate action required."
    interventionable_content = "None"

    if risk_score > threshold and event_type in {"quiz_failed", "video_pause"}:
        action_taken = f"High risk detected ({risk_score:.1%}). Triggering RAG micro-lesson."
        topic = metadata or "General Concepts"
        if rag_agent is not None:
            interventionable_content = rag_agent.generate_intervention(user_id, topic)
        else:
            interventionable_content = f"User {user_id} needs help with {topic}."

    return {
        "user_id": user_id,
        "new_risk_score": risk_score,
        "primary_driver": primary_driver,
        "action_taken": action_taken,
        "interventionable_content": interventionable_content,
    }
