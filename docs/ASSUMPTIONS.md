# Assumptions

## Product Assumptions

- The product is an EdTech subscription business where engagement patterns are meaningful leading indicators of churn.
- Customer success capacity is limited, so prioritization matters more than perfect labels.
- Monthly recurring revenue (`mrr`) is a useful proxy for account value in the advanced MAARS flow.

## Data Assumptions

- The classic pipeline uses synthetic user and session data generated locally.
- The advanced MAARS pipeline uses fully synthetic telemetry with simulated cohorts and struggle patterns.
- The advanced feature store excludes users with no generated events, so downstream dashboards and APIs only operate on users present in `advanced_features.csv`.

## Modeling Assumptions

- Risk scores are treated as prioritization signals, not guarantees of future churn.
- SHAP is used as an explanation layer for local user-level drivers.
- In the MAARS simulation, advanced labels come from generator logic rather than a production churn table.
