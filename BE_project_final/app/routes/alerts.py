"""
Alert routes — list, acknowledge, resolve alerts, and send manual SMS.
"""

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import ConfigDict, BaseModel
from sqlalchemy.orm import Session

from app.core import get_db
from app.models.db_models import Alert, AlertStatus, SeverityLevel, SMSLog
from app.routes.auth import get_current_user
from app.models.db_models import User
from app.services.twilio_service import send_sms

router = APIRouter(prefix="/alerts", tags=["Alerts"])


# --- Schemas ---

class AlertResponse(BaseModel):
    id: int
    title: str
    message: str
    severity: str
    status: str
    sms_sent: bool
    sms_sid: Optional[str]
    sensor_id: Optional[int]
    zone_id: Optional[int]
    created_at: datetime
    acknowledged_at: Optional[datetime]
    resolved_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class SMSSendRequest(BaseModel):
    message: str
    to_number: Optional[str] = None


class SMSLogResponse(BaseModel):
    id: int
    to_number: str
    from_number: str
    message_body: str
    twilio_sid: Optional[str]
    status: str
    error_message: Optional[str]
    sent_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Endpoints ---

@router.get("/", response_model=list[AlertResponse])
def list_alerts(
    severity: Optional[SeverityLevel] = Query(None),
    status: Optional[AlertStatus] = Query(None),
    limit: int = Query(50, le=500),
    db: Session = Depends(get_db),
):
    query = db.query(Alert).order_by(Alert.created_at.desc())
    if severity:
        query = query.filter(Alert.severity == severity)
    if status:
        query = query.filter(Alert.status == status)
    return query.limit(limit).all()


@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.patch("/{alert_id}/acknowledge", response_model=AlertResponse)
def acknowledge_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.status = AlertStatus.ACKNOWLEDGED
    alert.acknowledged_by = current_user.id
    alert.acknowledged_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(alert)
    return alert


@router.patch("/{alert_id}/resolve", response_model=AlertResponse)
def resolve_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.status = AlertStatus.RESOLVED
    alert.resolved_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(alert)
    return alert


# --- Manual SMS endpoints ---

@router.post("/sms/send", response_model=SMSLogResponse, status_code=201)
def send_manual_sms(
    payload: SMSSendRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Send a manual SMS alert (admin use)."""
    log = send_sms(payload.message, db, payload.to_number)
    return log


@router.get("/sms/logs", response_model=list[SMSLogResponse])
def sms_logs(
    limit: int = Query(50, le=500),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(SMSLog)
        .order_by(SMSLog.sent_at.desc())
        .limit(limit)
        .all()
    )
