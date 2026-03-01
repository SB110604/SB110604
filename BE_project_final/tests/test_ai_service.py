"""
Unit tests for the AI anomaly detection service.
No database or Twilio credentials required.
Run: pytest tests/
"""

import pytest
from app.services.ai_service import detect_anomaly, train_model


def test_detect_anomaly_returns_expected_keys():
    result = detect_anomaly(50.0, "TEMPERATURE")
    assert "is_anomaly" in result
    assert "anomaly_score" in result
    assert "confidence" in result
    assert "value" in result
    assert result["value"] == 50.0


def test_anomaly_score_is_float_in_range():
    result = detect_anomaly(100.0, "PRESSURE")
    assert isinstance(result["anomaly_score"], float)
    assert 0.0 <= result["anomaly_score"] <= 1.0


def test_train_model_requires_min_readings():
    result = train_model([1.0, 2.0], save=False)
    assert result["success"] is False
    assert "error" in result


def test_train_model_success():
    readings = list(range(20))
    result = train_model(readings, save=False)
    assert result["success"] is True
    assert result["samples_used"] == 20


def test_detect_anomaly_after_training():
    readings = [20.0 + i * 0.1 for i in range(50)]  # tight normal range
    train_model(readings, save=False)
    normal = detect_anomaly(20.5, "TEMPERATURE")
    assert isinstance(normal["is_anomaly"], bool)
