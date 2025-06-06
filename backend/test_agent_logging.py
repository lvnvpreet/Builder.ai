"""
Test script to verify agent-specific logging
"""

import asyncio
from core.logging import setup_logging, get_agent_logger
from core.config import settings
import os

async def test_agent_logging():
    # Setup logging
    setup_logging()
    
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(settings.AGENT_LOG_FILE), exist_ok=True)
    
    # Get loggers for each agent
    structure_logger = get_agent_logger('structure')
    content_logger = get_agent_logger('content')
    design_logger = get_agent_logger('design')
    image_logger = get_agent_logger('image')
    quality_logger = get_agent_logger('quality')
    
    # Log test messages
    structure_logger.info("Structure agent test log")
    structure_logger.debug("Structure agent debug message")
    structure_logger.warning("Structure agent warning")
    
    content_logger.info("Content agent test log")
    content_logger.debug("Content agent debug message")
    content_logger.warning("Content agent warning")
    
    design_logger.info("Design agent test log")
    design_logger.debug("Design agent debug message")
    design_logger.warning("Design agent warning")
    
    image_logger.info("Image agent test log")
    image_logger.debug("Image agent debug message")
    image_logger.warning("Image agent warning")
    
    quality_logger.info("Quality agent test log")
    quality_logger.debug("Quality agent debug message")
    quality_logger.warning("Quality agent warning")
    
    print(f"Test logs written to {settings.AGENT_LOG_FILE}")

if __name__ == "__main__":
    asyncio.run(test_agent_logging())
