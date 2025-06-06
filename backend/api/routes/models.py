"""
AI Models management endpoints
"""

from fastapi import APIRouter, HTTPException
from core.config import settings
import httpx
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/status")
async def get_models_status():
    """
    Get status of all AI models
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            
            if response.status_code != 200:
                raise HTTPException(status_code=503, detail="Ollama service unavailable")
            
            models_data = response.json()
            available_models = [model["name"] for model in models_data.get("models", [])]
            
            # Check which required models are available
            required_models = [
                settings.CONTENT_MODEL,
                settings.DESIGN_MODEL,
                settings.STRUCTURE_MODEL
            ]
            
            model_status = {}
            for model in required_models:
                model_status[model] = {
                    "available": model in available_models,
                    "purpose": get_model_purpose(model)
                }
            
            return {
                "ollama_status": "online",
                "models": model_status,
                "total_models": len(available_models)
            }
            
    except httpx.RequestError as e:
        logger.error(f"Failed to connect to Ollama: {e}")
        raise HTTPException(status_code=503, detail="Ollama service unavailable")
    except Exception as e:
        logger.error(f"Failed to get models status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get models status")


@router.get("/download/{model_name}")
async def download_model(model_name: str):
    """
    Download a specific model
    """
    try:
        # TODO: Implement model downloading
        return {
            "message": f"Model {model_name} download started",
            "status": "downloading"
        }
    except Exception as e:
        logger.error(f"Failed to download model {model_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to download model")


def get_model_purpose(model_name: str) -> str:
    """Get the purpose of a model based on its name"""
    if "llama" in model_name.lower():
        return "Content Generation"
    elif "codellama" in model_name.lower():
        return "Design & CSS Generation"
    elif "mistral" in model_name.lower():
        return "Structure & HTML Generation"
    else:
        return "General Purpose"
