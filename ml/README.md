# ML Notes

The `ml/` folder captures the earlier notebook-based version of the project.

## What Lives Here

- `risk_scoring.ipynb`: the original end-to-end exploratory notebook
- `model_notes.md`: business and modeling rationale for the baseline approach
- `feature_table.sql`: the SQL query used to create the classic ML-ready table

## How It Relates To `src/models/`

There are now two layers in the repo:

- `ml/`: historical baseline and exploratory work
- `src/models/`: current runnable training scripts used by the dashboards and API

The notebook-era materials focus on a highly interpretable retention-scoring baseline. The current runnable scripts use XGBoost plus SHAP for both the classic and MAARS flows.
