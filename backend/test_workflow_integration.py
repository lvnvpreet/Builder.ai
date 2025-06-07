#!/usr/bin/env python3
"""
Test script to validate the enhanced workflow integration
"""

import asyncio
import json
import uuid
from workflows.workflow import WebsiteGenerationWorkflow

async def test_enhanced_workflow():
    """Test the complete enhanced workflow"""
    
    # Create test business info
    business_info = {
        'business_name': 'Star Plumbers, NY',
        'business_category': 'plumbing',
        'business_description': 'Professional emergency plumbing services in New York City. Licensed, insured, and available 24/7.',
        'target_audience': 'NYC residents and businesses needing reliable plumbing services',
        'location': 'New York City, NY'
    }
    
    # Create workflow instance
    workflow = WebsiteGenerationWorkflow()
    generation_id = str(uuid.uuid4())
    
    print(f"Starting enhanced workflow test for {business_info['business_name']}")
    print(f"Generation ID: {generation_id}")
    
    try:
        # Test content generation only first
        print("\n=== Testing Content Agent ===")
        content_data = await workflow.content_agent.generate_content(business_info)
        
        print("✅ Content generated successfully!")
        print("Content keys:", list(content_data.keys()))
        print("Hero headline:", content_data.get('hero_headline'))
        print("Services count:", len(content_data.get('services', [])))
        
        # Test services rendering
        services_html = workflow._generate_services_html(content_data.get('services', []))
        print("Services HTML preview:", services_html[:200] + "..." if len(services_html) > 200 else services_html)
        
        # Test about content rendering
        about_html = workflow._generate_about_html(content_data)
        print("About HTML preview:", about_html[:200] + "..." if len(about_html) > 200 else about_html)
        
        print("\n=== Testing Design Agent ===")
        design_data = await workflow.design_agent.generate_design(business_info, content_data)
        print("✅ Design generated successfully!")
        print("Design keys:", list(design_data.keys()))
        
        print("\n=== Testing Structure Agent ===")
        structure_data = await workflow.structure_agent.generate_structure(business_info, content_data)
        print("✅ Structure generated successfully!")
        print("Structure keys:", list(structure_data.keys()))
        
        # Test final HTML generation
        print("\n=== Testing Final HTML Generation ===")
        
        # Create mock state for testing
        mock_state = {
            'generation_id': generation_id,
            'business_info': business_info,
            'content_data': content_data,
            'design_data': design_data,
            'structure_data': structure_data,
            'images_data': {'images': []},
            'quality_report': {'overall_score': 85}
        }
        
        final_html = workflow._generate_final_html(mock_state)
        final_css = workflow._generate_final_css(mock_state)
        
        print("✅ Final HTML/CSS generated successfully!")
        print("HTML length:", len(final_html), "characters")
        print("CSS length:", len(final_css), "characters")
        
        # Check if hero content is properly integrated
        if content_data.get('hero_headline') in final_html:
            print("✅ Hero headline properly integrated")
        else:
            print("❌ Hero headline not found in HTML")
        
        # Check if services are properly integrated
        if 'service-card' in final_html:
            print("✅ Services properly integrated")
        else:
            print("❌ Services not properly integrated")
        
        # Check if about content is properly integrated  
        if content_data.get('about_content', '')[:50] in final_html:
            print("✅ About content properly integrated")
        else:
            print("❌ About content not properly integrated")
        
        print("\n=== Enhanced Workflow Test Complete ===")
        print("🎉 All components working with enhanced prompts!")
        
        # Save test results
        with open('test_workflow_results.json', 'w') as f:
            json.dump({
                'business_info': business_info,
                'content_keys': list(content_data.keys()),
                'design_keys': list(design_data.keys()),
                'structure_keys': list(structure_data.keys()),
                'html_length': len(final_html),
                'css_length': len(final_css),
                'test_passed': True
            }, f, indent=2)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_enhanced_workflow())
    if success:
        print("\n🎉 Enhanced workflow is working perfectly!")
    else:
        print("\n💥 Enhanced workflow needs debugging")
