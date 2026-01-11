# 📊 Early Churn Risk Detection in an EdTech SaaS

> **From raw usage events → churn risk scores → retention decisions**

This project builds an **end-to-end retention intelligence system** for an EdTech SaaS platform.  
It combines **SQL-based behavioral analytics** with **interpretable machine learning** to proactively identify users at risk of churn.

Instead of asking *“Who churned last month?”*, this system answers:

> **“Which users are most likely to churn next — and should be prioritized today?”**

---

## 🚀 At a Glance

| Metric | Value |
|------|------|
| Users | 1,500 |
| Usage Events | 136,000+ |
| Time Span | ~9 months |
| Observed Churn Rate | ~13.5% |
| ML Model | Logistic Regression |
| ROC-AUC | **~0.85** |
| Output | User-level churn risk scores |

📌 **Final Deliverable:**  
A ranked list of users by churn risk probability — ready for retention action.

---

## 🧠 Why This Project Exists

Most churn analytics are **reactive**:
- Monthly churn rate
- Users who already left
- Lagging indicators

In real SaaS teams, the real problem is **prioritization**:

> Retention teams can’t act on everyone —  
> **so who should they focus on first?**

This project addresses that gap by:
- Defining churn rigorously using SQL
- Engineering behavioral features at scale
- Using ML only where it adds real value: **risk ranking**

---

## 🧩 System Architecture

# 📊 Early Churn Risk Detection in an EdTech SaaS

> **From raw usage events → churn risk scores → retention decisions**

This project builds an **end-to-end retention intelligence system** for an EdTech SaaS platform.  
It combines **SQL-based behavioral analytics** with **interpretable machine learning** to proactively identify users at risk of churn.

Instead of asking *“Who churned last month?”*, this system answers:

> **“Which users are most likely to churn next — and should be prioritized today?”**

---

## 🚀 At a Glance

| Metric | Value |
|------|------|
| Users | 1,500 |
| Usage Events | 136,000+ |
| Time Span | ~9 months |
| Observed Churn Rate | ~13.5% |
| ML Model | Logistic Regression |
| ROC-AUC | **~0.85** |
| Output | User-level churn risk scores |

📌 **Final Deliverable:**  
A ranked list of users by churn risk probability — ready for retention action.

---

## 🧠 Why This Project Exists

Most churn analytics are **reactive**:
- Monthly churn rate
- Users who already left
- Lagging indicators

In real SaaS teams, the real problem is **prioritization**:

> Retention teams can’t act on everyone —  
> **so who should they focus on first?**

This project addresses that gap by:
- Defining churn rigorously using SQL
- Engineering behavioral features at scale
- Using ML only where it adds real value: **risk ranking**

---

## 🧩 System Architecture

Python (Data Simulation)
↓
PostgreSQL (SQL Analytics & Feature Engineering)
↓
Machine Learning (Churn Risk Scoring)
↓
CSV Output → Retention / Marketing Teams


SQL owns the business logic.  
ML augments it with prioritization.

---

## 📂 Dataset Overview

Synthetic but **behaviorally realistic** data was generated to mimic a real EdTech SaaS.

| Component | Description |
|--------|------------|
| Users | Signup date, acquisition channel, country |
| Usage Events | Daily session counts per user |
| Behavior | Engagement decay, inactivity gaps |
| Reproducibility | Fully deterministic via Python |

---

## 🔍 Churn Definition

A user is labeled as **churned** if they have **no activity for 30 consecutive days**.

Why 30 days?
- Aligns with monthly learning cycles
- Avoids misclassifying short breaks
- Common heuristic in consumer SaaS

Churn labels are derived **purely via SQL window functions** — no manual tagging.

---

## 📐 SQL Analytics & Feature Engineering (Core Layer)

PostgreSQL is used as the **primary analytics engine**.

All business logic is consolidated in:


### What the SQL pipeline does:
- User activity lifecycle analysis
- Retention & engagement profiling
- Leakage-free churn definition
- ML-ready feature engineering

### Key features engineered in SQL:
- `active_days` — tenure & habit strength  
- `days_since_last_activity` — disengagement signal  
- `avg_sessions_per_day` — engagement intensity  
- `total_sessions` — cumulative usage  

This mirrors how real analytics teams prepare data for ML.

---

## 🤖 Machine Learning: Churn Risk Scoring

### Why ML?
SQL explains *what happened*.  
ML estimates *what is likely to happen next*.

The model converts behavioral signals into a **churn risk probability** for each user.

### Model Choice
- **Logistic Regression**
- Interpretable coefficients
- Probabilistic output
- Business-aligned decision support

Complex models were intentionally avoided in favor of **trust and explainability**.

---

## 📊 Model Performance

| Metric | Value |
|------|------|
| ROC-AUC | **~0.85** |
| Recall (Churned Users) | High |
| Accuracy | De-emphasized (class imbalance) |

The model prioritizes **early detection of at-risk users**.

---

## 🧮 What Is a Churn Risk Score?

A churn risk score represents:

> **The probability that a user will churn in the near future, given current behavior.**

Example:

| User | Risk Score | Interpretation |
|----|-----------|--------------|
| User A | 0.12 | Low risk |
| User B | 0.47 | Medium risk |
| User C | 0.81 | High risk |

---

## 🏢 Real-World Retention Example

If a retention team can act on only **10% of users**:

| User ID | Risk Score | Action |
|------|-----------|--------|
| 1489 | 0.82 | Personal outreach |
| 652 | 0.74 | Discount / reminder |
| 951 | 0.61 | Engagement nudge |
| 1272 | 0.08 | No action |

This turns analytics into **prioritized, actionable decisions**.

---

## 📁 Repository Structure
Edtech-SaaS-Retention-Analysis/
│
├── data/ # Final CSV outputs
├── data_generation/ # Synthetic data simulation
├── sql/ # Schema, ingestion & analytics
├── ml/ # ML pipeline & model notes
├── docs/ # Assumptions & business context
└── README.md

---

## 🧠 Key Takeaways

- Churn is a **prediction + prioritization** problem
- SQL should own business logic and feature engineering
- ML adds value by ranking risk, not by complexity
- Interpretability beats black-box accuracy in practice

---

## 🔮 Future Extensions

- Pricing / plan-level features
- Content-level engagement signals
- Rolling-window retraining
- Intervention A/B testing

---

## 👤 Author

**Aryan Raj**  
Computer Science Undergraduate | Data Analytics & Applied ML  
Focused on building business-aligned analytics systems
