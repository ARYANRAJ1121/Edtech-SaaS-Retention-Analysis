# Data Generation Logic

## Classic Data Generation

The `data_generation/` folder creates the original synthetic inputs:

- `generate_users.py`
  Generates users with signup dates, acquisition channels, and countries.
- `generate_usage_events.py`
  Assigns each user a hidden engagement archetype and simulates daily session counts with decay over time.

These outputs feed:

- `data/users.csv`
- `data/usage_events.csv`

## Advanced MAARS Telemetry Generation

`src/data/generate_telemetry.py` builds a richer simulation:

- user cohorts: `Power`, `Struggling`, `Casual`
- monetization: random `mrr` tiers
- event stream: login, video, quiz, rage-click, and support-style events
- simulated churn behavior: reduced login probability late in the lifecycle for users marked to churn

Derived advanced features include:

- `days_since_last_activity`
- `engagement_velocity`
- `frustration_index`
- `completion_ratio`
- `total_events`
- `mrr`

The generator writes both flat files and a SQLite warehouse so the MAARS apps can query the same synthetic environment through different interfaces.
