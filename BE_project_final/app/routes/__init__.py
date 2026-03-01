from app.routes.auth import router as auth_router
from app.routes.sensors import router as sensors_router
from app.routes.alerts import router as alerts_router
from app.routes.ai import router as ai_router
from app.routes.websocket import router as ws_router

__all__ = ["auth_router", "sensors_router", "alerts_router", "ai_router", "ws_router"]
