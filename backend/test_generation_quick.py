#!/usr/bin/env python3

import json
import os
from workflows.workflow import WebsiteWorkflow

def test_enhanced_generation():
    # Test business info
    business_info = {
        'business_name': 'Star Plumbers, NY',
        'business_category': 'plumbing',
        'business_description': 'Professional emergency plumbing services in New York City. Licensed, insured, and available 24/7.',
        'target_audience': 'NYC residents and businesses needing reliable plumbing services',
        'location': 'New York City, NY'
    }

    workflow = WebsiteWorkflow()
    result = workflow.run(business_info)

    # Save the generated files to see the actual output
    output_dir = 'test_generated_website'
    os.makedirs(output_dir, exist_ok=True)

    with open(f'{output_dir}/index.html', 'w', encoding='utf-8') as f:
        f.write(result['html'])

    with open(f'{output_dir}/styles.css', 'w', encoding='utf-8') as f:
        f.write(result['css'])

    print('Generated website saved to test_generated_website/')
    print(f'HTML length: {len(result["html"])}')
    print(f'CSS length: {len(result["css"])}')
    
    # Show a sample of the generated content
    print('\n--- Sample HTML (first 500 chars) ---')
    print(result['html'][:500])
    print('\n--- Sample CSS (first 500 chars) ---')
    print(result['css'][:500])

if __name__ == "__main__":
    test_enhanced_generation()
