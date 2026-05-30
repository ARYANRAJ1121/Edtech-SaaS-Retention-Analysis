# Business Decisions

## Why The Project Has Two Tracks

- The classic pipeline is simpler and easier to explain end to end.
- The MAARS pipeline demonstrates how the same retention problem could evolve into a richer telemetry and intervention system.

## Why Use Risk Scores

- Retention teams rarely have capacity to contact every at-risk user.
- A ranked list is more actionable than a binary churn label.
- Probability scores support thresholding, triage, and experimentation.

## Why Include SHAP

- Stakeholders need to understand why a user is being prioritized.
- Customer success workflows are easier to trust when the top driver is visible.
- The project aims to bridge analytics and action, not just prediction.

## Why Include LLM Components

- The SQL agent demonstrates natural-language access to the warehouse.
- The retention and RAG agents demonstrate prescriptive next steps after scoring.
- These pieces are intentionally lightweight and portfolio-oriented, not production-hardened orchestration.
