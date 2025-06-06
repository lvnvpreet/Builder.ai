"""
Website generation service
Orchestrates the complete website generation process
"""

import uuid
from typing import Dict, Optional
import logging
import asyncio
from datetime import datetime

from workflows.workflow import WebsiteGenerationWorkflow
from database.connection import get_database

logger = logging.getLogger(__name__)


class WebsiteGenerationService:
    """Service for managing website generation requests"""
    
    def __init__(self):
        self.workflow = WebsiteGenerationWorkflow()
    
    @property
    def db(self):
        """Get database instance dynamically"""
        database = get_database()
        if database is None:
            raise Exception("Database connection not available")
        return database
    
    async def start_generation(self, business_info: dict) -> str:
        """
        Start a new website generation process
        
        Args:
            business_info: Business information for generation
            
        Returns:
            Generation ID for tracking progress
        """
        try:
            generation_id = str(uuid.uuid4())
            logger.info(f"Starting generation process for ID: {generation_id}")
              # Store initial generation record in database
            generation_record = {
                "generation_id": generation_id,
                "business_info": business_info,
                "status": "started",
                "progress": 0,
                "current_step": "Initializing",
                "created_at": datetime.utcnow().isoformat() + "Z",
                "updated_at": datetime.utcnow().isoformat() + "Z",
                "errors": [],
                "final_website": None,
                "metadata": {},
                "quality_report": {}
            }
            
            result = await self.db.generations.insert_one(generation_record)
            logger.info(f"Created database record for generation {generation_id}: {result.inserted_id}")
            
            # Start generation workflow in background with proper error handling
            # Note: In production, this should be handled by a task queue
            task = asyncio.create_task(self._execute_generation(generation_id, business_info))
            # Add error handling for the background task
            task.add_done_callback(lambda t: self._handle_task_completion(t, generation_id))
            
            return generation_id
            
        except Exception as e:
            logger.error(f"Failed to start generation: {e}")
            raise

    def _handle_task_completion(self, task: asyncio.Task, generation_id: str):
        """Handle completion of background generation task"""
        try:
            if task.cancelled():
                logger.warning(f"Generation task cancelled for {generation_id}")
            elif task.exception():
                logger.error(f"Generation task failed for {generation_id}: {task.exception()}")
                # Try to update database with error if task failed unexpectedly
                asyncio.create_task(self._update_failed_generation(generation_id, str(task.exception())))
            else:
                logger.info(f"Generation task completed for {generation_id}")
        except Exception as e:
            logger.error(f"Error handling task completion for {generation_id}: {e}")
    async def _update_failed_generation(self, generation_id: str, error_message: str):
        """Update database when a generation task fails unexpectedly"""
        try:
            await self.db.generations.update_one(
                {"generation_id": generation_id},
                {
                    "$set": {
                        "status": "failed",
                        "errors": [error_message],
                        "failed_at": datetime.utcnow().isoformat() + "Z"
                    }
                }
            )
        except Exception as e:
            logger.error(f"Failed to update failed generation {generation_id}: {e}")
    
    async def _execute_generation(self, generation_id: str, business_info: dict):
        """
        Execute the generation workflow and send progress updates
        """
        try:
            logger.info(f"Starting generation workflow for {generation_id}")
            
            # Set a reasonable timeout for the entire generation process
            timeout_seconds = 600  # 10 minutes
            
            # Execute the LangGraph workflow with timeout
            final_state = await asyncio.wait_for(
                self.workflow.generate_website(generation_id, business_info),
                timeout=timeout_seconds
            )
              # Save final result to database
            await self.db.generations.update_one(
                {"generation_id": generation_id},
                {
                    "$set": {
                        "status": "completed" if not final_state["errors"] else "failed",
                        "progress": final_state["progress"],
                        "current_step": final_state["current_step"],
                        "final_website": final_state.get("final_website"),
                        "quality_report": final_state.get("quality_report"),
                        "errors": final_state["errors"],
                        "completed_at": datetime.utcnow().isoformat() + "Z"
                    }
                }
            )
            
            # Send completion notification via WebSocket
            try:
                from api.routes.websocket import manager
                await manager.send_generation_update(generation_id, {
                    "type": "generation_complete",
                    "generation_id": generation_id,
                    "status": "completed" if not final_state["errors"] else "failed",
                    "final_website": final_state.get("final_website"),
                    "quality_score": final_state.get("quality_report", {}).get("overall_score", 0)
                })
            except ImportError:
                logger.warning("WebSocket manager not available for notifications")
            
            logger.info(f"Generation workflow completed for {generation_id}")
            
        except asyncio.TimeoutError:
            logger.error(f"Generation workflow timed out for {generation_id}")
              # Update database with timeout error
            await self.db.generations.update_one(
                {"generation_id": generation_id},
                {
                    "$set": {
                        "status": "failed",
                        "errors": ["Generation timed out"],
                        "failed_at": datetime.utcnow().isoformat() + "Z"
                    }
                }
            )
            
            # Send timeout notification via WebSocket
            try:
                from api.routes.websocket import manager
                await manager.send_generation_update(generation_id, {
                    "type": "generation_error",
                    "generation_id": generation_id,
                    "error": "Generation timed out"
                })
            except ImportError:
                logger.warning("WebSocket manager not available for timeout notifications")
                
        except asyncio.CancelledError:
            logger.warning(f"Generation workflow cancelled for {generation_id}")
              # Update database with cancellation
            await self.db.generations.update_one(
                {"generation_id": generation_id},
                {
                    "$set": {
                        "status": "cancelled",
                        "errors": ["Generation was cancelled"],
                        "failed_at": datetime.utcnow().isoformat() + "Z"
                    }
                }
            )
            
            # Re-raise to properly handle cancellation
            raise
        except Exception as e:
            logger.error(f"Generation workflow failed for {generation_id}: {e}")
              # Update database with error
            await self.db.generations.update_one(
                {"generation_id": generation_id},
                {
                    "$set": {
                        "status": "failed",
                        "errors": [str(e)],
                        "failed_at": datetime.utcnow().isoformat() + "Z"
                    }
                }
            )
            
            # Send error notification via WebSocket
            try:
                from api.routes.websocket import manager
                await manager.send_generation_update(generation_id, {
                    "type": "generation_error",
                    "generation_id": generation_id,
                    "error": str(e)
                })
            except ImportError:
                logger.warning("WebSocket manager not available for error notifications")
    async def get_generation_status(self, generation_id: str) -> Optional[Dict]:
        """
        Get the current status of a generation
        
        Args:
            generation_id: ID of the generation to check
            
        Returns:
            Generation status data or None if not found
        """
        try:
            generation = await self.db.generations.find_one({"generation_id": generation_id})
            
            if generation:
                # Remove MongoDB _id field for JSON serialization
                generation.pop("_id", None)
                return generation
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get generation status for {generation_id}: {e}")
            return None
    async def get_generation_result(self, generation_id: str) -> Optional[Dict]:
        """
        Get final generation result from database
        
        Args:
            generation_id: ID of the generation
            
        Returns:
            Generation result data or None if not found
        """
        try:
            generation = await self.db.generations.find_one({"generation_id": generation_id})
            
            if generation:
                # Remove MongoDB _id field for JSON serialization
                generation.pop("_id", None)
                return generation
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting generation result for {generation_id}: {e}")
            return None

    async def get_completed_website(self, generation_id: str) -> Optional[Dict]:
        """
        Get the completed website data
        
        Args:
            generation_id: ID of the generation
            
        Returns:
            Website data or None if not found/completed
        """
        try:
            generation = await self.get_generation_status(generation_id)
            
            if generation and generation.get("status") == "completed":
                return generation.get("final_website")
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get completed website for {generation_id}: {e}")
            return None


# Global service instance
generation_service = WebsiteGenerationService()
