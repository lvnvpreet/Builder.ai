#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from workflows.workflow import WebsiteGenerationWorkflow
from core.state import GenerationState

def test_footer_fix():
    """Test the footer generation fix"""
    print("Testing footer generation with business_info...")
    
    # Create a test state
    state = GenerationState(
        generation_id="test-footer-fix",
        business_info={
            'business_name': 'Tech Solutions Pro',
            'business_category': 'Technology',
            'business_description': 'Professional IT consulting and software development services',
            'location': 'San Francisco, CA',
            'target_audience': 'Small to medium businesses'
        },
        content_data={
            'hero_headline': 'Professional IT Solutions',
            'hero_subtitle': 'Expert technology consulting for your business success',
            'hero_cta': 'Get Started',
            'about_headline': 'About Our Company',
            'about_content': 'We provide professional IT solutions.',
            'services_headline': 'Our Services',
            'services': [
                {
                    'name': 'IT Consulting',
                    'description': 'Strategic technology planning and implementation',
                    'icon_suggestion': 'laptop'
                }
            ],
            'contact_headline': 'Contact Us',
            'contact_content': 'Ready to transform your business with technology?',
            'footer_company_description': 'Tech Solutions Pro has been providing reliable IT services since 2010.',
            'footer_contact_info': {
                'address': '123 Tech Street, San Francisco, CA 94102',
                'phone': '(415) 555-TECH',
                'email': 'info@techsolutions.com',
                'hours': 'Mon-Fri 8AM-6PM'
            },
            'footer_services': ['IT Consulting', 'Software Development', 'Cloud Solutions', 'Tech Support'],
            'footer_areas': ['San Francisco', 'Bay Area', 'Silicon Valley'],
            'footer_social_links': {
                'linkedin': 'https://linkedin.com/company/techsolutions',
                'twitter': '@techsolutions',
                'facebook': 'https://facebook.com/techsolutions'
            },
            'meta_title': 'Tech Solutions Pro - IT Consulting San Francisco',
            'meta_description': 'Professional IT consulting and software development in San Francisco. Transform your business with expert technology solutions.'
        }
    )
    
    # Test the workflow
    workflow = WebsiteGenerationWorkflow()
    
    try:
        # Test footer generation directly
        footer_html = workflow._generate_footer_content(state["content_data"], state["business_info"])
        print("✅ Footer generation successful!")
        print(f"Footer HTML length: {len(footer_html)} characters")
        
        # Test full HTML generation
        html_content = workflow._generate_final_html(state)
        print("✅ Full HTML generation successful!")
        print(f"Full HTML length: {len(html_content)} characters")
        
        # Save test output
        with open('test_footer_fix_output.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ Test output saved to 'test_footer_fix_output.html'")
        
        # Check if business info is used correctly
        if 'Tech Solutions Pro' in html_content and 'San Francisco' in html_content:
            print("✅ Business info correctly integrated in footer!")
        else:
            print("❌ Business info not found in footer")
            
        return True
        
    except Exception as e:
        print(f"❌ Footer fix test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_footer_fix()
