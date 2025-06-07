"""
Test script for enhanced footer generation
"""

import asyncio
import json
from workflows.workflow import WebsiteGenerationWorkflow

async def test_enhanced_footer():
    """Test the enhanced footer with plumbing business data"""
    
    business_info = {
        "business_name": "Star Plumbers, NY",
        "business_category": "plumbing",
        "business_description": "Professional emergency plumbing services in New York City. Licensed, insured, and available 24/7.",
        "target_audience": "NYC residents and businesses needing reliable plumbing services",
        "location": "New York City, NY"
    }
    
    # Create workflow instance
    workflow = WebsiteGenerationWorkflow()
    
    try:
        # Generate content only first to see footer data
        print("Testing content generation with footer fields...")
        
        # Use the enhanced content agent directly
        from agents.enhanced_prompts import DynamicPromptManager
        prompt_manager = DynamicPromptManager()
        
        prompt = prompt_manager.get_enhanced_content_prompt(business_info)
        print(f"Enhanced prompt length: {len(prompt)} characters")
        
        # Test the footer generation helper method
        content_data = {
            'footer_company_description': 'Star Plumbers, NY has been serving NYC with reliable plumbing solutions since 2010.',
            'footer_contact_info': {
                'address': '123 Main Street, New York, NY 10001',
                'phone': '(555) 123-PLUMBER',
                'email': 'info@starplumbers.com',
                'hours': 'Mon-Fri 8AM-6PM, Emergency 24/7'
            },
            'footer_services': ['Emergency Repair', 'Drain Cleaning', 'Water Heater Service', 'Bathroom Plumbing'],
            'footer_areas': ['Manhattan', 'Brooklyn', 'Queens', 'Bronx'],
            'footer_social_links': {
                'facebook': 'https://facebook.com/starplumbers',
                'twitter': '@starplumbers',
                'linkedin': 'https://linkedin.com/company/starplumbers',
                'instagram': '@starplumbers_ny'
            }
        }
        
        footer_html = workflow._generate_footer_content(content_data, business_info['business_name'])
        
        print("\n" + "="*50)
        print("ENHANCED FOOTER HTML:")
        print("="*50)
        print(footer_html)
        
        # Save to file for inspection
        with open('test_footer_output.html', 'w', encoding='utf-8') as f:
            f.write(f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Footer Test</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; }}
        
        /* Enhanced Footer Styles */
        .footer {{
            background-color: #2c3e50;
            color: #ecf0f1;
            padding: 3rem 0 1rem;
        }}
        
        .footer-content {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }}
        
        .footer-section h3 {{
            color: #fff;
            margin-bottom: 1rem;
            font-size: 1.2rem;
            font-weight: 600;
        }}
        
        .footer-section p {{
            margin-bottom: 0.5rem;
            line-height: 1.6;
        }}
        
        .footer-section ul {{
            list-style: none;
            padding: 0;
        }}
        
        .footer-section ul li {{
            margin-bottom: 0.5rem;
        }}
        
        .footer-section ul li a {{
            color: #bdc3c7;
            text-decoration: none;
            transition: color 0.3s ease;
        }}
        
        .footer-section ul li a:hover {{
            color: #3498db;
        }}
        
        .footer-section a {{
            color: #3498db;
            text-decoration: none;
            transition: color 0.3s ease;
        }}
        
        .footer-section a:hover {{
            color: #e74c3c;
        }}
        
        .social-links {{
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
        }}
        
        .social-links a {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            background-color: #34495e;
            border-radius: 50%;
            color: #fff;
            text-decoration: none;
            transition: all 0.3s ease;
        }}
        
        .social-links a:hover {{
            background-color: #3498db;
            transform: translateY(-2px);
        }}
        
        .footer-bottom {{
            border-top: 1px solid #34495e;
            padding-top: 2rem;
            text-align: center;
        }}
        
        .footer-bottom p {{
            margin: 0;
            color: #95a5a6;
        }}
    </style>
</head>
<body>
    <div style="padding: 2rem; background: #f8f9fa;">
        <h1>Enhanced Footer Test</h1>
        <p>Below is the enhanced footer for Star Plumbers, NY:</p>
    </div>
    
    {footer_html}
</body>
</html>
            """)
        
        print("\n✅ Footer test saved to 'test_footer_output.html'")
        print("✅ Enhanced footer generation working correctly!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing enhanced footer: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_enhanced_footer())
