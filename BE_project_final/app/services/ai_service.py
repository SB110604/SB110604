"""
AI Anomaly Detection Service
Uses Isolation Forest to detect anomalous sensor readings in real-time.
"""

import logging
import os
from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import IsolationForest

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Module-level model cache
_model: IsolationForest | None = None


def _get_model() -> IsolationForest:
    """Load the saved model or create a default untrained one."""
    global _model
    if _model is not None:
        return _model

    model_path = Path(settings.ai_model_path)
    if model_path.exists():
        _model = joblib.load(model_path)
        logger.info("Loaded anomaly detection model from %s", model_path)
    else:
        logger.warning(
            "No trained model found at %s — using default Isolation Forest. "
            "Call /api/v1/ai/train to train on historical data.",
            model_path,
        )
        _model = IsolationForest(
            n_estimators=100,
            contamination=0.05,
            random_state=42,
        )
    return _model


def detect_anomaly(value: float, sensor_type: str) -> dict:
    """
    Predict whether a sensor reading is anomalous.

    Args:
        value:       The sensor reading value.
        sensor_type: Type string (TEMPERATURE, PRESSURE, etc.)

    Returns:
        dict with keys: is_anomaly (bool), anomaly_score (float), confidence (float)
    """
    model = _get_model()
    sample = np.array([[value]])

    try:
        # score_samples returns negative values; more negative = more anomalous
        raw_score = float(model.score_samples(sample)[0])
        # Normalise to [0, 1] where 1 = definitely anomaly
        anomaly_score = max(0.0, min(1.0, -raw_score))
        is_anomaly = anomaly_score >= settings.anomaly_threshold
    except Exception as exc:  # model may be unfitted; fall back to threshold check
        logger.warning("Anomaly model prediction failed (%s). Using fallback.", exc)
        anomaly_score = 0.0
        is_anomaly = False

    return {
        "is_anomaly": is_anomaly,
        "anomaly_score": round(anomaly_score, 4),
        "confidence": round(anomaly_score if is_anomaly else 1.0 - anomaly_score, 4),
        "sensor_type": sensor_type,
        "value": value,
    }


def train_model(readings: list[float], save: bool = True) -> dict:
    """
    Train (or re-train) the Isolation Forest on historical readings.

    Args:
        readings: List of historical sensor values.
        save:     Whether to persist the trained model to disk.

    Returns:
        dict with training summary.
    """
    global _model

    if len(readings) < 10:
        return {"success": False, "error": "Need at least 10 readings to train."}

    X = np.array(readings).reshape(-1, 1)
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    model.fit(X)
    _model = model

    if save:
        model_path = Path(settings.ai_model_path)
        model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, model_path)
        logger.info("Model saved to %s", model_path)

    return {
        "success": True,
        "samples_used": len(readings),
        "model_path": str(Path(settings.ai_model_path).resolve()) if save else None,
    }
