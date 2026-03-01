"""
AI routes — train the anomaly model on historical data, run predictions.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core import get_db
from app.models.db_models import SensorReading
from app.routes.auth import get_current_user
from app.models.db_models import User
from app.services.ai_service import detect_anomaly, train_model

router = APIRouter(prefix="/ai", tags=["AI / Anomaly Detection"])


class PredictRequest(BaseModel):
    value: float
    sensor_type: str = "GENERAL"


class TrainRequest(BaseModel):
    sensor_id: int
    save_model: bool = True


@router.post("/predict")
def predict(payload: PredictRequest):
    """Run anomaly detection on a single reading."""
    return detect_anomaly(payload.value, payload.sensor_type)


@router.post("/train")
def train(
    payload: TrainRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Train the Isolation Forest model on all stored readings for a sensor.
    Requires authentication.
    """
    readings = (
        db.query(SensorReading.value)
        .filter(SensorReading.sensor_id == payload.sensor_id)
        .all()
    )
    if not readings:
        raise HTTPException(status_code=404, detail="No readings found for this sensor.")

    values = [r.value for r in readings]
    return train_model(values, save=payload.save_model)
