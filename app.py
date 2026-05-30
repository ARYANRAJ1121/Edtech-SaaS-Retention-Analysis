import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv


load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent
CLASSIC_DATA_CANDIDATES = [
    PROJECT_ROOT / "data" / "churn_risk_scored_users_v2.csv",
    PROJECT_ROOT / "data" / "churn_risk_scored_users.csv",
]


st.set_page_config(page_title="Retention Intelligence", layout="wide")

st.markdown(
    """
<style>
.stApp {
    background-color: #0f172a;
    background-image:
        radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%),
        radial-gradient(at 50% 0%, hsla(225,39%,30%,1) 0, transparent 50%),
        radial-gradient(at 100% 0%, hsla(339,49%,30%,1) 0, transparent 50%);
    color: #e2e8f0;
}
div[data-testid="metric-container"] {
    background: rgba(30, 41, 59, 0.4) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 16px !important;
    padding: 20px !important;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1) !important;
}
h1, h2, h3 {
    background: -webkit-linear-gradient(45deg, #f8fafc, #94a3b8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
</style>
""",
    unsafe_allow_html=True,
)

st.title("EdTech Retention Intelligence Platform")
st.markdown("Proactively identify at-risk users using machine learning and AI.")


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

st.sidebar.header("AI Settings")
st.sidebar.write("Unlock the AI assistant by entering your Groq API key.")
api_key_input = st.sidebar.text_input(
    "Groq API Key",
    value=os.getenv("GROQ_API_KEY", ""),
    type="password",
)

if df is None:
    st.error(
        "Could not find a scored classic churn dataset. "
        "Run `python src/models/train_xgboost.py` to generate one."
    )
else:
    st.caption(f"Loaded dataset: `{data_source.relative_to(PROJECT_ROOT)}`")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Users Analyzed", f"{len(df):,}")

    score_col = "risk_score" if "risk_score" in df.columns else None

    if score_col:
        high_risk = len(df[df[score_col] > 0.7])
        col2.metric("High Risk Users (>70%)", f"{high_risk:,}")
        col3.metric("Avg Risk Score", f"{df[score_col].mean():.1%}")

        st.markdown("### Risk Distribution")
        fig = px.histogram(df, x=score_col, nbins=40, color_discrete_sequence=["#8b5cf6"])
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
        )
        st.plotly_chart(fig, width="stretch")

        st.markdown("### High Priority Interventions")
        st.dataframe(
            df.sort_values(by=score_col, ascending=False).head(15),
            width="stretch",
        )
    else:
        st.warning("Risk score column not found in the dataset. Displaying raw rows instead.")
        st.dataframe(df.head(20), width="stretch")

    st.markdown("---")
    st.subheader("Chat With Your Data")

    user_query = st.text_input(
        "Ask the AI about your retention data (for example, 'What should I do about high-risk users?'):"
    )

    if st.button("Generate Insight"):
        if not api_key_input:
            st.error("Please enter a Groq API key in the sidebar first.")
        elif not user_query:
            st.warning("Please type a question.")
        else:
            with st.spinner("AI is analyzing..."):
                try:
                    from groq import Groq

                    client = Groq(api_key=api_key_input)
                    data_summary = df.describe(include="all").transpose().fillna("").to_string()

                    prompt = f"""
                    You are an expert data analyst copilot.
                    Here is a summary of the user retention dataset:
                    {data_summary}

                    The user asked: {user_query}

                    Provide a concise, professional, and actionable business answer.
                    """

                    completion = client.chat.completions.create(
                        model="llama3-8b-8192",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7,
                    )
                    st.info(completion.choices[0].message.content)
                except Exception as exc:
                    st.error(f"Error connecting to Groq: {exc}")
