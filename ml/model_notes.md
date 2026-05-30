# Model Notes

## Purpose

The project is designed to prioritize retention outreach, not to maximize accuracy in isolation. The main output is a churn risk score that helps customer success teams decide where to spend time first.

## Baseline Framing

The original notebook work in `ml/risk_scoring.ipynb` emphasized:

- transparent features derived in SQL
- probabilistic scoring
- business-friendly interpretation
- proactive intervention instead of post-hoc reporting

## Current Runnable Models

The repo now ships two script-driven model paths:

- `src/models/train_xgboost.py`
  Uses the classic feature set: `active_days`, `days_since_last_activity`, `avg_sessions_per_day`, and `total_sessions`.
- `src/models/train_advanced_xgboost.py`
  Uses the advanced telemetry feature set: `days_since_last_activity`, `engagement_velocity`, `frustration_index`, `completion_ratio`, `total_events`, and `mrr`.

Both scripts:

- train an XGBoost classifier
- output probability-based risk scores
- compute SHAP explanations
- export scored datasets for the dashboards

## Business Interpretation

- higher `days_since_last_activity` usually increases risk
- lower `engagement_velocity` suggests recent drop-off
- higher `frustration_index` indicates repeated struggle
- lower completion and lower sustained activity often signal disengagement

The goal is not to prove certainty about churn. The goal is to rank users credibly enough that the next best intervention becomes obvious.
