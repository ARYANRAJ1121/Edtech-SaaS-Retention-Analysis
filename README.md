# Nexus Retention Intelligence

Nexus Retention Intelligence is an end-to-end EdTech retention analytics project that combines synthetic product telemetry, SQL-based churn logic, machine learning risk scoring, and lightweight AI-assisted intervention workflows.

The repository is organized around two complementary execution paths:

- `Classic pipeline`: a streamlined churn analytics workflow built on generated user/session data, SQL feature engineering, XGBoost scoring, and a Streamlit dashboard.
- `MAARS pipeline`: an advanced simulation layer with richer telemetry, behavioral features, a scored SQLite warehouse, a Streamlit command center, a live event simulator, and a FastAPI inference API.

## Highlights

- End-to-end churn scoring workflow from synthetic data generation to dashboard consumption
- Two modeling layers: a classic retention-scoring path and a richer event-driven MAARS path
- Explainable predictions using SHAP-based churn driver attribution
- Natural-language SQL exploration through an LLM-assisted analytics agent
- Live event simulation for real-time risk recalculation and intervention triggering
- Streamlit dashboards for both executive analytics and interactive experimentation

## Architecture

### Classic Pipeline

1. Generate synthetic users and usage events
2. Define churn and derive features through SQL
3. Train an XGBoost churn model
4. Export scored users and model artifacts
5. Review results in the classic Streamlit dashboard

### MAARS Pipeline

1. Generate detailed event telemetry and behavioral features
2. Persist feature tables and scored outputs to SQLite and CSV
3. Train the advanced XGBoost model with SHAP explanations
4. Query scored users through the MAARS command center
5. Simulate live events and trigger real-time re-scoring via Streamlit or FastAPI

## Technology Stack

- `Python`
- `Pandas`, `NumPy`
- `XGBoost`
- `SHAP`
- `SQLite`
- `Streamlit`
- `FastAPI`
- `Plotly`
- `Groq API` for optional LLM-assisted features

## Repository Structure

```text
Edtech-SaaS-Retention-Analysis/
|-- app.py                     # Classic Streamlit dashboard
|-- data/                      # Classic and advanced datasets
|-- data_generation/           # Classic synthetic data generators
|-- docs/                      # Assumptions, churn logic, and business notes
|-- ml/                        # Notebook-era baseline references
|-- sql/                       # Classic schema and feature engineering SQL
`-- src/
    |-- agents/                # SQL and retention agent helpers
    |-- api/                   # FastAPI event API and RAG engine
    |-- app/                   # MAARS Streamlit applications
    |-- core/                  # Shared MAARS event-processing logic
    |-- data/                  # Advanced telemetry generator
    |-- models/                # Classic and advanced training scripts
    `-- utils/                 # Shared path and utility helpers
```
## Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file if you want to enable LLM-backed features:

```text
GROQ_API_KEY=your_key_here
```

The project runs without a Groq key, but AI-assisted querying and intervention generation will fall back to offline responses or heuristics.

## Running The Classic Pipeline

### Generate source data

```bash
python data_generation/generate_users.py
python data_generation/generate_usage_events.py
```

### Train and score users

```bash
python src/models/train_xgboost.py
```

### Launch the dashboard

```bash
streamlit run app.py
```

### Primary outputs

- `data/churn_risk_scored_users.csv`
- `src/models/artifacts/xgboost_model.pkl`
- `src/models/artifacts/shap_explainer.pkl`

## Running The MAARS Pipeline

### Generate advanced telemetry

```bash
python src/data/generate_telemetry.py
```

### Train the advanced model

```bash
python src/models/train_advanced_xgboost.py
```

### Launch the MAARS command center

```bash
streamlit run src/app/main.py
```

### Launch the live streaming simulator

```bash
streamlit run src/app/live_dashboard.py
```

### Run the FastAPI event API

```bash
python src/api/server.py
```

### API endpoints

- `GET /health`
- `POST /track-event`

### Primary outputs

- `data/advanced/advanced_features.csv`
- `data/advanced/scored_users.csv`
- `data/advanced/telemetry.db`
- `src/models/artifacts/maars_model.pkl`
- `src/models/artifacts/maars_explainer.pkl`

## Machine Learning Notes

- The classic model scores users using retention-oriented behavioral features such as activity recency, active days, and average session intensity.
- The MAARS model extends this with richer behavioral signals including engagement velocity, frustration, completion behavior, and account value.
- SHAP explanations are generated for both tracks to surface the strongest churn driver for each scored user.

## AI-Assisted Features

When a Groq API key is configured, the project can:

- translate natural-language questions into SQL over the advanced scored-user warehouse
- summarize query results into retention-oriented business insights
- generate lightweight intervention or micro-lesson responses for struggling users

## Project Notes

- The advanced telemetry and churn labels are synthetic by design and intended for demonstration, experimentation, and portfolio use.
- The `ml/` directory contains earlier notebook-oriented work and supporting notes; the actively maintained runtime flows live in `src/`.
- The repository is structured to be executable locally without external infrastructure beyond optional API access for LLM features.
