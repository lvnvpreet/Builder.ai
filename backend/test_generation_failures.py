"""
Test script to verify proper failure handling when AI generation fails
"""

import asyncio
import httpx
import json
import logging
import uuid
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_failed_generation():
    """Test that failed generations properly propagate errors"""
    try:
        # Simulated data for a generation that should fail
        # This will help verify our error handling is working
        test_request = {
            "business_name": "ERROR_SIMULATION_TEST",
            "business_category": "Test",
            "business_description": "This is a test to simulate an AI generation failure",
            "target_audience": "Developers",
            "preferred_colors": [],
            "additional_requirements": "FORCE_ERROR_TEST" 
        }
        
        # Start a generation
        logger.info("Starting test generation that should fail...")
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "http://localhost:8000/api/v1/generate/",
                json=test_request
            )
            
            if response.status_code == 200:
                result = response.json()
                generation_id = result["generation_id"]
                logger.info(f"Test generation started with ID: {generation_id}")
                
                # Wait for the generation to complete/fail
                max_retries = 10
                retry_count = 0
                status = None
                
                while retry_count < max_retries:
                    await asyncio.sleep(5)  # Wait 5 seconds between status checks
                    status_response = await client.get(
                        f"http://localhost:8000/api/v1/generate/status/{generation_id}"
                    )
                    
                    if status_response.status_code == 200:
                        status = status_response.json()
                        current_status = status.get("status")
                        logger.info(f"Current status: {current_status}, progress: {status.get('progress', 0)}")
                        
                        # Check if generation has completed or failed
                        if current_status in ["completed", "failed"]:
                            break
                    else:
                        logger.error(f"Failed to get status: {status_response.status_code} - {status_response.text}")
                    
                    retry_count += 1
                
                # Verify final status
                if status and status.get("status") == "failed":
                    logger.info("SUCCESS: Generation properly failed as expected")
                    logger.info(f"Reported errors: {status.get('errors', [])}")
                    
                    # Try to get the result to test error handling in the result endpoint
                    result_response = await client.get(
                        f"http://localhost:8000/api/v1/generate/result/{generation_id}"
                    )
                    
                    if result_response.status_code == 422:
                        logger.info("SUCCESS: Result endpoint correctly returned 422 for failed generation")
                        logger.info(f"Error details: {result_response.json()}")
                    else:
                        logger.error(f"FAILED: Expected 422 status code, got {result_response.status_code}")
                        logger.error(f"Response: {result_response.text}")
                elif status and status.get("status") == "completed":
                    logger.error("FAILED: Generation completed successfully when it should have failed")
                else:
                    logger.error(f"FAILED: Unexpected final status: {status.get('status') if status else 'unknown'}")
            else:
                logger.error(f"Failed to start test generation: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Test failed with exception: {e}")


if __name__ == "__main__":
    asyncio.run(test_failed_generation())
