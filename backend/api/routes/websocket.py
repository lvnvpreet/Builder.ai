"""
WebSocket endpoints for real-time communication
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, BackgroundTasks, Depends
import json
import logging
import asyncio
import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)
router = APIRouter()


class ConnectionManager:
    """WebSocket connection manager"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.generation_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("New WebSocket connection established")
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        
        # Remove from generation-specific connections
        for generation_id, connections in list(self.generation_connections.items()):
            if websocket in connections:
                connections.remove(websocket)
                # Clean up empty lists
                if not connections:
                    del self.generation_connections[generation_id]
                break
        
        logger.info("WebSocket connection closed")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to specific connection"""
        try:
            await websocket.send_text(json.dumps(message))
            return True
        except Exception as e:
            logger.error(f"Failed to send personal message: {e}")
            return False
    
    async def send_generation_update(self, generation_id: str, message: dict):
        """Send update to all connections tracking a specific generation"""
        if generation_id not in self.generation_connections:
            # No active connections for this generation
            return
            
        failed_connections = []
        for connection in self.generation_connections[generation_id]:
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Failed to send update to connection: {e}")
                failed_connections.append(connection)
        
        # Clean up failed connections
        for connection in failed_connections:
            if connection in self.generation_connections[generation_id]:
                self.generation_connections[generation_id].remove(connection)
    
    def subscribe_to_generation(self, generation_id: str, websocket: WebSocket):
        """Subscribe connection to generation updates"""
        if generation_id not in self.generation_connections:
            self.generation_connections[generation_id] = []
        if websocket not in self.generation_connections[generation_id]:
            self.generation_connections[generation_id].append(websocket)
            logger.info(f"Client subscribed to generation {generation_id}")


# Global connection manager
manager = ConnectionManager()


@router.websocket("/generation/{generation_id}")
async def websocket_generation_endpoint(websocket: WebSocket, generation_id: str, background_tasks: BackgroundTasks):
    """
    WebSocket endpoint for tracking generation progress
    """
    await manager.connect(websocket)
    manager.subscribe_to_generation(generation_id, websocket)
    
    # Send initial connection confirmation
    await manager.send_personal_message(
        {
            "type": "connection",
            "message": f"Connected to generation {generation_id}",
            "generation_id": generation_id,
            "timestamp": datetime.datetime.now().isoformat()
        },
        websocket
    )
    
    # Send initial status update for this generation
    background_tasks.add_task(send_initial_status, generation_id, websocket)
    
    try:
        # Keep connection alive and handle incoming messages
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                
                # Handle different message types
                if message.get("type") == "ping":
                    await manager.send_personal_message(
                        {"type": "pong", "timestamp": datetime.datetime.now().isoformat()},
                        websocket
                    )
            except json.JSONDecodeError:
                logger.warning(f"Received invalid JSON: {data}")
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info(f"Client disconnected from generation {generation_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)


async def send_initial_status(generation_id: str, websocket: WebSocket):
    """
    Send initial status for a generation when a client connects
    This runs as a background task to avoid blocking the WebSocket connection
    """
    try:
        from services.generation_service import generation_service
        
        # Get current generation status from the database
        generation = await generation_service.get_generation_status(generation_id)
        if generation:
            # Send current status
            await manager.send_personal_message(
                {
                    "type": "progress_update",
                    "generation_id": generation_id,
                    "progress": generation.get("progress", 0),
                    "step": generation.get("current_step", "Unknown"),
                    "timestamp": datetime.datetime.now().isoformat()
                },
                websocket
            )
    except Exception as e:
        logger.error(f"Failed to send initial status for {generation_id}: {e}")
