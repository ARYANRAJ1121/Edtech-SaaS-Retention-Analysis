from pathlib import Path
import sys
from typing import Literal

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.api.rag_engine import rag_agent
from src.core.maars_engine import load_feature_store, load_model_bundle, process_event


app = FastAPI(title="MAARS Event Streaming Pipeline")

model, explainer = load_model_bundle()
feature_store = load_feature_store()


class Event(BaseModel):
    user_id: int
    event_type: Literal["quiz_failed", "rage_click", "video_pause", "login"]
    metadata: str = Field(default="", description="Topic or event-specific metadata")


class EventResponse(BaseModel):
    user_id: int
    new_risk_score: float
    primary_driver: str
    action_taken: str
    interventionable_content: str


@app.get("/health")
def healthcheck():
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "explainer_loaded": explainer is not None,
        "feature_store_size": len(feature_store),
    }


@app.post("/track-event", response_model=EventResponse)
def track_live_event(event: Event):
    try:
        result = process_event(
            feature_store=feature_store,
            model=model,
            explainer=explainer,
            user_id=event.user_id,
            event_type=event.event_type,
            metadata=event.metadata,
            rag_agent=rag_agent,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="User not found in feature store.") from exc

    return EventResponse(**result)


if __name__ == "__main__":
    print("Starting MAARS real-time inference pipeline...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
