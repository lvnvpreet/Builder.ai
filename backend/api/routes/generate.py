"""
Website generation endpoints
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List
import uuid
import logging
import asyncio
from services.generation_service import generation_service

logger = logging.getLogger(__name__)
router = APIRouter()


class GenerationRequest(BaseModel):
    """Website generation request model"""
    business_name: str = Field(..., min_length=1, description="Name of the business")
    business_category: str = Field(..., min_length=1, description="Category/type of business")
    business_description: str = Field(..., min_length=1, description="Description of the business")
    target_audience: Optional[str] = Field(None, description="Target audience description")
    preferred_colors: Optional[List[str]] = Field(default=[], description="Preferred color schemes")
    additional_requirements: Optional[str] = Field(None, description="Additional requirements")


class GenerationResponse(BaseModel):
    """Website generation response model"""
    generation_id: str
    status: str
    message: str


@router.post("/", response_model=GenerationResponse)
async def create_website(request: GenerationRequest, background_tasks: BackgroundTasks):
    """
    Start website generation process
    """
    try:
        logger.info(f"Received generation request: {request.dict()}")
        
        # Validate required fields
        if not request.business_name.strip():
            raise HTTPException(status_code=422, detail="Business name is required")
        if not request.business_category.strip():
            raise HTTPException(status_code=422, detail="Business category is required")
        if not request.business_description.strip():
            raise HTTPException(status_code=422, detail="Business description is required")
        
        # Use the generation service instead of direct background task
        generation_id = await generation_service.start_generation(request.dict())
        
        return GenerationResponse(
            generation_id=generation_id,
            status="started",
            message="Website generation started. Use WebSocket connection to track progress."
        )
        
    except HTTPException:
        raise
    except asyncio.CancelledError:
        logger.warning("Generation request was cancelled")
        raise HTTPException(status_code=499, detail="Request was cancelled")
    except Exception as e:
        logger.error(f"Failed to start website generation: {e}")
        raise HTTPException(status_code=500, detail="Failed to start generation")


@router.get("/status/{generation_id}")
async def get_generation_status(generation_id: str):
    """Get the status of a generation request"""
    try:
        generation = await generation_service.get_generation_status(generation_id)
        if not generation:
            raise HTTPException(status_code=404, detail="Generation not found")
        
        return {
            "generation_id": generation_id,
            "status": generation.get("status", "unknown"),
            "progress": generation.get("progress", 0),
            "current_step": generation.get("current_step", ""),
            "errors": generation.get("errors", []),
            "completed_at": generation.get("completed_at")
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting generation status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/result/{generation_id}")
async def get_generation_result(generation_id: str):
    """Get the final website result"""
    try:
        generation = await generation_service.get_generation_status(generation_id)
        if not generation:
            raise HTTPException(status_code=404, detail="Generation not found")
        
        if generation.get("status") != "completed":
            if generation.get("status") == "failed":
                errors = generation.get("errors", ["Unknown error occurred"])
                raise HTTPException(status_code=422, detail={"errors": errors, "message": "Generation failed"})
            else:
                raise HTTPException(status_code=400, detail="Generation not completed yet")
        
        return {
            "generation_id": generation_id,
            "website": generation.get("final_website", {}),
            "metadata": generation.get("metadata", {}),
            "quality_report": generation.get("quality_report", {})
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting generation result: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{generation_id}")
async def get_generation_status_legacy(generation_id: str):
    """
    Get status of a specific generation (legacy endpoint)
    """
    try:
        logger.info(f"Getting status for generation ID: {generation_id}")
        
        # Use the generation service to get status
        status = await generation_service.get_generation_status(generation_id)
        
        if not status:
            raise HTTPException(status_code=404, detail="Generation not found")
        
        return status
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get generation status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get status")


async def generate_website_background(generation_id: str, request_data: dict):
    """
    Background task for website generation
    """
    try:
        logger.info(f"Starting website generation for ID: {generation_id}")
        
        # TODO: Implement LangGraph workflow execution
        # This will be implemented when we create the LangGraph components
        
        logger.info(f"Website generation completed for ID: {generation_id}")
        
    except Exception as e:
        logger.error(f"Website generation failed for ID {generation_id}: {e}")
