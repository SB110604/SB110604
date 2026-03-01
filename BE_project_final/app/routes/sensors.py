"""
Sensor routes — CRUD for zones, sensors, and posting readings.
Readings are automatically evaluated by the AI anomaly detector.
Critical anomalies trigger an SMS alert via Twilio.
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import ConfigDict, BaseModel
from sqlalchemy.orm import Session

from app.core import get_db
from app.models.db_models import Alert, AlertStatus, Sensor, SensorReading, SensorType, SeverityLevel, Zone
from app.routes.auth import get_current_user
from app.services.ai_service import detect_anomaly
from app.services.twilio_service import send_alert_sms

router = APIRouter(prefix="/sensors", tags=["Sensors"])


# --- Schemas ---

class ZoneCreate(BaseModel):
    name: str
    description: Optional[str] = None
    location: Optional[str] = None


class ZoneResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    location: Optional[str]
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class SensorCreate(BaseModel):
    name: str
    sensor_type: SensorType
    unit: Optional[str] = None
    min_threshold: Optional[float] = None
    max_threshold: Optional[float] = None
    zone_id: int


class SensorResponse(BaseModel):
    id: int
    name: str
    sensor_type: str
    unit: Optional[str]
    min_threshold: Optional[float]
    max_threshold: Optional[float]
    is_active: bool
    zone_id: int

    model_config = ConfigDict(from_attributes=True)


class ReadingCreate(BaseModel):
    sensor_id: int
    value: float


class ReadingResponse(BaseModel):
    id: int
    sensor_id: int
    value: float
    is_anomaly: bool
    anomaly_score: Optional[float]
    recorded_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Zone endpoints ---

@router.post("/zones", response_model=ZoneResponse, status_code=201)
def create_zone(payload: ZoneCreate, db: Session = Depends(get_db)):
    zone = Zone(**payload.model_dump())
    db.add(zone)
    db.commit()
    db.refresh(zone)
    return zone


@router.get("/zones", response_model=list[ZoneResponse])
def list_zones(db: Session = Depends(get_db)):
    return db.query(Zone).filter(Zone.is_active.is_(True)).all()


@router.get("/zones/{zone_id}", response_model=ZoneResponse)
def get_zone(zone_id: int, db: Session = Depends(get_db)):
    zone = db.query(Zone).filter(Zone.id == zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    return zone


# --- Sensor endpoints ---

@router.post("/", response_model=SensorResponse, status_code=201)
def create_sensor(payload: SensorCreate, db: Session = Depends(get_db)):
    if not db.query(Zone).filter(Zone.id == payload.zone_id).first():
        raise HTTPException(status_code=404, detail="Zone not found")
    sensor = Sensor(**payload.model_dump())
    db.add(sensor)
    db.commit()
    db.refresh(sensor)
    return sensor


@router.get("/", response_model=list[SensorResponse])
def list_sensors(
    zone_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Sensor).filter(Sensor.is_active.is_(True))
    if zone_id:
        query = query.filter(Sensor.zone_id == zone_id)
    return query.all()


@router.get("/{sensor_id}", response_model=SensorResponse)
def get_sensor(sensor_id: int, db: Session = Depends(get_db)):
    sensor = db.query(Sensor).filter(Sensor.id == sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor


# --- Readings endpoint (core logic) ---

@router.post("/readings", response_model=ReadingResponse, status_code=201)
def post_reading(payload: ReadingCreate, db: Session = Depends(get_db)):
    """
    Accept a sensor reading, run anomaly detection, and — if CRITICAL — send SMS.
    """
    sensor = db.query(Sensor).filter(Sensor.id == payload.sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    # --- AI anomaly detection ---
    result = detect_anomaly(payload.value, sensor.sensor_type.value)

    reading = SensorReading(
        sensor_id=sensor.id,
        value=payload.value,
        is_anomaly=result["is_anomaly"],
        anomaly_score=result["anomaly_score"],
    )
    db.add(reading)

    # --- Threshold breach detection ---
    threshold_breach = False
    severity = SeverityLevel.LOW
    if sensor.max_threshold and payload.value > sensor.max_threshold:
        threshold_breach = True
        severity = SeverityLevel.CRITICAL
    elif sensor.min_threshold and payload.value < sensor.min_threshold:
        threshold_breach = True
        severity = SeverityLevel.HIGH

    if result["is_anomaly"]:
        severity = SeverityLevel.CRITICAL

    # --- Create alert and send SMS for serious events ---
    if result["is_anomaly"] or threshold_breach:
        zone = db.query(Zone).filter(Zone.id == sensor.zone_id).first()
        zone_name = zone.name if zone else "Unknown Zone"

        alert = Alert(
            title=f"Anomaly detected on {sensor.name}",
            message=(
                f"Sensor '{sensor.name}' ({sensor.sensor_type.value}) in zone '{zone_name}' "
                f"reported value {payload.value} {sensor.unit or ''}. "
                f"Anomaly score: {result['anomaly_score']}."
            ),
            severity=severity,
            status=AlertStatus.PENDING,
            sensor_id=sensor.id,
            zone_id=sensor.zone_id,
        )
        db.add(alert)
        db.flush()  # get alert.id before commit

        if severity in (SeverityLevel.CRITICAL, SeverityLevel.HIGH):
            sms_log = send_alert_sms(
                alert_title=alert.title,
                zone_name=zone_name,
                severity=severity.value,
                sensor_value=payload.value,
                db=db,
            )
            alert.sms_sent = sms_log.status not in ("failed", None)
            alert.sms_sid = sms_log.twilio_sid

    db.commit()
    db.refresh(reading)
    return reading


@router.get("/readings/{sensor_id}", response_model=list[ReadingResponse])
def get_readings(
    sensor_id: int,
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db),
):
    return (
        db.query(SensorReading)
        .filter(SensorReading.sensor_id == sensor_id)
        .order_by(SensorReading.recorded_at.desc())
        .limit(limit)
        .all()
    )
