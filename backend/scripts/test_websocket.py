"""
Test script for website generation to troubleshoot WebSocket issues
"""

import asyncio
import json
import logging
import sys
import requests
from websockets.client import connect

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API URLs
API_URL = "http://localhost:8000/api/v1/generate"
WS_URL = "ws://localhost:8000/api/websocket/generation/"


async def monitor_generation(generation_id):
    """Monitor website generation using WebSockets"""
    websocket_url = f"{WS_URL}{generation_id}"
    logger.info(f"Connecting to WebSocket at {websocket_url}")
    
    async with connect(websocket_url) as websocket:
        # Wait for the initial connection message
        response = await websocket.recv()
        data = json.loads(response)
        logger.info(f"Initial connection: {data}")
        
        # Send a ping to test bidirectional communication
        await websocket.send(json.dumps({"type": "ping"}))
        
        # Monitor until complete or failed
        while True:
            try:
                response = await websocket.recv()
                data = json.loads(response)
                logger.info(f"Received update: {data}")
                
                # Check if generation is complete or failed
                if data.get("type") in ("generation_complete", "error"):
                    logger.info("Generation process ended")
                    break
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                break


async def start_generation():
    """Start a website generation and monitor its progress"""
    business_info = {
        "business_name": "Test Plumbers",
        "business_category": "Service",
        "business_description": "We provide quick plumbing services for homes and businesses",
        "target_audience": "homeowners and businesses",
        "preferred_colors": ["blue", "gray"]
    }
    
    try:
        # Start generation
        logger.info("Starting website generation...")
        response = requests.post(API_URL, json=business_info)
        response.raise_for_status()
        
        generation_data = response.json()
        generation_id = generation_data.get("generation_id")
        logger.info(f"Generation started with ID: {generation_id}")
        
        # Monitor using WebSockets
        await monitor_generation(generation_id)
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(start_generation())
    except KeyboardInterrupt:
        logger.info("Test cancelled by user")
        sys.exit(0)
