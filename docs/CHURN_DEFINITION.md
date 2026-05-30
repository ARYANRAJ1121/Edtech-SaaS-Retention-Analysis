# Churn Definition

This repo uses two different label strategies because it contains two different pipelines.

## Classic Pipeline

The classic SQL workflow defines churn behaviorally:

- reference date: the latest activity date in `usage_events`
- churn rule: user is churned when `days_since_last_activity >= 30`

This logic is implemented in:

- `sql/analysis/02_churn_definition.sql`
- `sql/analysis/03_feature_engineering.sql`

## Advanced MAARS Pipeline

The MAARS simulation generates a latent `will_churn` flag during synthetic data creation:

- struggling cohorts churn more often
- casual cohorts churn at moderate rates
- power cohorts churn least often
- users marked to churn experience a sharp engagement drop near the end of their simulated lifespan

That generated label becomes the `churned` target used in `data/advanced/advanced_features.csv`.

## Practical Meaning

- The classic flow is closer to an analytics definition based on inactivity.
- The advanced flow is closer to a simulation environment for event-driven intervention and richer features.
