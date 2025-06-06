"""
Health check endpoints
"""

from fastapi import APIRouter, Depends
from database.connection import get_database
from core.config import settings
import httpx
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "service": "AI Website Builder",
        "version": "1.0.0"
    }


@router.get("/detailed")
async def detailed_health_check():
    """Detailed health check including dependencies"""
    health_status = {
        "status": "healthy",
        "service": "AI Website Builder",
        "version": "1.0.0",
        "dependencies": {}
    }
      # Check MongoDB connection
    try:
        db = get_database()
        if db is not None:
            # Use the client's admin command to ping
            from database.connection import client
            if client is not None:
                await client.admin.command('ping')
                health_status["dependencies"]["mongodb"] = "healthy"
            else:
                health_status["dependencies"]["mongodb"] = "unhealthy"
                health_status["status"] = "degraded"
        else:
            health_status["dependencies"]["mongodb"] = "unhealthy"
            health_status["status"] = "degraded"
    except Exception as e:
        logger.error(f"MongoDB health check failed: {e}")
        health_status["dependencies"]["mongodb"] = "unhealthy"
        health_status["status"] = "degraded"
    
    # Check Ollama connection
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            if response.status_code == 200:
                health_status["dependencies"]["ollama"] = "healthy"
            else:
                health_status["dependencies"]["ollama"] = "unhealthy"
                health_status["status"] = "degraded"
    except Exception as e:
        logger.error(f"Ollama health check failed: {e}")
        health_status["dependencies"]["ollama"] = "unhealthy"
        health_status["status"] = "degraded"
    
    return health_status
