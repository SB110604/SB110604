"""
Integration tests for the FastAPI application using an in-memory SQLite DB.
Run: pytest tests/
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db

# --- In-memory SQLite for tests ---
TEST_DATABASE_URL = "sqlite:///./test_temp.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_dashboard_returns_html():
    r = client.get("/")
    assert r.status_code == 200
    assert "Industrial Safety" in r.text


def test_register_and_login():
    # Register
    r = client.post("/api/v1/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "secret123",
        "full_name": "Test User",
    })
    assert r.status_code == 201
    data = r.json()
    assert data["username"] == "testuser"

    # Login
    r = client.post("/api/v1/auth/login", data={
        "username": "testuser",
        "password": "secret123",
    })
    assert r.status_code == 200
    token = r.json()["access_token"]
    assert token


def test_duplicate_register():
    client.post("/api/v1/auth/register", json={
        "username": "dupuser",
        "email": "dup@example.com",
        "password": "pass",
    })
    r = client.post("/api/v1/auth/register", json={
        "username": "dupuser",
        "email": "dup2@example.com",
        "password": "pass",
    })
    assert r.status_code == 400


def test_create_zone_and_sensor():
    # Create zone
    r = client.post("/api/v1/sensors/zones", json={"name": "Boiler Room", "location": "Floor 1"})
    assert r.status_code == 201
    zone_id = r.json()["id"]

    # Create sensor
    r = client.post("/api/v1/sensors/", json={
        "name": "Temp Sensor A",
        "sensor_type": "TEMPERATURE",
        "unit": "°C",
        "min_threshold": 10.0,
        "max_threshold": 80.0,
        "zone_id": zone_id,
    })
    assert r.status_code == 201
    sensor_id = r.json()["id"]

    # Post a normal reading
    r = client.post("/api/v1/sensors/readings", json={"sensor_id": sensor_id, "value": 45.0})
    assert r.status_code == 201
    assert "is_anomaly" in r.json()

    # Post an above-threshold reading (should trigger alert creation)
    r = client.post("/api/v1/sensors/readings", json={"sensor_id": sensor_id, "value": 999.0})
    assert r.status_code == 201

    # Get readings
    r = client.get(f"/api/v1/sensors/readings/{sensor_id}")
    assert r.status_code == 200
    assert len(r.json()) >= 2


def test_list_alerts():
    r = client.get("/api/v1/alerts/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_ai_predict():
    r = client.post("/api/v1/ai/predict", json={"value": 55.5, "sensor_type": "TEMPERATURE"})
    assert r.status_code == 200
    data = r.json()
    assert "is_anomaly" in data
    assert "anomaly_score" in data
