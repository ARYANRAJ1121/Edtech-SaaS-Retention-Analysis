# Churn Risk Scoring (Machine Learning)

## Purpose

The goal of the ML component is to **augment SQL-based retention analytics** by assigning a **churn risk score** to each user.

Rather than predicting churn after it occurs, the model estimates the **probability that a user will churn in the near future**, enabling proactive prioritization.

This module intentionally focuses on **interpretability and decision support**, not model complexity.

---

## Why Machine Learning Here?

SQL is used to:
- Define churn objectively
- Engineer behavioral features
- Explain historical patterns

However, SQL alone cannot:
- Combine multiple weak behavioral signals
- Rank active users by future churn likelihood
- Produce a single, actionable prioritization metric

Machine learning bridges this gap by converting engagement, recency, and tenure signals into a **churn risk probability**.

---

## Feature Inputs

Features are engineered upstream in PostgreSQL to ensure transparency and reproducibility.

Final features used:

- **days_since_last_activity**  
  Measures recency and disengagement.

- **active_days**  
  Captures tenure and habit formation.

- **avg_sessions_per_day**  
  Measures engagement intensity.

Redundant features (e.g., total sessions) were excluded to reduce multicollinearity.

---

## Model Choice

**Logistic Regression** was selected deliberately.

Reasons:
- Dataset size is moderate
- Stakeholders require interpretability
- Coefficient direction and magnitude must be explainable
- Probabilistic outputs are required for prioritization

This aligns with real-world retention systems where transparency is preferred over black-box performance.

---

## Handling Class Imbalance

Churned users represent a minority of the dataset.

Mitigation strategy:
- `class_weight="balanced"`
- Evaluation focused on **ROC-AUC** and **recall for churned users**

Accuracy is intentionally de-emphasized, as it is misleading in imbalanced churn problems.

---

## Output

The model outputs:
- **Churn probability (risk score)** per user
- Binary churn label (for validation only)

The final dataset is exported as:
# Churn Risk Scoring (Machine Learning)

## Purpose

The goal of the ML component is to **augment SQL-based retention analytics** by assigning a **churn risk score** to each user.

Rather than predicting churn after it occurs, the model estimates the **probability that a user will churn in the near future**, enabling proactive prioritization.

This module intentionally focuses on **interpretability and decision support**, not model complexity.

---

## Why Machine Learning Here?

SQL is used to:
- Define churn objectively
- Engineer behavioral features
- Explain historical patterns

However, SQL alone cannot:
- Combine multiple weak behavioral signals
- Rank active users by future churn likelihood
- Produce a single, actionable prioritization metric

Machine learning bridges this gap by converting engagement, recency, and tenure signals into a **churn risk probability**.

---

## Feature Inputs

Features are engineered upstream in PostgreSQL to ensure transparency and reproducibility.

Final features used:

- **days_since_last_activity**  
  Measures recency and disengagement.

- **active_days**  
  Captures tenure and habit formation.

- **avg_sessions_per_day**  
  Measures engagement intensity.

Redundant features (e.g., total sessions) were excluded to reduce multicollinearity.

---

## Model Choice

**Logistic Regression** was selected deliberately.

Reasons:
- Dataset size is moderate
- Stakeholders require interpretability
- Coefficient direction and magnitude must be explainable
- Probabilistic outputs are required for prioritization

This aligns with real-world retention systems where transparency is preferred over black-box performance.

---

## Handling Class Imbalance

Churned users represent a minority of the dataset.

Mitigation strategy:
- `class_weight="balanced"`
- Evaluation focused on **ROC-AUC** and **recall for churned users**

Accuracy is intentionally de-emphasized, as it is misleading in imbalanced churn problems.

---

## Output

The model outputs:
- **Churn probability (risk score)** per user
- Binary churn label (for validation only)

The final dataset is exported as:
data/churn_risk_scored_users.csv

This output is designed to be consumed by:
- Retention teams
- Marketing automation
- Experimentation pipelines

---

## Evaluation Summary

- ROC-AUC ≈ 0.85
- High recall for churned users
- Feature coefficients align with domain intuition

Detailed interpretation and design rationale are documented in `model_notes.md`.

---

## Files

- `risk_scoring.ipynb` — End-to-end modeling pipeline
- `model_notes.md` — Design decisions and trade-offs
- `feature_table.sql` — Feature extraction logic (SQL)

---

## Key Takeaway

The ML component is not a standalone model — it is a **decision-support layer** built on top of robust SQL analytics, designed to enable proactive retention actions.
