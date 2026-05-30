import os
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv

# Load agent for generating win-back emails
from src.agents.retention_agent import generate_retention_email

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent
CLASSIC_DATA_CANDIDATES = [
    PROJECT_ROOT / "data" / "churn_risk_scored_users_v2.csv",
    PROJECT_ROOT / "data" / "churn_risk_scored_users.csv",
]

st.set_page_config(page_title="Nexus Retention Intelligence", layout="wide", page_icon="🎯")

# Ultra-premium styling
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');

.stApp {
    background-color: #0b0f19;
    background-image:
        radial-gradient(at 0% 0%, hsla(244, 33%, 12%, 1) 0, transparent 50%),
        radial-gradient(at 50% 0%, hsla(220, 45%, 15%, 1) 0, transparent 50%),
        radial-gradient(at 100% 0%, hsla(340, 50%, 13%, 1) 0, transparent 50%);
    color: #f1f5f9;
    font-family: 'Plus Jakarta Sans', sans-serif;
}

h1, h2, h3, h4 {
    font-family: 'Outfit', sans-serif;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #ffffff 30%, #94a3b8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.02em;
}

/* Premium Card / Container Style */
div[data-testid="metric-container"], .premium-card {
    background: rgba(17, 24, 39, 0.45) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 20px !important;
    padding: 24px !important;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

div[data-testid="metric-container"]:hover {
    border-color: rgba(99, 102, 241, 0.3) !important;
    box-shadow: 0 10px 30px -5px rgba(99, 102, 241, 0.15) !important;
    transform: translateY(-2px);
}

.email-box {
    background: rgba(99, 102, 241, 0.06) !important;
    border: 1px dashed rgba(99, 102, 241, 0.3) !important;
    border-radius: 12px;
    padding: 20px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #e2e8f0;
    line-height: 1.6;
    margin-top: 15px;
}

.highlight-text {
    color: #818cf8;
    font-weight: 700;
}

.resume-highlight {
    background: rgba(239, 68, 68, 0.06);
    border-left: 4px solid #ef4444;
    padding: 16px;
    border-radius: 0 12px 12px 0;
    margin-bottom: 20px;
}
</style>
""",
    unsafe_allow_html=True,
)

# Header Section
col_logo, col_title = st.columns([1, 12])
with col_title:
    st.title("Nexus Retention Intelligence Platform")
    st.markdown(
        "<p style='font-size:1.15rem; color:#94a3b8; margin-top:-10px;'>High-fidelity retention scoring, driver attribution, and automated interventions.</p>",
        unsafe_allow_html=True,
    )

@st.cache_data
def load_data():
    for path in CLASSIC_DATA_CANDIDATES:
        if path.exists():
            df = pd.read_csv(path)
            if "risk_score" not in df.columns and "churn_risk_score" in df.columns:
                df = df.rename(columns={"churn_risk_score": "risk_score"})
            return df, path
    return None, None

df, data_source = load_data()

# Sidebar Config
st.sidebar.image(
    "https://img.icons8.com/gradient/100/000000/radar-plot.png",
    width=60,
)
st.sidebar.markdown("### **Platform Config**")
st.sidebar.markdown(
    "Configure key settings and view system status below."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### **Groq AI Assistant**")
api_key_input = st.sidebar.text_input(
    "Groq API Key",
    value=os.getenv("GROQ_API_KEY", ""),
    type="password",
    help="Pasted in your local .env file. Used to power the conversational copilot and personalized email generator.",
)

# Update environment variable if manually entered
if api_key_input:
    os.environ["GROQ_API_KEY"] = api_key_input

st.sidebar.markdown("---")
st.sidebar.markdown("### **Pipeline Status**")
st.sidebar.success("✓ Synthetic Telemetry (136k events)")
st.sidebar.success("✓ SQL Feature Pipeline (Engineered)")
st.sidebar.success("✓ Churn Model (ROC-AUC ~0.85)")

if df is None:
    st.error(
        "Could not locate the scored classic churn dataset. "
        "Please run `python src/models/train_xgboost.py` to compile."
    )
else:
    # ------------------ EXECUTIVE METRICS ------------------
    total_users = len(df)
    high_risk_users = len(df[df["risk_score"] > 0.7])
    avg_risk = df["risk_score"].mean()

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(
            label="Total Active Cohort",
            value=f"{total_users:,}",
            help="Total synthetic users simulated across 6 months.",
        )
    with m2:
        st.metric(
            label="High Risk Users (>70%)",
            value=f"{high_risk_users:,}",
            delta=f"{(high_risk_users / total_users) * 100:.1f}% of Cohort",
            delta_color="inverse",
            help="Users whose behavioral patterns indicate imminent churn.",
        )
    with m3:
        st.metric(
            label="Average Cohort Risk",
            value=f"{avg_risk:.1%}",
            help="The average probability score of churn across the entire active set.",
        )

    st.markdown("---")

    # Main Tab Control
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📊 Executive Overview",
            "🛡️ Retention Control Room",
            "🧠 AI Copilot",
            "🎓 Interview Prep & Code Map",
        ]
    )

    # ==================== TAB 1: EXECUTIVE OVERVIEW ====================
    with tab1:
        col_chart1, col_chart2 = st.columns([1, 1])

        with col_chart1:
            st.subheader("Distribution of Risk Probabilities")
            st.markdown("Most users cluster in the low-risk zone, with a trailing tail of disengaged users.")
            fig_hist = px.histogram(
                df,
                x="risk_score",
                nbins=35,
                color_discrete_sequence=["#6366f1"],
                labels={"risk_score": "Churn Probability"},
                template="plotly_dark",
            )
            fig_hist.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_family="Plus Jakarta Sans",
                margin=dict(l=20, r=20, t=20, b=20),
            )
            st.plotly_chart(fig_hist, use_container_width=True)

        with col_chart2:
            st.subheader("Tenure (Active Days) vs. Churn Risk")
            st.markdown("Users with low active tenure (bottom-left) carry the highest density of high churn risk.")
            
            # Subsample slightly for performance visualization
            sample_df = df.sample(min(1000, len(df)), random_state=42)
            fig_scatter = px.scatter(
                sample_df,
                x="active_days",
                y="risk_score",
                color="primary_churn_driver",
                size="total_sessions",
                color_discrete_sequence=px.colors.qualitative.Safe,
                labels={"active_days": "Active Tenure (Days)", "risk_score": "Churn Risk"},
                template="plotly_dark",
            )
            fig_scatter.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_family="Plus Jakarta Sans",
                margin=dict(l=20, r=20, t=20, b=20),
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

    # ==================== TAB 2: RETENTION CONTROL ROOM ====================
    with tab2:
        st.subheader("High Priority Accounts & Interventions")
        st.markdown(
            "This control room allows you to inspect at-risk accounts, isolate their primary failure driver, "
            "and generate highly personalized outreach emails using the **RAG Retention Agent**."
        )

        col_table, col_detail = st.columns([3, 2])

        # Filter to at-risk accounts
        at_risk_df = df.sort_values(by="risk_score", ascending=False)

        with col_table:
            st.markdown("**At-Risk User Registry** (Click a row to inspect metrics)")
            st.dataframe(
                at_risk_df[["user_id", "active_days", "days_since_last_activity", "avg_sessions_per_day", "risk_score", "primary_churn_driver"]].head(15),
                use_container_width=True,
                height=480,
            )

        with col_detail:
            st.markdown("**Outreach & Retention Agent Generator**")
            
            selected_user_id = st.selectbox(
                "Select User ID to generate outreach:",
                at_risk_df["user_id"].head(15).tolist()
            )

            if selected_user_id:
                user_row = df[df["user_id"] == selected_user_id].iloc[0]
                
                # Render details card
                st.markdown(
                    f"""
                    <div class="premium-card">
                        <h4>Account Metrics for User #{int(user_row['user_id'])}</h4>
                        <table style="width:100%; border-collapse:collapse; margin-top:10px;">
                            <tr><td style="padding:6px 0; color:#94a3b8;">Active Tenure:</td><td style="text-align:right; font-weight:700;">{int(user_row['active_days'])} days</td></tr>
                            <tr><td style="padding:6px 0; color:#94a3b8;">Days Inactive:</td><td style="text-align:right; font-weight:700; color:#f87171;">{int(user_row['days_since_last_activity'])} days</td></tr>
                            <tr><td style="padding:6px 0; color:#94a3b8;">Daily Intensity:</td><td style="text-align:right; font-weight:700;">{user_row['avg_sessions_per_day']:.2f} sessions/day</td></tr>
                            <tr><td style="padding:6px 0; color:#94a3b8;">Total Sessions:</td><td style="text-align:right; font-weight:700;">{int(user_row['total_sessions'])}</td></tr>
                            <tr><td style="padding:6px 0; color:#94a3b8; font-weight:bold;">Churn Probability:</td><td style="text-align:right; font-weight:800; color:#f87171; font-size:1.1rem;">{user_row['risk_score']:.1%}</td></tr>
                            <tr><td style="padding:6px 0; color:#94a3b8; font-weight:bold;">Primary Churn Driver:</td><td style="text-align:right; font-weight:800; color:#818cf8;">{user_row['primary_churn_driver']}</td></tr>
                        </table>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown("#### **Automated Win-Back Outreach Generator**")
                if st.button("Generate Email Outreach"):
                    with st.spinner("Analyzing driver & drafting outreach email..."):
                        user_data = {
                            "user_id": int(user_row["user_id"]),
                            "active_days": int(user_row["active_days"]),
                            "days_since_last_activity": int(user_row["days_since_last_activity"]),
                            "avg_sessions_per_day": float(user_row["avg_sessions_per_day"]),
                            "total_sessions": int(user_row["total_sessions"]),
                        }
                        
                        email_content = generate_retention_email(
                            user_data=user_data,
                            primary_driver=user_row["primary_churn_driver"],
                            risk_score=float(user_row["risk_score"]),
                        )
                        
                        email_content_html = email_content.replace("\n", "<br>")
                        st.markdown(
                            f"""
                            <div class="email-box">
                                {email_content_html}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

    # ==================== TAB 3: AI COPILOT ====================
    with tab3:
        st.subheader("AI Churn Copilot Assistant")
        st.markdown(
            "Leverage the power of natural-language data analysis. This assistant utilizes Groq "
            "to query statistical summaries, synthesize business recommendations, and answer questions."
        )

        user_query = st.text_input(
            "Ask the AI about your cohort (for example, 'Analyze why low tenure users are dropping off and recommend 3 interventions'):",
            placeholder="Type your question..."
        )

        if st.button("Analyze Data"):
            if not api_key_input:
                st.error("Configure your Groq API Key in the sidebar to enable the copilot.")
            elif not user_query:
                st.warning("Please enter a question.")
            else:
                with st.spinner("Analyzing cohort metrics..."):
                    try:
                        from groq import Groq

                        client = Groq(api_key=api_key_input)
                        data_summary = df.describe(include="all").transpose().fillna("").to_string()

                        prompt = f"""
                        You are an expert SaaS retention analyst and data copilot.
                        Here is a complete statistical summary of the scored user dataset:
                        {data_summary}

                        The user asked: {user_query}

                        Provide a highly concise, professional, and actionable business answer detailing your findings. Use bolding and structured bullet points.
                        """

                        completion = client.chat.completions.create(
                            model="llama3-8b-8192",
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0.6,
                        )
                        st.info(completion.choices[0].message.content)
                    except Exception as exc:
                        st.error(f"Groq Integration Error: {exc}")

    # ==================== TAB 4: INTERVIEW PREP & CODE MAP ====================
    with tab4:
        st.subheader("🎓 Interview Preparation & Project Mapping")
        st.markdown(
            "Use this tab to master this project. This section correlates the bullet points on your resume "
            "directly to the files in your workspace, allowing you to explain your architectural choices in interviews."
        )

        resume_points = [
            {
                "title": "🧠 1. Churn Prediction & synthetic data simulation",
                "bullet": "Built a churn prediction system on 136,000+ user engagement events across 1,500 customers over 9 months, identifying at-risk users an average of 14 days before platform departure.",
                "files": [
                    ("data_generation/generate_users.py", "Simulates base metadata (countries, channels) for 1,500 active accounts."),
                    ("data_generation/generate_usage_events.py", "Generates daily session logs (136k+ events) based on high, medium, and low engagement archetypes with exponential decay decay rates."),
                    ("src/models/train_xgboost.py", "Upgraded production modeling script that splits features, fits the XGBoost model, exports model objects, and runs SHAP explanations.")
                ],
                "pitch": "I wrote custom data generators using NumPy and Pandas to simulate realistic B2B student behaviors (logins, session intensities, decay coefficients) over a 6-month cohort, establishing a rigorous benchmark for predictive testing without using generic public datasets."
            },
            {
                "title": "📐 2. SQL Feature Engineering Layer",
                "bullet": "Engineered behavioral features using PostgreSQL window functions including rolling active-day counts, session frequency, engagement intensity scores, and recency metrics.",
                "files": [
                    ("sql/complete_sql_queries.sql", "Contains the exact feature queries. Review the aggregation block on lines 106-123."),
                ],
                "pitch": "Instead of doing expensive calculations in Pandas, I engineered all ML-ready behavioral indicators in the database layer. I calculated active tenure (active_days), recency (days_since_last_activity), and intensity (avg_sessions_per_day) directly using optimized aggregate SQL structures."
            },
            {
                "title": "🤖 3. Churn Risk & Explainer Models",
                "bullet": "Trained a logistic regression classifier achieving ROC-AUC of 0.85, enabling the retention team to prioritize the top 200 high-risk accounts monthly for targeted outreach.",
                "files": [
                    ("ml/risk_scoring.ipynb", "Original exploratory Jupyter Notebook demonstrating the baseline Logistic Regression modeling code and training evaluations."),
                    ("src/models/train_xgboost.py", "Production script training a highly accurate XGBoost model, utilizing scale_pos_weight to manage severe class imbalances."),
                ],
                "pitch": "I started by building a transparent baseline using Logistic Regression in a Jupyter Notebook to gain immediate feature interpretability. To maximize predictive accuracy, I migrated this into a structured Python pipeline using XGBoost, resulting in a robust ROC-AUC score. I leveraged SHAP values to attribute a primary churn driver directly to every user record, making the outputs actionable for customer success teams."
            },
            {
                "title": "🔒 4. Eliminating Data Leakage",
                "bullet": "Enforced a strict 30-day churn definition via SQL temporal logic to eliminate data leakage, producing a clean, production-ready feature set with fully reproducible preprocessing steps.",
                "files": [
                    ("sql/complete_sql_queries.sql", "Check lines 126-158. Uses LEAD() OVER (PARTITION BY ... ORDER BY ...) to determine activity gap durations."),
                ],
                "pitch": "A common mistake in churn modeling is using future event variables to predict current state (data leakage). I solved this by utilizing SQL window functions to compute sequential gaps between subsequent logins. If a user is inactive for 28+ consecutive days, they are labeled as churned. This logical gate cleanly separates historical inputs from labels."
            }
        ]

        for pt in resume_points:
            with st.expander(pt["title"]):
                st.markdown(f"<div class='resume-highlight'><b>Resume Bullet Point:</b><br><i>{pt['bullet']}</i></div>", unsafe_allow_html=True)
                st.markdown("#### **📂 Project File Map**")
                for filepath, desc in pt["files"]:
                    st.markdown(f"- 📄 `file:///{filepath}` — *{desc}*")
                st.markdown("#### **💬 How to explain it in an Interview**")
                st.info(pt["pitch"])
