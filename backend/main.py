"""
AI Website Builder - Main Application Entry Point
FastAPI server with WebSocket support for real-time AI website generation
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import asyncio
import logging
from contextlib import asynccontextmanager

from api.routes import health, generate, models, websocket
from core.config import settings
from core.logging import setup_logging
from database.connection import init_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    setup_logging()
    await init_database()
    
    # Ensure uploads directories exist
    import os
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("uploads/websites", exist_ok=True)
    os.makedirs("uploads/images", exist_ok=True)
    
    # Log startup message
    logging.getLogger(__name__).info("Server started. Uploads directory initialized.")
    
    yield
    # Shutdown
    try:
        # Cancel any running tasks
        tasks = [task for task in asyncio.all_tasks() if not task.done()]
        if tasks:
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
    except Exception as e:
        logging.getLogger(__name__).error(f"Error during shutdown: {e}")


# Initialize FastAPI app
app = FastAPI(
    title="AI Website Builder",
    description="Multi-Agent AI System for Intelligent Website Generation",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(generate.router, prefix="/api/v1/generate", tags=["generation"])
app.include_router(models.router, prefix="/api/v1/models", tags=["models"])
app.include_router(websocket.router, prefix="/api/websocket", tags=["websocket"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Website Builder API",
        "version": "1.0.0",
        "status": "running"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
