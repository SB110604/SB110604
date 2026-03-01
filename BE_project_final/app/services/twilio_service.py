"""
Twilio SMS Service
Sends SMS alerts via Twilio REST API.
"""

import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from app.core.config import get_settings
from app.models.db_models import SMSLog

logger = logging.getLogger(__name__)
settings = get_settings()


def _get_twilio_client() -> Client:
    """Create and return a Twilio REST client."""
    if not settings.twilio_account_sid or not settings.twilio_auth_token:
        raise ValueError(
            "Twilio credentials are not configured. "
            "Set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN in your .env file."
        )
    return Client(settings.twilio_account_sid, settings.twilio_auth_token)


def send_sms(
    message: str,
    db: Session,
    to_number: str | None = None,
) -> SMSLog:
    """
    Send an SMS via Twilio and persist a log entry in the database.

    Args:
        message:   The SMS body text.
        db:        SQLAlchemy database session.
        to_number: Recipient phone number (E.164 format).
                   Falls back to settings.alert_to_number.

    Returns:
        The persisted SMSLog ORM object.
    """
    recipient = to_number or settings.alert_to_number
    log = SMSLog(
        to_number=recipient,
        from_number=settings.twilio_from_number,
        message_body=message,
        sent_at=datetime.now(timezone.utc),
    )

    try:
        client = _get_twilio_client()
        twilio_msg = client.messages.create(
            body=message,
            from_=settings.twilio_from_number,
            to=recipient,
        )
        log.twilio_sid = twilio_msg.sid
        log.status = twilio_msg.status
        logger.info("SMS sent to %s | SID: %s", recipient, twilio_msg.sid)
    except ValueError as exc:
        log.status = "failed"
        log.error_message = str(exc)
        logger.error("SMS configuration error: %s", exc)
    except TwilioRestException as exc:
        log.status = "failed"
        log.error_message = str(exc)
        logger.error("Twilio API error sending SMS to %s: %s", recipient, exc)

    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def send_alert_sms(
    alert_title: str,
    zone_name: str,
    severity: str,
    sensor_value: float,
    db: Session,
    to_number: str | None = None,
) -> SMSLog:
    """
    Compose and send a formatted safety-alert SMS.

    Args:
        alert_title:  Short description of the alert.
        zone_name:    Name of the zone where the alert occurred.
        severity:     Severity level string (LOW/MEDIUM/HIGH/CRITICAL).
        sensor_value: The sensor reading that triggered the alert.
        db:           SQLAlchemy database session.
        to_number:    Override recipient phone number.

    Returns:
        The persisted SMSLog ORM object.
    """
    body = (
        f"🚨 SAFETY ALERT [{severity}]\n"
        f"Zone : {zone_name}\n"
        f"Issue: {alert_title}\n"
        f"Value: {sensor_value}\n"
        f"Action required immediately!\n"
        f"— Industrial Safety System"
    )
    return send_sms(body, db, to_number)
