"""
Test script to verify the improved content parsing functionality
"""

import asyncio
from agents.content_agent import ContentAgent
from core.logging import setup_logging

# Sample business info
TEST_BUSINESS_INFO = {
    "business_name": "Star Plumbers, NY",
    "business_category": "Plumbing Services",
    "business_description": "Professional plumbing services for residential and commercial clients in NYC.",
    "target_audience": "Home owners and businesses in New York City"
}

# Sample responses with varying JSON quality
TEST_RESPONSES = [
    # Well-formatted JSON response
    """{
      "hero_headline": "Star Plumbers: NYC's Most Trusted Plumbing Experts",
      "hero_subtitle": "Fast, Reliable Solutions for All Your Plumbing Needs",
      "about_content": "Star Plumbers has been serving New York City for over 15 years with expert plumbing services. Our licensed and insured team brings unparalleled expertise to every job, from emergency repairs to complete plumbing system installations. We pride ourselves on quick response times, transparent pricing, and the highest quality workmanship.",
      "services": ["Emergency Plumbing Repair", "Pipe Installation & Replacement", "Drain Cleaning", "Water Heater Services"],
      "contact_content": "Available 24/7 for emergencies. Call us at (555) 123-4567 or fill out our form for a free estimate.",
      "meta_title": "Star Plumbers NYC | Professional Plumbing Services | 24/7 Emergency Repairs",
      "meta_description": "NYC's top-rated plumbing service specializing in emergency repairs, installations, and maintenance for residential and commercial properties. Available 24/7."
    }""",
    
    # Malformed JSON with missing fields
    """{
      "headline": "Expert Plumbing Services in NYC",
      "subtitle": "Professional & Reliable Solutions",
      "about": "Star Plumbers provides expert services in New York City. Our team is dedicated to excellence.",
      "services": ["Emergency Repairs", "Installation", "Maintenance"]
    }""",
    
    # Not proper JSON but text with labels
    """
    Hero Headline: Top-Rated Plumbing Professionals in New York
    Hero Subtitle: Professional plumbing when you need it most
    
    About Content:
    Star Plumbers has been serving the NYC area with distinction for over a decade. Our team consists of certified professionals who are ready to tackle any plumbing issue, big or small. We pride ourselves on our quick response times and quality workmanship.
    
    Services:
    1. Emergency plumbing repairs
    2. Drain cleaning and unclogging
    3. Fixture installation and repair
    4. Water heater services
    
    Contact Content:
    Call us today at (555) 987-6543 for a free consultation or emergency service.
    
    Meta Title: Star Plumbers - NYC's Premier Plumbing Service
    Meta Description: Professional plumbing services for residential and commercial properties in NYC. Fast response times and quality work guaranteed.
    """,
    
    # Completely unstructured text
    """
    Star Plumbers offers the best plumbing services in New York City. We handle everything from emergency repairs to new installations. Our team of experienced professionals is available 24/7 to address your plumbing needs. Contact us today to schedule an appointment or for emergency services.
    """
]

async def test_content_parsing():
    # Setup logging
    setup_logging()
    
    # Create content agent
    content_agent = ContentAgent()
    
    # Test parsing with different response types
    for i, response in enumerate(TEST_RESPONSES):
        print(f"\n--- Testing Response #{i+1} ---")
        try:
            result = content_agent._parse_content_response(response)
            print(f"Successfully parsed content with {len(result)} fields")
            for key, value in result.items():
                print(f"  {key}: {value[:50]}..." if isinstance(value, str) else f"  {key}: {value}")
        except Exception as e:
            print(f"Error parsing response: {e}")
    
    print("\nTesting complete!")

if __name__ == "__main__":
    asyncio.run(test_content_parsing())
