"""
Test script to verify agent output logging
This script will simulate output from each agent and log it
"""

import asyncio
import os
import json
from core.logging import setup_logging, get_agent_logger, log_generation_separator
from core.config import settings

async def test_agent_output_logging():
    # Setup logging
    setup_logging()
    
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(settings.AGENT_LOG_FILE), exist_ok=True)
    
    # Simulate a website generation
    business_name = "Test Business"
    session_id = "test-session-123"
    
    # Log the generation separator
    log_generation_separator(website_name=business_name, session_id=session_id)
    
    # Get loggers for each agent
    content_logger = get_agent_logger('content')
    design_logger = get_agent_logger('design')
    structure_logger = get_agent_logger('structure')
    image_logger = get_agent_logger('image')
    quality_logger = get_agent_logger('quality')
    workflow_logger = get_agent_logger('workflow')
    
    # Simulate content agent output
    content_logger.info(f"Starting content generation for {business_name}")
    content_output = {
        "hero_headline": "Professional Solutions for Your Business",
        "hero_subtitle": "Quality services tailored to your needs",
        "about_content": "Our company has been providing excellent services for over 10 years...",
        "services": ["Service 1", "Service 2", "Service 3"],
        "contact_content": "Reach out to us at contact@testbusiness.com",
        "meta_title": "Test Business - Professional Services",
        "meta_description": "We provide professional services for businesses of all sizes."
    }
    content_logger.info(f"Content output: {json.dumps(content_output)[:500]}...")
    
    # Simulate design agent output
    design_logger.info(f"Starting design generation for {business_name}")
    design_output = {
        "colors": {
            "primary": "#3f51b5",
            "secondary": "#f50057",
            "text": "#212121",
            "background": "#ffffff"
        },
        "fonts": {
            "headings": "Roboto, sans-serif",
            "body": "Open Sans, sans-serif"
        },
        "styles": {
            "header": "fixed top navigation with logo",
            "hero": "full-width with image background",
            "sections": "alternating color blocks"
        }
    }
    design_logger.info(f"Design output: {json.dumps(design_output)[:500]}...")
    
    # Simulate structure agent output
    structure_logger.info(f"Starting structure generation for {business_name}")
    structure_logger.info("Structure generation successful")
    structure_output = {
        "layout": "standard business layout",
        "sections": ["header", "hero", "about", "services", "testimonials", "contact", "footer"],
        "responsive": True,
        "navigation": "top fixed with hamburger menu on mobile"
    }
    structure_logger.info(f"Structure output: {json.dumps(structure_output)[:500]}...")
    
    # Simulate image agent output
    image_logger.info(f"Starting image selection for {business_name}")
    image_output = {
        "hero_image": {"url": "https://example.com/image1.jpg", "alt": "Professional team"},
        "about_image": {"url": "https://example.com/image2.jpg", "alt": "Office space"},
        "service_images": [
            {"url": "https://example.com/service1.jpg", "alt": "Service 1 illustration"},
            {"url": "https://example.com/service2.jpg", "alt": "Service 2 illustration"},
            {"url": "https://example.com/service3.jpg", "alt": "Service 3 illustration"}
        ]
    }
    image_logger.info(f"Image selection output: {json.dumps(image_output)[:500]}...")
    
    # Simulate quality agent output
    quality_logger.info("Starting website quality validation")
    quality_output = {
        "overall_score": 85.5,
        "content_validation": {"score": 90, "issues": [], "recommendations": ["Add more keywords"]},
        "design_validation": {"score": 85, "issues": [], "recommendations": []},
        "structure_validation": {"score": 88, "issues": [], "recommendations": []},
        "images_validation": {"score": 79, "issues": ["Some images might be slow to load"], "recommendations": ["Optimize images"]}
    }
    quality_logger.info(f"Quality issues found: {len(quality_output['content_validation']['issues'])}")
    quality_logger.info(f"Quality validation output: {json.dumps(quality_output)[:500]}...")
    
    # Simulate workflow final output
    workflow_logger.info("Generating final website")
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Business - Professional Services</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <nav>Menu goes here</nav>
    </header>
    <main>
        <section class="hero">Hero content</section>
    </main>
</body>
</html>"""
    
    css_content = """body {
    font-family: 'Open Sans', sans-serif;
    margin: 0;
    padding: 0;
    color: #212121;
}
header {
    background-color: #3f51b5;
    color: white;
    padding: 1rem;
}
"""
    workflow_logger.info(f"Final HTML (first 500 chars): {html_content[:500]}...")
    workflow_logger.info(f"Final CSS (first 500 chars): {css_content[:500]}...")
    
    print(f"Test logs written to {settings.AGENT_LOG_FILE}")
    print("Check the log file to verify that agent outputs are being logged")

if __name__ == "__main__":
    asyncio.run(test_agent_output_logging())
