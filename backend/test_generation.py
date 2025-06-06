"""
Test script to verify the generation endpoint works properly
"""

import asyncio
import httpx
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_generation_endpoint():
    """Test the generation endpoint"""
    try:
        # Test data
        test_request = {
            "business_name": "Test Business",
            "business_category": "Technology",
            "business_description": "A test technology business",
            "target_audience": "Tech professionals",
            "preferred_colors": ["blue", "white"],
            "additional_requirements": "Modern and clean design"
        }
        
        # Make request to generation endpoint
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "http://localhost:8000/api/v1/generate/",
                json=test_request
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Generation started successfully: {result}")
                
                # Check status
                generation_id = result["generation_id"]
                status_response = await client.get(
                    f"http://localhost:8000/api/v1/generate/{generation_id}"
                )
                
                if status_response.status_code == 200:
                    status = status_response.json()
                    logger.info(f"Generation status: {status}")
                else:
                    logger.error(f"Failed to get status: {status_response.status_code}")
                    
            else:
                logger.error(f"Generation failed: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Test failed: {e}")


if __name__ == "__main__":
    asyncio.run(test_generation_endpoint())
