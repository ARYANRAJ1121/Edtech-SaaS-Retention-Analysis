from pathlib import Path
import sqlite3
import sys

import pandas as pd
import plotly.express as px
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.agents.sql_agent import ask_agent
from src.utils.project_paths import advanced_data_path, project_path


st.set_page_config(page_title="MAARS Command Center", layout="wide")


def load_css(file_path: Path) -> None:
    if file_path.exists():
        st.markdown(f"<style>{file_path.read_text()}</style>", unsafe_allow_html=True)


@st.cache_data
def load_scored_users():
    db_path = advanced_data_path("telemetry.db")
    csv_path = advanced_data_path("scored_users.csv")

    if db_path.exists():
        try:
            with sqlite3.connect(db_path) as conn:
                df = pd.read_sql("SELECT * FROM scored_users", conn)
            if not df.empty:
                return df, db_path, None
        except Exception as exc:
            db_error = str(exc)
        else:
            db_error = None
    else:
        db_error = None

    if csv_path.exists():
        return pd.read_csv(csv_path), csv_path, db_error

    return None, None, db_error


load_css(project_path("src", "app", "style.css"))

st.markdown(
    """
<style>
.stApp {
    background-color: #050505;
    background-image: radial-gradient(circle at 50% 0%, #1a1a2e, #050505 80%);
    color: #00ffcc;
    font-family: "Courier New", Courier, monospace;
}
div[data-testid="metric-container"] {
    background: rgba(0, 255, 204, 0.05) !important;
    border: 1px solid rgba(0, 255, 204, 0.2) !important;
    box-shadow: 0 0 15px rgba(0, 255, 204, 0.1) !important;
}
h1, h2, h3, label {
    color: #00ffcc !important;
}
</style>
""",
    unsafe_allow_html=True,
)

st.title("MAARS: Multi-Agentic Autonomous Retention System")
st.markdown("---")

df, data_source, load_error = load_scored_users()

if df is None or df.empty:
    detail = f" Loader error: {load_error}" if load_error else ""
    st.error(
        "Telemetry data is offline. Run `python src/data/generate_telemetry.py` "
        "and `python src/models/train_advanced_xgboost.py` first." + detail
    )
else:
    st.caption(f"Loaded source: `{data_source.relative_to(PROJECT_ROOT)}`")

    mrr_at_risk = df[df["risk_score"] > 0.7]["mrr"].sum()
    total_mrr = df["mrr"].sum()
    avg_frustration = df["frustration_index"].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Active Cohort", f"{len(df):,}")
    col2.metric("MRR at High Risk", f"${mrr_at_risk:,.0f}", f"-{(mrr_at_risk / total_mrr) * 100:.1f}% of Total")
    col3.metric("System Frustration Index", f"{avg_frustration:.1f}", "Rage clicks + fails")
    col4.metric("Avg Engagement Velocity", f"{df['engagement_velocity'].mean():.2f}", "<1 means drop-off")

    st.markdown("---")

    tab1, tab2 = st.tabs(["Behavioral Clusters", "AI Data Scientist Terminal"])

    with tab1:
        st.subheader("Behavioral Topology: Frustration vs. Engagement Velocity")
        st.write(
            "Visualize user clusters to spot where interventions matter most. "
            "Top left is the danger zone: high frustration with dropping velocity."
        )

        fig = px.scatter(
            df,
            x="engagement_velocity",
            y="frustration_index",
            color="risk_score",
            size="mrr",
            hover_data=["user_id", "primary_churn_driver"],
            color_continuous_scale="Turbo",
            template="plotly_dark",
        )
        fig.add_shape(
            type="rect",
            x0=0,
            y0=df["frustration_index"].median(),
            x1=1,
            y1=df["frustration_index"].max(),
            fillcolor="red",
            opacity=0.1,
            line_width=0,
        )
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, width="stretch")

    with tab2:
        st.subheader("Autonomous SQL Agent")
        st.write(
            "Query the telemetry warehouse in plain English. "
            "The agent will translate it to SQLite and summarize the result."
        )

        query = st.text_input(
            "Query the data lake:",
            "Show me the top 5 users by MRR who have an engagement velocity < 0.5",
        )
        if st.button("Execute"):
            with st.spinner("Compiling SQL and analyzing telemetry..."):
                response = ask_agent(query)
            st.markdown(response)
