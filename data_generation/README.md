# Classic Data Generation

This folder contains the original synthetic data generators for the classic churn pipeline.

## Scripts

- `generate_users.py`: creates `data/users.csv`
- `generate_usage_events.py`: creates `data/usage_events.csv` based on hidden engagement archetypes
- `config.py`: shared generation settings such as user count, signup window, channel mix, and country mix

## Run Order

```bash
python data_generation/generate_users.py
python data_generation/generate_usage_events.py
```

These files feed the classic SQL analysis in `sql/` and the classic model artifacts created by `src/models/train_xgboost.py`.
