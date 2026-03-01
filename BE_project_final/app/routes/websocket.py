"""
WebSocket route — real-time live sensor feed.
Clients connect and receive new sensor readings as they arrive.
"""

import asyncio
import json
import logging
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ws", tags=["WebSocket"])


class ConnectionManager:
    """Manages active WebSocket connections."""

    def __init__(self) -> None:
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        self.active.append(ws)
        logger.info("WebSocket client connected. Total: %d", len(self.active))

    def disconnect(self, ws: WebSocket) -> None:
        self.active.remove(ws)
        logger.info("WebSocket client disconnected. Total: %d", len(self.active))

    async def broadcast(self, data: Any) -> None:
        """Send data to all connected clients, removing dead connections."""
        dead: list[WebSocket] = []
        for ws in self.active:
            try:
                await ws.send_text(json.dumps(data))
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.active.remove(ws)


manager = ConnectionManager()


@router.websocket("/live")
async def live_feed(ws: WebSocket):
    """
    Connect to receive real-time sensor readings and alerts.

    Message format:
        {"type": "reading", "sensor_id": 1, "value": 42.5, "is_anomaly": false}
        {"type": "alert",   "severity": "CRITICAL", "title": "...", "zone": "..."}
    """
    await manager.connect(ws)
    try:
        while True:
            # Keep connection alive; actual pushes happen via manager.broadcast()
            await asyncio.sleep(30)
            await ws.send_text(json.dumps({"type": "ping"}))
    except WebSocketDisconnect:
        manager.disconnect(ws)
