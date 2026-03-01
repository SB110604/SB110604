"""
BE Project Final — Industrial Safety Monitoring System
FastAPI application entry point.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.config import get_settings
from app.core.database import Base, engine
from app.routes import auth_router, sensors_router, alerts_router, ai_router, ws_router

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# App bootstrap
# ---------------------------------------------------------------------------
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Creating database tables if they don't exist…")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database ready.")
    yield


app = FastAPI(
    title="Industrial Safety Monitoring System",
    description=(
        "Advanced AI-powered industrial safety platform with real-time sensor monitoring, "
        "anomaly detection, Twilio SMS alerts, and a live dashboard."
    ),
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS — restrict origins in production via ALLOWED_ORIGINS env var
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files & templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ---------------------------------------------------------------------------
# API routes
# ---------------------------------------------------------------------------
API_PREFIX = "/api/v1"

app.include_router(auth_router,    prefix=API_PREFIX)
app.include_router(sensors_router, prefix=API_PREFIX)
app.include_router(alerts_router,  prefix=API_PREFIX)
app.include_router(ai_router,      prefix=API_PREFIX)
app.include_router(ws_router)       # WebSocket — no versioned prefix

# ---------------------------------------------------------------------------
# Dashboard (served from templates/)
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(request, "dashboard.html")


@app.get("/health")
def health():
    return {"status": "ok", "env": settings.app_env}
