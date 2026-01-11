📊 EdTech SaaS Retention & Churn Risk Analysis
Overview

User churn in EdTech SaaS platforms rarely happens abruptly — it is usually preceded by gradual disengagement.
The real challenge is not identifying users who have already churned, but detecting early churn risk while intervention is still possible.

This project builds an end-to-end retention intelligence system that combines:

Behavioral analytics using PostgreSQL & SQL

Feature engineering grounded in user activity

Interpretable machine learning–based churn risk scoring

The final output enables proactive retention decision-making, not just retrospective reporting.

Business Problem

Traditional analytics typically answers:

Who churned last month?

What is the overall churn rate?

These insights are reactive and often arrive too late.

This project focuses on a more actionable question:

Which current users are most likely to churn soon, and should be prioritized for retention efforts today?

Dataset & Simulation

To mirror real SaaS constraints while maintaining reproducibility, user behavior was simulated programmatically.

Users: 1,500

Usage events: 136,000+

Time span: ~9 months of activity

Behavioral realism:

Irregular usage patterns

Engagement decay

Long-tail inactivity

All data generation logic is deterministic and documented.

Churn Definition

A user is labeled as churned if they exhibit no activity for 28 consecutive days.

Why 28 days?

Aligns with monthly learning and subscription cycles

Avoids misclassifying short breaks as churn

Common heuristic in consumer SaaS and EdTech

The churn label is derived purely from behavioral data using SQL window functions — no manual tagging or assumptions.

Technical Architecture
Python (Data Generation)
        ↓
PostgreSQL + SQL (Analytics & Features)
        ↓
Machine Learning (Churn Risk Scoring)
        ↓
CSV Output for Business Use

1. Data Generation (Python)

Synthetic but realistic user and usage data

Time-aware simulation

Reproducible via fixed random seeds

2. Analytics & Feature Engineering (PostgreSQL)

Cohort retention analysis

Engagement and recency metrics

Leakage-free feature computation using SQL

3. Machine Learning (scikit-learn)

Logistic regression for interpretability

Class imbalance handling

Risk probabilities instead of hard labels

Why Machine Learning?

SQL is excellent for:

Describing past behavior

Defining churn

Measuring engagement

However, SQL alone cannot:

Rank active users by future churn risk

Combine multiple weak behavioral signals

Produce a single actionable prioritization score

Machine learning bridges this gap by converting behavioral signals into a churn risk score — a probability that a user is likely to churn in the near future.

Model Output

The final output is a user-level churn risk dataset, including:

Engagement metrics

Recency and tenure signals

Predicted churn probability

Binary churn label (for validation)

This output can be directly consumed by:

Retention teams

Marketing automation

Experimentation pipelines (A/B testing)

Results (High-Level)

Churn rate: ~13–14%

ROC-AUC: ~0.85

High recall for churned users, prioritizing early detection

Model behavior aligns with domain intuition:

Longer inactivity → higher churn risk

Strong daily engagement → lower churn risk

Detailed modeling rationale is documented in ml/model_notes.md.

Repository Structure
Edtech-SaaS-Retention-Analysis/
│
├── data/                 # Final CSV datasets
├── data_generation/      # Python data simulation
├── sql/                  # Schema, loading, analytics queries
├── ml/                   # ML pipeline, notebooks, model notes
├── docs/                 # Assumptions & business context
├── requirements.txt
└── README.md

Key Takeaways

Retention problems are prediction + prioritization problems, not just reporting problems

Interpretable ML often outperforms complex models in business settings

Clean SQL → ML handoffs are critical in real analytics systems

Churn risk scores enable proactive, not reactive, retention strategies

Next Extensions

Possible future improvements:

Pricing and plan-level features

Content-level engagement signals

Rolling-window retraining

Intervention effectiveness via A/B testing

Aryan Raj
Computer Science Undergraduate | Data Analytics & Applied ML
Focused on building business-aligned analytics systems
