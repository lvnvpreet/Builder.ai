"""
Test script to verify improved agent-specific logging with separators
"""

import asyncio
import os
import uuid
from core.logging import setup_logging, get_agent_logger, log_generation_separator
from core.config import settings

async def test_improved_logging():
    # Setup logging
    setup_logging()
    
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(settings.AGENT_LOG_FILE), exist_ok=True)
    
    # Test with multiple website generations to verify separators
    for business_name in ["Test Bakery", "Sample Plumbing", "Demo Consulting"]:
        # Generate a unique session ID
        session_id = str(uuid.uuid4())
        
        # Log the generation separator
        log_generation_separator(website_name=business_name, session_id=session_id)
        
        # Get loggers for each agent
        structure_logger = get_agent_logger('structure')
        content_logger = get_agent_logger('content')
        design_logger = get_agent_logger('design')
        image_logger = get_agent_logger('image')
        quality_logger = get_agent_logger('quality')
        
        # Simulate agent logs for a generation
        content_logger.info(f"Starting content generation for {business_name}")
        content_logger.debug(f"Content prompt: Sample prompt for {business_name}")
        
        # Test error logging with different exception types
        try:
            # Simulate a connection error
            raise ConnectionError("Failed to connect to Ollama server")
        except Exception as e:
            content_logger.error(f"Content generation failed: {type(e).__name__} - {e}")
        
        # Continue with other agents
        design_logger.info(f"Starting design generation for {business_name}")
        structure_logger.info(f"Starting structure generation for {business_name}")
        image_logger.info(f"Starting image selection for {business_name}")
        
        # Log successful operations
        image_logger.info(f"Successfully selected images for {business_name}")
        design_logger.info(f"Successfully generated design for {business_name}")
        structure_logger.info("Structure generation successful")
        
        # Log quality validation
        quality_logger.info("Starting website quality validation")
        quality_logger.info(f"Quality validation completed with overall score: 85.5")
        
        # Small delay between "website generations"
        await asyncio.sleep(0.5)
    
    print(f"Test logs written to {settings.AGENT_LOG_FILE}")
    print("Check the log file to verify improved logging with clear separators between generations")

if __name__ == "__main__":
    asyncio.run(test_improved_logging())
