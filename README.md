# 🎯 Nexus Retention Intelligence

[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Database Engine](https://img.shields.io/badge/SQL-PostgreSQL%20%7C%20SQLite-indigo.svg)](https://www.postgresql.org/)
[![Model Stack](https://img.shields.io/badge/Model-XGBoost%20%7C%20SHAP-darkgreen.svg)](https://xgboost.readthedocs.io/)
[![Framework](https://img.shields.io/badge/UI-Streamlit-ff4b4b.svg)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)

An end-to-end, enterprise-grade B2B EdTech retention analytics platform. It combines synthetic behavioral telemetry simulation, database-level SQL feature engineering, non-linear machine learning risk scoring, Shapley-based risk driver attribution, and real-time agentic interventions using Retrieval-Augmented Generation (RAG).

---

## 🏢 The Business Problem (SaaS Retention ROI)

In software-as-a-service (SaaS) business models, **customer acquisition cost (CAC) is extremely high**. Retaining an active subscriber is up to **5x cheaper** than acquiring a new one. 

In EdTech, students rarely click "cancel" the moment they lose interest; instead, they slowly disengage and enter a phase of **"silent churn."** This project builds a proactive scoring pipeline that flags at-risk accounts based on telemetry logs, allowing customer success teams to execute personalized outreach before the billing cycle terminates.

---

## 📐 System Architecture & Pipelines

The platform operates two distinct processing tracks:

```text
========================================================================================
[1] CLASSIC PIPELINE (Batch Analysis & Outreach)
========================================================================================
Simulate 1.5k Users       SQL Window Functions      Train XGBoost & SHAP     Streamlit Executive
& 136k Session Logs  -->  in PostgreSQL Layer   -->  Model Pipeline       -->  Outreach Dashboard
(generate_telemetry)      (engineered features)     (train_xgboost)          (app.py)

========================================================================================
[2] MAARS PIPELINE (Autonomous Event Streaming & Agentic RAG)
========================================================================================
Simulate Granular        FastAPI Ingestion /       XGBoost Recalculation   Groq Agentic RAG
Telemetry Events    -->  SQLite State Store   -->  & SHAP Attribution  -->  Micro-Lessons Pop-up
(video pauses, clicks)   (server.py / SQLite)      (maars_engine)           (rag_engine)
```

---

## 🛠️ Deep Technical Deep-Dive

### 1. Database-Level Feature Engineering (SQL Layer)
To eliminate latency and scale to millions of records, all core behavioral features are engineered directly within the database index using PostgreSQL window functions:

*   **Behavioral Churn definition**: A user is flagged as `churned = 1` if their sequence of usage events contains a consecutive inactivity gap of **$\ge 28$ days**.
*   **Leakage-Free Temporal Queries**: We utilize `LEAD()` over user partitions to calculate the duration of subsequent login gaps without introducing future look-ahead bias:

```sql
WITH ordered_events AS (
    SELECT
        user_id,
        event_date,
        LEAD(event_date) OVER (
            PARTITION BY user_id
            ORDER BY event_date
        ) AS next_event_date
    FROM usage_events
),
gaps AS (
    SELECT
        user_id,
        next_event_date - event_date AS gap_days
    FROM ordered_events
)
SELECT DISTINCT user_id 
FROM gaps 
WHERE gap_days >= 28;
```

#### Engineered Predictors:
| Predictor Name | Feature Type | Business Rationale |
|---|---|---|
| `active_days` | Frequency | Measures total user tenure and product engagement habit strength. |
| `days_since_last_activity` | Recency | The primary indicator of immediate disengagement. |
| `avg_sessions_per_day` | Intensity | Captures active session density when the user is logged in. |
| `total_sessions` | Volume | Cumulative usage metric reflecting absolute product value consumed. |

---

### 2. Explainable Churn Risk Modeling (ML Layer)
*   **The Baseline**: We established a baseline modeling framework using **Logistic Regression** in our exploratory notebook (`ml/risk_scoring.ipynb`).
*   **The Production Classifier**: We upgraded to **XGBoost** to capture highly complex, non-linear feature interactions natively.
*   **Class Imbalance Handling**: Standard model accuracies are deceptive due to skewed classes (mostly active users, few churners). We resolved this by calculating the inverse class ratio and injecting it into the model using the `scale_pos_weight` hyperparameter, heavily penalizing minority class misclassifications.
*   **Explainable AI (XAI)**: We pack each model with a **SHAP (SHapley Additive exPlanations)** explainer. The system evaluates mathematical contributions for every prediction, tagging the user with a concrete, actionable primary risk driver (e.g. Inactivity vs. Dropping Intensity) instead of a simple probability number.

---

### 3. Real-Time Streaming & AI Agent Layer (MAARS)
*   **FastAPI Real-Time Ingest**: Exposes a `POST /track-event` endpoint to simulate standard streaming pipelines.
*   **Dynamic State Store**: Telemetry events dynamically increment user features (e.g. `quiz_failed` increments a custom `frustration_index`).
*   **Agentic Retrieval-Augmented Generation (RAG)**: If a struggling event triggers a risk score above `65%`, our **TF-IDF + Cosine Similarity** vector DB simulator searches indexed course transcripts, retrieves the most relevant material, and calls the **Groq Llama 3 API** to compile a personalized 3-sentence micro-lesson.

---

## ⚡ Quick Start (One-Click Execution)

We have built a unified pipeline automation controller (`run.py`) to launch all services.

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Credentials
Create a `.env` file in the root directory to store your LLM configuration:
```text
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Run the Automation Menu
Execute this single command to access the interactive CLI command center:
```bash
python run.py
```
From the terminal menu, you can launch:
*   **Option 1**: Run the entire Classic Batch Pipeline and open the Executive Dashboard.
*   **Option 2**: Run the Advanced MAARS Pipeline and open the Command Center.
*   **Option 3**: Launch the Streaming Event RAG Simulator.
*   **Option 4**: Spin up the FastAPI API Ingest endpoint on `localhost:8000`.
