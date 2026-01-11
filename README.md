# 📊 Early Churn Risk Detection in an EdTech SaaS

> **From raw usage events → churn risk scores → retention decisions**

This project builds an **end-to-end retention intelligence system** for a B2C EdTech SaaS, designed to **identify users at risk of churn *before* they leave**.

Instead of static churn reports, the system produces **user-level churn risk scores** that can be acted on immediately.

---

## 🚀 Why This Matters (30-second view)

- **Users:** 1,500  
- **Usage events:** 136,000+  
- **Observed churn rate:** ~13.5%  
- **Model ROC-AUC:** ~0.85  

📌 Output: a ranked list of users by churn risk — not just who churned, but **who is likely to churn next**.

---

## 🧠 The Core Problem

Most retention dashboards answer:
- “Who churned last month?”
- “What is the churn rate?”

That’s **too late**.

In real SaaS teams, the real question is:

> **Which users should we focus on *today* to prevent churn?**

This project solves that by combining:
- SQL-based behavioral analysis (what happened)
- Interpretable ML risk scoring (what’s likely to happen)

---
Edtech-SaaS-Retention-Analysis/
│
├── data/ # Final CSV outputs
├── data_generation/ # Synthetic data generation
├── sql/ # Schema & analytics queries
├── ml/ # Risk scoring model
├── docs/ # Assumptions & decisions
└── README.md
---

## 📂 Dataset Overview

| Component | Description |
|--------|------------|
| Users | Signup date, acquisition channel, country |
| Usage events | Daily sessions per user |
| Time span | ~9 months |
| Behavior patterns | Engagement decay, inactivity gaps |

All data is **synthetically generated but behaviorally realistic** and fully reproducible.

---

## 🔍 Churn Definition (Ground Truth)

A user is marked as **churned** if they have **no activity for 28 consecutive days**.

Why 28 days?
- Matches monthly learning cycles
- Avoids misclassifying short breaks
- Common heuristic in consumer SaaS

This label is derived **purely via SQL**, using window functions — no manual assumptions.

---

## 📐 Feature Engineering (SQL)

Features are computed in PostgreSQL to ensure transparency:

- **days_since_last_activity** → recency
- **active_days** → tenure & habit formation
- **avg_sessions_per_day** → engagement intensity

⚠️ No future data leakage  
⚠️ No hand-crafted labels

---

## 🤖 Machine Learning (Why & How)

### Why ML?
SQL is excellent for analysis, but it cannot:
- Rank active users by future churn risk
- Combine weak signals into one decision score

ML converts multiple behavioral signals into a **single churn probability per user**.

### Model Choice
- **Logistic Regression**
- Interpretable coefficients
- Probabilistic output
- Suitable for business decision-making

---

## 📊 Model Performance

| Metric | Value |
|------|------|
| ROC-AUC | ~0.85 |
| Recall (churned users) | High |
| Accuracy | De-emphasized (imbalanced data) |

The model prioritizes **catching at-risk users early**, not cosmetic accuracy.

---

## 🧮 What Is a Churn Risk Score?

A churn risk score is:

> **The estimated probability that a user will churn soon, given their current behavior.**

Example:
- User A → 0.12 (low risk)
- User B → 0.78 (high risk)

---

## 🏢 Real-World Usage Example

Imagine a retention team with capacity to contact only **10% of users**:

| User | Risk Score | Action |
|----|-----------|-------|
| 1489 | 0.82 | Personal outreach |
| 652 | 0.74 | Discount / reminder |
| 951 | 0.61 | Engagement nudge |
| 1272 | 0.08 | No action |

This turns analytics into **prioritized action**.

---

## 📁 Repository Structure
Edtech-SaaS-Retention-Analysis/
│
├── data/ # Final CSV outputs
├── data_generation/ # Synthetic data generation
├── sql/ # Schema & analytics queries
├── ml/ # Risk scoring model
├── docs/ # Assumptions & decisions
└── README.md

---

## 🧠 Key Takeaways

- Retention is a **prediction + prioritization** problem
- Interpretable ML often beats complex models in practice
- Clean SQL → ML handoff is critical in real systems
- Risk scores enable **proactive**, not reactive, retention

---

## 🔮 Possible Extensions

- Pricing & plan features
- Content-level engagement
- Rolling retraining
- Intervention A/B testing

---

## 👤 Author

**Aryan Raj**  
Computer Science Undergraduate | Data Analytics & Applied ML  
Focused on business-aligned analytics systems



## 🧩 End-to-End Architecture

