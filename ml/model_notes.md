Churn Risk Scoring — Model Notes
1. Problem Definition

The goal of this model is not to predict churn after it happens, but to identify users who are at risk of churning soon, so that the business can intervene proactively.

Churn is costly, but intervention resources (emails, discounts, outreach) are limited.
Therefore, the objective is risk prioritization, not perfect classification.

2. Churn Definition (Ground Truth)

A user is labeled as churned if they exhibit no activity for 28 consecutive days following an active session.

Why 28 days?

Aligns with monthly subscription and learning cycles

Avoids misclassifying short breaks or weekends as churn

Common industry heuristic for consumer SaaS and EdTech

This churn definition is derived purely from behavioral data using SQL window functions, not arbitrary labels.

3. Feature Engineering (SQL → ML Handoff)

All features are engineered in PostgreSQL before modeling to ensure:

Transparency

Reproducibility

Clear separation between data logic and ML logic

Final features used:

days_since_last_activity
Measures recency. Strong indicator of disengagement.

active_days
Measures user tenure and habit formation. Longer-tenured users are typically more stable.

avg_sessions_per_day
Measures engagement intensity. Captures how embedded the product is in the user’s routine.

Features such as total_sessions were intentionally excluded due to multicollinearity, as they are redundant with active_days and avg_sessions_per_day.

4. Model Choice

Logistic Regression was selected deliberately.

Why not complex models (XGBoost, Random Forests)?

Dataset is relatively small (~1500 users)

Business stakeholders require interpretability

Coefficient direction and magnitude matter for decision-making

Logistic regression provides:

Probabilistic outputs (risk scores)

Clear feature influence

Stable behavior under limited data

5. Handling Class Imbalance

Churned users represent ~13–14% of the dataset.

To account for this:

class_weight="balanced" was used

Evaluation focused on recall and ROC-AUC, not accuracy

Why recall matters more than precision:

Missing a true churner is more costly than contacting a non-churner

False positives result in low-cost interventions (emails, nudges)

False negatives result in lost users

6. Model Performance

ROC AUC ≈ 0.85
Indicates strong ranking ability — the model can reliably distinguish higher-risk users from lower-risk ones.

High recall for churned users
Confirms the model successfully captures disengagement patterns.

Accuracy is intentionally not emphasized, as it is misleading in imbalanced churn problems.

7. Coefficient Interpretation (Business Meaning)

After standardization and removal of redundant features, coefficients align with domain logic:

days_since_last_activity (positive)
Longer inactivity increases churn risk.

active_days (negative)
Longer tenure reduces churn risk due to habit formation.

avg_sessions_per_day (strong negative)
High daily engagement is the strongest protective factor against churn.

This confirms that the model is not only predictive, but conceptually sound.

8. Churn Risk Score

The churn risk score is the predicted probability that a user will churn, given their current behavior.

It is used to:

Rank users by risk

Prioritize intervention

Allocate retention resources efficiently

It is not a guarantee of churn, but a decision-support signal.

9. Business Application

Typical usage:

Top 5–10% highest risk users → proactive outreach

Medium risk → automated nudges or reminders

Low risk → no action

This enables a shift from reactive churn analysis to proactive retention strategy.

10. Summary

This project demonstrates:

Behavioral churn definition using SQL

Feature engineering grounded in product usage

Interpretable ML for risk prioritization

Clear separation between analytics and modeling

Business-aligned decision-making

The model is designed to be useful, not just accurate.