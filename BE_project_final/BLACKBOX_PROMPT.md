# 🤖 Blackbox AI Prompts — BE Project Final
# ==========================================
# How to use:
#   1. Install the "Blackbox" extension in VS Code  (ID: Blackboxapp.blackbox)
#   2. Open Blackbox chat:  Ctrl+Shift+A  (or click the Blackbox icon in sidebar)
#   3. Copy any prompt below and paste it into the Blackbox chat box
# ==========================================


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PROMPT 1 — UNDERSTAND & RUN THE PROJECT
# Paste this first to let Blackbox understand the full project
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I have a FastAPI backend project called "BE_project_final" — an Industrial Safety Monitoring System. Here is the complete structure:

PROJECT STACK:
- FastAPI 0.110 + Uvicorn (Python web server)
- SQLAlchemy 2.0 ORM with MySQL database
- Twilio SMS alerts (fires on CRITICAL/HIGH sensor events)
- scikit-learn Isolation Forest (AI anomaly detection)
- JWT authentication (bcrypt + python-jose)
- WebSocket live feed (/ws/live)
- Jinja2 HTML dashboard at /

FOLDER LAYOUT:
BE_project_final/
  app/
    main.py              ← FastAPI app entry point
    core/
      config.py          ← pydantic-settings, reads .env
      database.py        ← SQLAlchemy engine + get_db()
      security.py        ← JWT create/decode, bcrypt hash
    models/
      db_models.py       ← ORM: User, Zone, Sensor, SensorReading, Alert, SMSLog
    routes/
      auth.py            ← POST /api/v1/auth/register, /login, GET /me
      sensors.py         ← POST /api/v1/sensors/readings (triggers AI + SMS)
      alerts.py          ← GET/PATCH /api/v1/alerts, POST /sms/send
      ai.py              ← POST /api/v1/ai/predict, /train
      websocket.py       ← WS /ws/live
    services/
      twilio_service.py  ← send_sms(), send_alert_sms()
      ai_service.py      ← detect_anomaly(), train_model()
  templates/
    dashboard.html       ← live browser dashboard
  static/                ← static assets
  setup.py               ← one-command first-time setup
  run.py                 ← start server
  requirements.txt
  .env.example           ← copy to .env and fill in credentials

HOW TO RUN:
  Step 1: python setup.py     (first time only — creates venv, installs deps, sets up .env and MySQL)
  Step 2: python run.py       (starts server at http://localhost:8000)

IMPORTANT .env values needed:
  DB_PASSWORD=<your MySQL root password>
  TWILIO_ACCOUNT_SID=<from twilio.com/console>
  TWILIO_AUTH_TOKEN=<from twilio.com/console>
  TWILIO_FROM_NUMBER=<your Twilio number like +1XXXXXXXXXX>
  ALERT_TO_NUMBER=+919322511660

Please help me understand this project and assist me in running it.


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PROMPT 2 — FULL STEP-BY-STEP RUN GUIDE
# Paste this to get exact terminal commands to run the project
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I have a FastAPI Industrial Safety project in the folder BE_project_final/.
Give me the exact terminal commands (Windows CMD/PowerShell) to:
1. Navigate into the project folder
2. Run the automated setup script (setup.py) that creates venv + installs packages + creates .env + creates MySQL database
3. Start the server using run.py
4. Open the dashboard and API docs in the browser
The project uses Python, FastAPI, MySQL, and Twilio SMS.


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PROMPT 3 — DEBUG A STARTUP ERROR
# Paste this if the server crashes on startup
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

My FastAPI Industrial Safety project (BE_project_final/) crashes when I run
  python run.py
Here is the exact error message I see in the terminal:

[PASTE YOUR ERROR HERE]

The project uses FastAPI, SQLAlchemy + MySQL, Twilio SMS, and scikit-learn.
The main entry point is app/main.py. The config is loaded from .env via app/core/config.py.
What is causing this error and how do I fix it step by step?


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PROMPT 4 — TEST THE TWILIO SMS ALERT
# Paste this to test that Twilio SMS is working
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

My FastAPI project is running at http://localhost:8000.
It uses Twilio to send SMS alerts to +919322511660 when a sensor reading is CRITICAL.
I want to test that Twilio SMS is working.

Step 1: Show me the curl command (or HTTP request) to:
  a) Register a user at POST /api/v1/auth/register
  b) Login at POST /api/v1/auth/login to get a JWT token
  c) Create a zone at POST /api/v1/sensors/zones
  d) Create a temperature sensor at POST /api/v1/sensors/
  e) Post a sensor reading with a dangerously high value (e.g. 999.0) at POST /api/v1/sensors/readings
     — this should trigger the anomaly detector and fire an SMS to +919322511660

Step 2: Show me how to check if the SMS was sent by viewing SMS logs at GET /api/v1/alerts/sms/logs


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PROMPT 5 — FIX MySQL CONNECTION ERROR
# Paste this if you get a database connection error
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

My FastAPI project cannot connect to MySQL.
The database URL in my .env is:
  DB_HOST=localhost
  DB_PORT=3306
  DB_USER=root
  DB_PASSWORD=<my password>
  DB_NAME=industrial_safety_db

The SQLAlchemy connection string used is:
  mysql+pymysql://root:<password>@localhost:3306/industrial_safety_db

I get this error: [PASTE ERROR HERE]

Help me fix this step by step. Also show me how to:
1. Check if MySQL is running
2. Create the database manually if needed
3. Verify the connection works


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PROMPT 6 — ADD A NEW SENSOR TYPE / FEATURE
# Paste this to extend the project with Blackbox's help
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I have a FastAPI Industrial Safety project with the following sensor types defined in
app/models/db_models.py:
  TEMPERATURE, PRESSURE, GAS, SMOKE, VIBRATION, HUMIDITY, MOTION

I want to add a new sensor type called "FIRE". Help me:
1. Add FIRE to the SensorType enum in app/models/db_models.py
2. Add specific threshold defaults for fire sensors in app/routes/sensors.py
3. Write a new alert message specifically for fire events
4. Show me the full modified code for each file


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PROMPT 7 — EXPLAIN A SPECIFIC FILE
# Replace <filename> with any file you want to understand
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Explain this Python file from my FastAPI Industrial Safety project in simple terms.
Tell me: what it does, what each function/class does, and how it connects to the rest of the project.

[OPEN THE FILE IN VS CODE, SELECT ALL (Ctrl+A), THEN PASTE IT HERE]
