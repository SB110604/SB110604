# 🏭 BE Project Final — Industrial Safety Monitoring System

> **Final-year BE project** — Advanced AI-powered industrial safety platform with real-time IoT sensor monitoring, machine-learning anomaly detection, Twilio SMS alerts, MySQL database, and a live web dashboard.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🤖 **AI Anomaly Detection** | Isolation Forest ML model auto-detects dangerous sensor readings |
| 📲 **Twilio SMS Alerts** | Instant SMS to `+919322511660` on CRITICAL / HIGH severity events |
| 🗄️ **MySQL Database** | Full relational schema: Users, Zones, Sensors, Readings, Alerts, SMS Logs |
| ⚡ **Real-time WebSocket** | Live sensor feed pushed to the browser dashboard |
| 🔐 **JWT Authentication** | Secure login, role-based access (admin / user) |
| 🗺️ **REST API** | FastAPI with auto-generated Swagger UI at `/docs` |
| 📊 **Live Dashboard** | Browser dashboard showing alerts, SMS logs, and sensor KPIs |
| 🔄 **Alembic Migrations** | Database schema versioning |

---

## 🏗️ Project Structure

```
BE_project_final/
├── app/
│   ├── core/
│   │   ├── config.py        # All settings via env vars
│   │   ├── database.py      # SQLAlchemy engine & session
│   │   └── security.py      # JWT + bcrypt helpers
│   ├── models/
│   │   └── db_models.py     # ORM: User, Zone, Sensor, Alert, SMSLog
│   ├── routes/
│   │   ├── auth.py          # /api/v1/auth/  — register, login, me
│   │   ├── sensors.py       # /api/v1/sensors/ — zones, sensors, readings
│   │   ├── alerts.py        # /api/v1/alerts/  — alerts + manual SMS
│   │   ├── ai.py            # /api/v1/ai/      — predict, train
│   │   └── websocket.py     # /ws/live         — real-time feed
│   └── services/
│       ├── twilio_service.py  # send_sms(), send_alert_sms()
│       └── ai_service.py      # detect_anomaly(), train_model()
├── migrations/              # Alembic migration scripts
├── templates/
│   └── dashboard.html       # Live web dashboard
├── tests/
│   ├── test_ai_service.py
│   └── test_api.py
├── .env.example             # ← Copy to .env and fill in credentials
├── alembic.ini
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start (VS Code)

### 1 — Clone & open
```bash
git clone https://github.com/SB110604/SB110604.git
cd SB110604/BE_project_final
code .
```

### 2 — Run the automated setup script ⚡
This single command handles **Steps 2–5** automatically:
- ✅ Creates Python virtual environment
- ✅ Installs all dependencies
- ✅ Guides you through `.env` configuration (asks for your values)
- ✅ Creates the MySQL database and all tables

```bash
python setup.py
```

> You'll be asked to enter your MySQL password and Twilio credentials interactively.

### 3 — Start the server
```bash
python run.py
```

Open **http://localhost:8000** → Live Dashboard  
Open **http://localhost:8000/docs** → Swagger API Explorer

---

## 📲 Twilio SMS Setup (Free)

1. Sign up at [twilio.com](https://www.twilio.com/) — free trial includes credits
2. Go to **Console → Account Info** — copy your `Account SID` and `Auth Token`
3. Get a free Twilio phone number (`+1XXXXXXXXXX`)
4. Add to `.env`:
   ```
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_FROM_NUMBER=+1XXXXXXXXXX
   ALERT_TO_NUMBER=+919322511660
   ```

SMS will automatically be sent when a sensor reading is CRITICAL or HIGH severity.

---

## 🗄️ Database Schema

```
users          → id, username, email, hashed_password, phone, is_admin
zones          → id, name, description, location
sensors        → id, name, type, unit, min/max threshold, zone_id
sensor_readings → id, sensor_id, value, is_anomaly, anomaly_score, recorded_at
alerts         → id, title, message, severity, status, sms_sent, sensor_id, zone_id
sms_logs       → id, to_number, from_number, message_body, twilio_sid, status
```

---

## 🤖 AI Model

The system uses **Isolation Forest** (scikit-learn) for unsupervised anomaly detection:

- **Train**: `POST /api/v1/ai/train` — trains on all stored readings for a sensor
- **Predict**: `POST /api/v1/ai/predict` — classify a single reading
- Model auto-saves to `app/models/safety_model.pkl`
- Anomaly threshold configurable via `ANOMALY_THRESHOLD` (default 0.85)

---

## 🧪 Run Tests
```bash
pip install pytest
pytest tests/ -v
```

---

## 🔑 API Quick Reference

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login → JWT token |
| GET  | `/api/v1/auth/me` | Current user info |
| POST | `/api/v1/sensors/zones` | Create monitoring zone |
| GET  | `/api/v1/sensors/` | List all sensors |
| POST | `/api/v1/sensors/readings` | Submit sensor reading (triggers AI + SMS) |
| GET  | `/api/v1/alerts/` | List alerts |
| PATCH | `/api/v1/alerts/{id}/acknowledge` | Acknowledge alert |
| PATCH | `/api/v1/alerts/{id}/resolve` | Resolve alert |
| POST | `/api/v1/alerts/sms/send` | Send manual SMS |
| GET  | `/api/v1/alerts/sms/logs` | View SMS history |
| POST | `/api/v1/ai/predict` | Run anomaly prediction |
| POST | `/api/v1/ai/train` | Train ML model |
| WS   | `/ws/live` | WebSocket live feed |

---

## 🛡️ Security Notes

- Never commit your `.env` file (it is in `.gitignore`)
- Change `APP_SECRET_KEY` and `JWT_SECRET_KEY` before deploying
- Restrict `allow_origins` in `app/main.py` CORS middleware for production

---

*Built with ❤️ by Sahil Bodke — Final Year BE Project*
