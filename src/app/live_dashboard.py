from pathlib import Path
import sys

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.api.rag_engine import rag_agent
from src.core.maars_engine import load_feature_store, load_model_bundle, process_event


st.set_page_config(page_title="MAARS Streaming Terminal", layout="wide")

st.markdown(
    """
<style>
.stApp {
    background-color: #050505;
    background-image: radial-gradient(circle at 50% 0%, #1a1a2e, #050505 80%);
    color: #00ffcc;
    font-family: "Courier New", Courier, monospace;
}
div[data-testid="stMetricValue"] {
    color: #ff0055 !important;
}
.rag-box {
    background: rgba(16, 185, 129, 0.1);
    border-left: 4px solid #10b981;
    padding: 20px;
    border-radius: 8px;
    font-family: monospace;
    color: #a7f3d0;
    white-space: pre-wrap;
    margin-top: 10px;
}
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource
def load_engine():
    model, explainer = load_model_bundle()
    feature_store = load_feature_store()
    return model, explainer, feature_store


model, explainer, feature_store = load_engine()
available_user_ids = sorted(feature_store.keys())

st.title("MAARS: Real-Time Streaming Intervention")
st.write(
    "Simulate a live event stream, recalculate churn risk on the fly, and trigger "
    "a retrieval-augmented micro-lesson when a user starts struggling."
)
st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Simulate Live Event Stream")

    if not available_user_ids:
        st.error("Feature store is empty. Run `python src/data/generate_telemetry.py` first.")
    else:
        user_id = st.selectbox("User ID", available_user_ids, index=0)
        event_type = st.selectbox("Event Type", ["quiz_failed", "rage_click", "video_pause", "login"])

        metadata = ""
        if event_type == "quiz_failed":
            metadata = st.selectbox(
                "Quiz Topic",
                ["Python Basics", "For Loops", "SQL Joins", "SQL Group By", "Machine Learning Overfitting"],
            )
        elif event_type == "video_pause":
            metadata = st.selectbox("Video Topic", ["SQL Joins", "Python Basics"])

        if st.button("Fire Event"):
            if model is None or explainer is None:
                st.error("Model offline. Run `python src/models/train_advanced_xgboost.py` first.")
            else:
                with st.spinner("Streaming event to the inference engine..."):
                    st.session_state["latest_data"] = process_event(
                        feature_store=feature_store,
                        model=model,
                        explainer=explainer,
                        user_id=user_id,
                        event_type=event_type,
                        metadata=metadata,
                        rag_agent=rag_agent,
                    )

with col2:
    st.subheader("Inference and RAG Output")

    if "latest_data" in st.session_state:
        data = st.session_state["latest_data"]

        c1, c2, c3 = st.columns(3)
        c1.metric("Current Risk Score", f"{data['new_risk_score']:.1%}")
        c2.metric("Primary SHAP Driver", data["primary_driver"])
        c3.metric("System Action", "Triggered RAG" if "RAG" in data["action_taken"] else "Logged")

        if "RAG" in data["action_taken"]:
            st.warning(data["action_taken"])
            st.markdown("### LLM RAG Micro-Lesson Generated:")
            st.markdown(f"<div class='rag-box'>{data['interventionable_content']}</div>", unsafe_allow_html=True)
        else:
            st.success("Event tracked. User remains stable. No intervention needed.")
    else:
        st.info("Awaiting live events from the stream...")
