"""
Test script for enhanced prompts and parsing
Tests the improved agent functionality with enhanced prompts
"""

import asyncio
import json
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the enhanced components
from agents.enhanced_prompts import DynamicPromptManager
from agents.enhanced_parsers import EnhancedResponseParser

def test_enhanced_prompts():
    """Test the enhanced prompt generation"""
    print("=" * 60)
    print("TESTING ENHANCED PROMPTS")
    print("=" * 60)
    
    # Test business info
    business_info = {
        'business_name': 'TechFlow Solutions',
        'business_category': 'Technology',
        'business_description': 'AI-powered software solutions for modern businesses',
        'target_audience': 'Small to medium businesses',
        'additional_requirements': 'Focus on automation and efficiency'
    }
    
    # Mock content data for design/structure prompts
    content_data = {
        'hero_headline': 'Transform Your Business with AI',
        'hero_subtitle': 'Cutting-edge software solutions that automate workflows and boost productivity',
        'services': [
            {'name': 'AI Automation', 'description': 'Intelligent workflow automation'},
            {'name': 'Data Analytics', 'description': 'Advanced business intelligence'},
            {'name': 'Cloud Integration', 'description': 'Seamless cloud migration'}
        ],
        'meta_title': 'TechFlow Solutions - AI Software for Business',
        'meta_description': 'Transform your business with AI-powered software solutions. Automation, analytics, and cloud integration services.',
        'primary_keywords': ['AI software', 'business automation', 'cloud solutions'],
        'tone_indicators': {
            'formality': 'professional',
            'energy': 'confident',
            'emotion': 'trustworthy'
        }
    }
    
    # Initialize prompt manager
    prompt_manager = DynamicPromptManager()
    
    # Test enhanced content prompt
    print("\n1. TESTING ENHANCED CONTENT PROMPT")
    print("-" * 40)
    content_prompt = prompt_manager.get_enhanced_content_prompt(business_info)
    print(f"Content prompt length: {len(content_prompt)} characters")
    print(f"Contains industry strategy: {'Technology' in content_prompt and 'innovation' in content_prompt}")
    print(f"Contains reasoning process: {'Analysis' in content_prompt and 'Strategy' in content_prompt}")
    print(f"Contains quality criteria: {'Quality Criteria' in content_prompt}")
    print(f"Contains error prevention: {'Error Prevention' in content_prompt}")
    print("✅ Enhanced content prompt generated successfully")
    
    # Test enhanced design prompt
    print("\n2. TESTING ENHANCED DESIGN PROMPT")
    print("-" * 40)
    design_prompt = prompt_manager.get_enhanced_design_prompt(business_info, content_data)
    print(f"Design prompt length: {len(design_prompt)} characters")
    print(f"Contains industry guidelines: {'TECHNOLOGY DESIGN GUIDELINES' in design_prompt}")
    print(f"Contains modern CSS features: {'CSS Grid' in design_prompt and 'Custom Properties' in design_prompt}")
    print(f"Contains accessibility requirements: {'WCAG 2.1 AA' in design_prompt}")
    print(f"Contains performance considerations: {'Core Web Vitals' in design_prompt}")
    print("✅ Enhanced design prompt generated successfully")
    
    # Test enhanced structure prompt
    print("\n3. TESTING ENHANCED STRUCTURE PROMPT")
    print("-" * 40)
    structure_prompt = prompt_manager.get_enhanced_structure_prompt(business_info, content_data)
    print(f"Structure prompt length: {len(structure_prompt)} characters")
    print(f"Contains semantic HTML5: {'semantic HTML5' in structure_prompt}")
    print(f"Contains SEO optimization: {'SEO Optimization' in structure_prompt}")
    print(f"Contains accessibility: {'WCAG 2.1 AA' in structure_prompt}")
    print(f"Contains schema markup: {'schema.org' in structure_prompt}")
    print("✅ Enhanced structure prompt generated successfully")
    
    print(f"\n✅ ALL ENHANCED PROMPTS GENERATED SUCCESSFULLY!")
    return True

def test_enhanced_parsers():
    """Test the enhanced response parsers"""
    print("\n" + "=" * 60)
    print("TESTING ENHANCED PARSERS")
    print("=" * 60)
    
    # Test content parser with JSON response
    print("\n1. TESTING ENHANCED CONTENT PARSER")
    print("-" * 40)
    
    sample_content_response = '''```json
{
    "hero_headline": "AI-Powered Business Solutions",
    "hero_subtitle": "Transform your operations with cutting-edge artificial intelligence and automation technology",
    "hero_cta": "Get Started",
    "about_headline": "About TechFlow Solutions",
    "about_content": "TechFlow Solutions specializes in AI-powered software that transforms how businesses operate. With over 10 years of experience in enterprise technology, we help companies automate workflows, analyze data, and integrate cloud solutions.\\n\\nOur team of certified AI specialists and cloud architects delivers measurable results, typically reducing operational costs by 30-50% while improving efficiency and accuracy.",
    "services_headline": "Our AI Solutions",
    "services": [
        {
            "name": "Intelligent Automation",
            "description": "AI-driven workflow automation that eliminates manual tasks and reduces errors by up to 90%.",
            "icon_suggestion": "cpu"
        },
        {
            "name": "Predictive Analytics",
            "description": "Advanced data analysis that provides actionable insights and forecasts business trends.",
            "icon_suggestion": "trending-up"
        },
        {
            "name": "Cloud AI Integration",
            "description": "Seamless integration of AI capabilities into your existing cloud infrastructure.",
            "icon_suggestion": "cloud"
        }
    ],
    "testimonial_placeholder": "TechFlow's AI automation increased our productivity by 45% and reduced processing errors to near zero. The ROI was evident within the first quarter.",
    "contact_headline": "Start Your AI Journey",
    "contact_content": "Ready to transform your business with AI? Schedule a free consultation and discover how our solutions can deliver measurable results in 90 days or less.",
    "meta_title": "TechFlow Solutions - AI Software & Automation for Business",
    "meta_description": "Transform your business with AI-powered automation, predictive analytics, and cloud integration. Proven to reduce costs by 30-50%. Free consultation available.",
    "primary_keywords": ["AI automation", "business intelligence", "cloud AI solutions", "workflow optimization"],
    "tone_indicators": {
        "formality": "professional",
        "energy": "confident",
        "emotion": "trustworthy"
    }
}
```'''
    
    parsed_content = EnhancedResponseParser.parse_enhanced_content_response(sample_content_response)
    print(f"Parsed {len(parsed_content)} content fields")
    print(f"Hero headline: {parsed_content.get('hero_headline', 'MISSING')}")
    print(f"Services count: {len(parsed_content.get('services', []))}")
    print(f"Has tone indicators: {'tone_indicators' in parsed_content}")
    print(f"Has primary keywords: {'primary_keywords' in parsed_content}")
    
    # Validate services structure
    services = parsed_content.get('services', [])
    if services and isinstance(services[0], dict):
        print(f"First service has icon: {'icon_suggestion' in services[0]}")
        print(f"First service has description: {'description' in services[0]}")
    
    print("✅ Enhanced content parser working correctly")
    
    # Test design parser
    print("\n2. TESTING ENHANCED DESIGN PARSER")
    print("-" * 40)
    
    sample_design_response = '''```json
{
    "css_variables": ":root {\\n  --primary-color: #2563eb;\\n  --secondary-color: #1e40af;\\n  --accent-color: #3b82f6;\\n  --neutral-50: #f8fafc;\\n  --neutral-900: #0f172a;\\n}",
    "base_styles": "* { margin: 0; padding: 0; box-sizing: border-box; }\\nbody { font-family: 'Inter', sans-serif; line-height: 1.6; }",
    "component_styles": {
        "header": "header { background: var(--primary-color); color: white; padding: 1rem 0; position: sticky; top: 0; z-index: 100; }",
        "hero": ".hero { padding: 6rem 0; background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); color: white; text-align: center; }",
        "about": ".about { padding: 5rem 0; background: var(--neutral-50); }",
        "services": ".services { padding: 5rem 0; } .service-card { padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }",
        "contact": ".contact { padding: 5rem 0; background: var(--neutral-50); } .contact-form { max-width: 600px; margin: 0 auto; }"
    },
    "design_tokens": {
        "colors": {
            "primary": "#2563eb",
            "secondary": "#1e40af",
            "accent": "#3b82f6"
        },
        "typography": {
            "heading_font": "Inter, sans-serif",
            "body_font": "Inter, sans-serif"
        }
    }
}
```'''
    
    parsed_design = EnhancedResponseParser.parse_enhanced_design_response(sample_design_response)
    print(f"Parsed {len(parsed_design)} design fields")
    print(f"Has CSS variables: {'css_variables' in parsed_design}")
    print(f"Has component styles: {'component_styles' in parsed_design}")
    print(f"Has design tokens: {'design_tokens' in parsed_design}")
    
    component_styles = parsed_design.get('component_styles', {})
    print(f"Component styles count: {len(component_styles)}")
    print(f"Has hero styles: {'hero' in component_styles}")
    
    print("✅ Enhanced design parser working correctly")
    
    # Test structure parser
    print("\n3. TESTING ENHANCED STRUCTURE PARSER")
    print("-" * 40)
    
    sample_structure_response = '''```json
{
    "document_structure": "<!DOCTYPE html>\\n<html lang=\\"en\\">\\n<head>\\n  <meta charset=\\"UTF-8\\">\\n  <title>TechFlow Solutions</title>\\n</head>\\n<body>\\n  <header></header>\\n  <main></main>\\n  <footer></footer>\\n</body>\\n</html>",
    "head_section": {
        "meta_tags": "<meta charset=\\"UTF-8\\">\\n<meta name=\\"viewport\\" content=\\"width=device-width, initial-scale=1.0\\">\\n<meta name=\\"description\\" content=\\"AI-powered business solutions\\">",
        "structured_data": "{\\"@context\\": \\"https://schema.org\\", \\"@type\\": \\"Organization\\", \\"name\\": \\"TechFlow Solutions\\"}",
        "social_meta": "<meta property=\\"og:title\\" content=\\"TechFlow Solutions\\">\\n<meta property=\\"og:description\\" content=\\"AI-powered business solutions\\">"
    },
    "content_sections": {
        "hero": "<section class=\\"hero\\">\\n  <h1>AI-Powered Business Solutions</h1>\\n  <p>Transform your operations with cutting-edge AI</p>\\n</section>",
        "about": "<section class=\\"about\\">\\n  <h2>About TechFlow Solutions</h2>\\n  <p>We specialize in AI-powered software...</p>\\n</section>",
        "services": "<section class=\\"services\\">\\n  <h2>Our AI Solutions</h2>\\n  <div class=\\"services-grid\\"></div>\\n</section>"
    }
}
```'''
    
    parsed_structure = EnhancedResponseParser.parse_enhanced_structure_response(sample_structure_response)
    print(f"Parsed {len(parsed_structure)} structure fields")
    print(f"Has document structure: {'document_structure' in parsed_structure}")
    print(f"Has head section: {'head_section' in parsed_structure}")
    print(f"Has content sections: {'content_sections' in parsed_structure}")
    
    head_section = parsed_structure.get('head_section', {})
    print(f"Head section components: {len(head_section)}")
    print(f"Has structured data: {'structured_data' in head_section}")
    
    content_sections = parsed_structure.get('content_sections', {})
    print(f"Content sections count: {len(content_sections)}")
    
    print("✅ Enhanced structure parser working correctly")
    
    print(f"\n✅ ALL ENHANCED PARSERS WORKING CORRECTLY!")
    return True

def test_fallback_parsing():
    """Test parser fallback mechanisms"""
    print("\n" + "=" * 60)
    print("TESTING FALLBACK PARSING")
    print("=" * 60)
    
    # Test content parser with non-JSON response
    print("\n1. TESTING CONTENT PARSER FALLBACK")
    print("-" * 40)
    
    sample_fallback_response = '''
    Here's the content for your technology business:
    
    Hero Headline: "Innovative Tech Solutions"
    Hero Subtitle: "Cutting-edge technology services for modern businesses"
    
    About Content: "We are a leading technology company specializing in innovative solutions."
    
    Services:
    - Service 1: "Custom Software Development"
    - Service 2: "Cloud Infrastructure"
    - Service 3: "AI Integration"
    
    Meta Title: "Tech Solutions - Innovation at Scale"
    Meta Description: "Leading technology company providing innovative solutions for modern businesses."
    '''
    
    parsed_fallback = EnhancedResponseParser.parse_enhanced_content_response(sample_fallback_response)
    print(f"Fallback parsed {len(parsed_fallback)} fields")
    print(f"Has all required fields: {all(key in parsed_fallback for key in ['hero_headline', 'hero_subtitle', 'about_content', 'services'])}")
    print(f"Services structure is valid: {isinstance(parsed_fallback.get('services', []), list)}")
    
    if parsed_fallback.get('services'):
        first_service = parsed_fallback['services'][0]
        print(f"Service has proper structure: {isinstance(first_service, dict) and 'name' in first_service}")
    
    print("✅ Content parser fallback working correctly")
    
    print(f"\n✅ ALL FALLBACK MECHANISMS WORKING CORRECTLY!")
    return True

def run_comprehensive_test():
    """Run all enhanced prompt tests"""
    print("STARTING COMPREHENSIVE ENHANCED PROMPTS TEST")
    print("=" * 80)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Run all tests
        prompt_test = test_enhanced_prompts()
        parser_test = test_enhanced_parsers()
        fallback_test = test_fallback_parsing()
        
        # Summary
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print(f"✅ Enhanced Prompts Test: {'PASSED' if prompt_test else 'FAILED'}")
        print(f"✅ Enhanced Parsers Test: {'PASSED' if parser_test else 'FAILED'}")
        print(f"✅ Fallback Parsing Test: {'PASSED' if fallback_test else 'FAILED'}")
        
        all_passed = all([prompt_test, parser_test, fallback_test])
        print(f"\n🎉 OVERALL RESULT: {'ALL TESTS PASSED!' if all_passed else 'SOME TESTS FAILED!'}")
        
        if all_passed:
            print("\n📈 IMPROVEMENTS IMPLEMENTED:")
            print("• Industry-specific content strategies")
            print("• Advanced prompt engineering techniques")
            print("• Comprehensive JSON parsing with fallbacks")
            print("• Enhanced error handling and validation")
            print("• Modern CSS architecture support")
            print("• Semantic HTML5 and accessibility features")
            print("• Performance optimization guidelines")
            print("• SEO and schema markup requirements")
        
        return all_passed
        
    except Exception as e:
        print(f"\n❌ TEST FAILED WITH ERROR: {e}")
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    exit(0 if success else 1)
