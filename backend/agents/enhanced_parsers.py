"""
Enhanced parsing utilities for improved agent responses
Handles complex JSON structures from enhanced prompts
"""

import json
import re
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class EnhancedResponseParser:
    """Enhanced parser for handling complex AI responses with improved error handling"""
    
    @staticmethod
    def parse_enhanced_content_response(response: str) -> dict:
        """Parse enhanced content response with comprehensive field mapping"""
        
        # Default content structure matching enhanced prompt
        default_content = {
            "hero_headline": "Professional Business Solutions",
            "hero_subtitle": "Quality service you can trust with proven results",
            "hero_cta": "Get Started",
            "about_headline": "About Our Company",
            "about_content": "We are a professional business dedicated to providing excellent services to our clients. With years of experience in the industry, our team is committed to delivering high-quality results that exceed expectations.\n\nOur commitment to excellence and customer satisfaction sets us apart from the competition. We pride ourselves on building long-term relationships with our clients through transparent communication and reliable service delivery.",
            "services_headline": "Our Services",
            "services": [
                {
                    "name": "Professional Service 1",
                    "description": "High-quality service designed to meet your specific needs with proven results and expert guidance.",
                    "icon_suggestion": "briefcase"
                },
                {
                    "name": "Expert Service 2", 
                    "description": "Comprehensive solutions that deliver measurable value and long-term success for your business.",
                    "icon_suggestion": "star"
                },
                {
                    "name": "Premium Service 3",
                    "description": "Specialized expertise that transforms challenges into opportunities with innovative approaches.",
                    "icon_suggestion": "target"
                }
            ],
            "testimonial_placeholder": "Working with this team has been transformative for our business. Their expertise and dedication resulted in a 40% increase in our efficiency and significant cost savings.",
            "contact_headline": "Get In Touch",
            "contact_content": "Ready to take the next step? Contact us today for a free consultation and discover how we can help transform your business with our proven solutions.",
            "meta_title": "Professional Business Services - Quality Solutions",
            "meta_description": "Expert business services with proven results. Contact us today for a free consultation and discover how we can help transform your business with quality solutions.",
            "primary_keywords": ["professional services", "business solutions", "expert consultation", "quality service"],
            "tone_indicators": {
                "formality": "professional",
                "energy": "confident",
                "emotion": "trustworthy"
            }
        }
        
        try:
            # Method 1: Try to extract JSON from response
            json_blocks = re.findall(r'```json\s*([\s\S]*?)\s*```|({[\s\S]*})', response, re.IGNORECASE)
            
            for json_block in json_blocks:
                json_str = json_block[0] if json_block[0] else json_block[1]
                if not json_str:
                    continue
                    
                try:
                    parsed_json = json.loads(json_str)
                    if isinstance(parsed_json, dict) and len(parsed_json) > 5:
                        # Validate required fields exist
                        required_fields = ["hero_headline", "hero_subtitle", "about_content", "services"]
                        if all(field in parsed_json for field in required_fields):
                            # Ensure services have proper structure
                            if "services" in parsed_json and isinstance(parsed_json["services"], list):
                                for service in parsed_json["services"]:
                                    if isinstance(service, dict):
                                        if "icon_suggestion" not in service:
                                            service["icon_suggestion"] = "star"
                                    elif isinstance(service, str):
                                        # Convert string services to proper structure
                                        parsed_json["services"] = [
                                            {
                                                "name": svc if isinstance(svc, str) else str(svc),
                                                "description": f"Professional {svc.lower()} service with expert guidance and proven results.",
                                                "icon_suggestion": "star"
                                            } for svc in parsed_json["services"]
                                        ]
                                        break
                            
                            # Fill in missing fields with defaults
                            for key, default_value in default_content.items():
                                if key not in parsed_json:
                                    parsed_json[key] = default_value
                                    
                            logger.info("Successfully parsed enhanced JSON content from response")
                            return parsed_json
                            
                except json.JSONDecodeError:
                    continue
            
            # Method 2: Regex extraction with enhanced field mapping
            logger.info("No valid JSON found, attempting regex extraction")
            extracted_data = {}
            
            # Enhanced field patterns
            field_patterns = {
                "hero_headline": [r'(?:hero_headline|headline|title)[:\s]+"?([^"]+?)"?(?:\n|\r|,|})', r'Hero\s*Headline[:\s]*"?([^"]+?)"?(?:\n|\r|,|})', r'Main\s*Headline[:\s]*"?([^"]+?)"?(?:\n|\r|,|})'],
                "hero_subtitle": [r'(?:hero_subtitle|subtitle|tagline)[:\s]+"?([^"]+?)"?(?:\n|\r|,|})', r'Hero\s*Subtitle[:\s]*"?([^"]+?)"?(?:\n|\r|,|})'],
                "hero_cta": [r'(?:hero_cta|cta|call_to_action)[:\s]+"?([^"]+?)"?(?:\n|\r|,|})', r'Call.*Action[:\s]*"?([^"]+?)"?(?:\n|\r|,|})'],
                "about_headline": [r'(?:about_headline|about_title)[:\s]+"?([^"]+?)"?(?:\n|\r|,|})', r'About\s*Headline[:\s]*"?([^"]+?)"?(?:\n|\r|,|})'],
                "about_content": [r'(?:about_content|about)[:\s]+"?([^"]+?)"?(?:\n|\r|,|})', r'About\s*Content[:\s]*"?([^"]+?)"?(?:\n|\r|,|})'],
                "services_headline": [r'(?:services_headline|services_title)[:\s]+"?([^"]+?)"?(?:\n|\r|,|})', r'Services\s*Headline[:\s]*"?([^"]+?)"?(?:\n|\r|,|})'],
                "contact_headline": [r'(?:contact_headline|contact_title)[:\s]+"?([^"]+?)"?(?:\n|\r|,|})', r'Contact\s*Headline[:\s]*"?([^"]+?)"?(?:\n|\r|,|})'],
                "contact_content": [r'(?:contact_content|contact)[:\s]+"?([^"]+?)"?(?:\n|\r|,|})', r'Contact\s*Content[:\s]*"?([^"]+?)"?(?:\n|\r|,|})'],
                "meta_title": [r'(?:meta_title|seo_title)[:\s]+"?([^"]+?)"?(?:\n|\r|,|})', r'Meta\s*Title[:\s]*"?([^"]+?)"?(?:\n|\r|,|})'],
                "meta_description": [r'(?:meta_description|seo_description)[:\s]+"?([^"]+?)"?(?:\n|\r|,|})', r'Meta\s*Description[:\s]*"?([^"]+?)"?(?:\n|\r|,|})'],
                "testimonial_placeholder": [r'(?:testimonial_placeholder|testimonial)[:\s]+"?([^"]+?)"?(?:\n|\r|,|})', r'Testimonial[:\s]*"?([^"]+?)"?(?:\n|\r|,|})']
            }
            
            # Extract each field using multiple patterns
            for field, patterns in field_patterns.items():
                for pattern in patterns:
                    match = re.search(pattern, response, re.IGNORECASE | re.DOTALL)
                    if match:
                        extracted_data[field] = match.group(1).strip()
                        break
            
            # Extract services with enhanced structure
            services = []
            # Try to find services array first
            services_array_match = re.search(r'services[:\s]*\[([\s\S]*?)\]', response, re.IGNORECASE)
            if services_array_match:
                services_content = services_array_match.group(1)
                # Parse individual service objects
                service_objects = re.findall(r'\{([^}]+)\}', services_content)
                for obj in service_objects:
                    service = {}
                    name_match = re.search(r'(?:name|service)[:\s]*"?([^",]+)"?', obj, re.IGNORECASE)
                    desc_match = re.search(r'(?:description|desc)[:\s]*"?([^",]+)"?', obj, re.IGNORECASE)
                    icon_match = re.search(r'(?:icon_suggestion|icon)[:\s]*"?([^",]+)"?', obj, re.IGNORECASE)
                    
                    if name_match:
                        service["name"] = name_match.group(1).strip()
                        service["description"] = desc_match.group(1).strip() if desc_match else f"Professional {service['name'].lower()} service with expert guidance."
                        service["icon_suggestion"] = icon_match.group(1).strip() if icon_match else "star"
                        services.append(service)
            
            # Fallback: extract simple service list
            if not services:
                service_matches = re.findall(r'(?:Service|Offering)\s*\d*[:\s]*"?([^"]+?)"?(?:\n|\r|,)', response, re.IGNORECASE)
                for i, service_name in enumerate(service_matches[:4]):  # Limit to 4 services
                    services.append({
                        "name": service_name.strip(),
                        "description": f"Professional {service_name.lower()} service with expert guidance and proven results.",
                        "icon_suggestion": ["briefcase", "star", "target", "shield"][i] if i < 4 else "star"
                    })
            
            if services:
                extracted_data["services"] = services
            
            # Extract keywords
            keywords_match = re.search(r'(?:primary_keywords|keywords)[:\s]*\[([\s\S]*?)\]', response, re.IGNORECASE)
            if keywords_match:
                keywords_content = keywords_match.group(1)
                keywords = re.findall(r'"([^"]+)"', keywords_content)
                if keywords:
                    extracted_data["primary_keywords"] = keywords
            
            # Extract tone indicators
            tone_match = re.search(r'tone_indicators[:\s]*\{([^}]+)\}', response, re.IGNORECASE)
            if tone_match:
                tone_content = tone_match.group(1)
                tone_obj = {}
                for indicator in ["formality", "energy", "emotion"]:
                    pattern = f'{indicator}[:\s]*"?([^",]+)"?'
                    match = re.search(pattern, tone_content, re.IGNORECASE)
                    if match:
                        tone_obj[indicator] = match.group(1).strip()
                if tone_obj:
                    extracted_data["tone_indicators"] = tone_obj
            
            # Merge with defaults
            final_content = default_content.copy()
            final_content.update(extracted_data)
            
            logger.info(f"Successfully extracted {len(extracted_data)} fields via regex")
            return final_content
            
        except Exception as e:
            logger.error(f"Failed to parse enhanced content response: {e}")
            return default_content

    @staticmethod 
    def parse_enhanced_design_response(response: str) -> dict:
        """Parse enhanced design response with comprehensive CSS extraction"""
        
        default_design = {
            "css_variables": ":root {\n  --primary-color: #2563eb;\n  --secondary-color: #1e40af;\n  --accent-color: #3b82f6;\n}",
            "base_styles": "* { margin: 0; padding: 0; box-sizing: border-box; }",
            "layout_styles": ".container { max-width: 1200px; margin: 0 auto; padding: 0 1rem; }",
            "component_styles": {
                "header": "header { background: var(--primary-color); color: white; padding: 1rem 0; }",
                "hero": ".hero { padding: 4rem 0; text-align: center; background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); }",
                "about": ".about { padding: 4rem 0; }",
                "services": ".services { padding: 4rem 0; background: #f8fafc; }",
                "testimonials": ".testimonials { padding: 4rem 0; }",
                "contact": ".contact { padding: 4rem 0; background: #f8fafc; }",
                "footer": "footer { background: #1f2937; color: white; padding: 2rem 0; }"
            },
            "responsive_styles": "@media (max-width: 768px) { .container { padding: 0 0.5rem; } }",
            "animation_styles": ".btn { transition: all 0.3s ease; }",
            "utility_classes": ".text-center { text-align: center; }",
            "dark_mode_styles": "@media (prefers-color-scheme: dark) { :root { --bg-color: #1f2937; } }",
            "performance_optimizations": "/* Critical CSS optimizations */",
            "design_tokens": {
                "colors": {
                    "primary": "#2563eb",
                    "secondary": "#1e40af", 
                    "accent": "#3b82f6",
                    "neutral": ["#f8fafc", "#e2e8f0", "#64748b"]
                },
                "typography": {
                    "heading_font": "Inter, sans-serif",
                    "body_font": "Inter, sans-serif",
                    "sizes": {"base": "16px", "large": "24px"}
                },
                "spacing": {
                    "scale": ["0.5rem", "1rem", "1.5rem", "2rem"],
                    "containers": {"sm": "640px", "lg": "1024px"}
                },
                "breakpoints": {
                    "mobile": "640px",
                    "tablet": "768px", 
                    "desktop": "1024px"
                }
            },
            "color_scheme": {
                "primary": "#2563eb",
                "secondary": "#1e40af",
                "accent": "#3b82f6"
            }
        }
        
        try:
            # Try to extract JSON structure first
            json_blocks = re.findall(r'```json\s*([\s\S]*?)\s*```|({[\s\S]*})', response, re.IGNORECASE)
            
            for json_block in json_blocks:
                json_str = json_block[0] if json_block[0] else json_block[1]
                if not json_str:
                    continue
                    
                try:
                    parsed_json = json.loads(json_str)
                    if isinstance(parsed_json, dict) and "component_styles" in parsed_json:
                        # Fill in missing fields with defaults
                        for key, default_value in default_design.items():
                            if key not in parsed_json:
                                parsed_json[key] = default_value
                        logger.info("Successfully parsed enhanced JSON design from response")
                        return parsed_json
                except json.JSONDecodeError:
                    continue
            
            # Fallback to CSS extraction
            logger.info("No valid JSON found, attempting CSS extraction")
            extracted_css = EnhancedResponseParser._extract_css_sections(response)
            
            # Merge with defaults
            final_design = default_design.copy()
            final_design.update(extracted_css)
            
            return final_design
            
        except Exception as e:
            logger.error(f"Failed to parse enhanced design response: {e}")
            return default_design

    @staticmethod
    def _extract_css_sections(response: str) -> dict:
        """Extract CSS sections from response text"""
        sections = {}
        
        # Define section patterns
        section_patterns = {
            "css_variables": [r':root\s*\{[^}]+\}', r'CSS\s*Variables[:\s]*([\s\S]*?)(?=\n\n|\Z)'],
            "base_styles": [r'\/\*\s*Base\s*Styles\s*\*\/([\s\S]*?)(?=\/\*|\Z)', r'Base\s*Styles[:\s]*([\s\S]*?)(?=\n\n|\Z)'],
            "header": [r'\/\*\s*Header[\s\S]*?\*\/([\s\S]*?)(?=\/\*|\Z)', r'header\s*\{[^}]+\}'],
            "hero": [r'\/\*\s*Hero[\s\S]*?\*\/([\s\S]*?)(?=\/\*|\Z)', r'\.hero\s*\{[^}]+\}'],
            "responsive_styles": [r'@media[^{]+\{[\s\S]*?\}[\s\S]*?\}', r'Responsive[:\s]*([\s\S]*?)(?=\n\n|\Z)']
        }
        
        for section, patterns in section_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, response, re.IGNORECASE)
                if match:
                    sections[section] = match.group(0) if len(match.groups()) == 0 else match.group(1)
                    break
        
        return sections

    @staticmethod
    def parse_enhanced_structure_response(response: str) -> dict:
        """Parse enhanced structure response with comprehensive HTML extraction"""
        
        default_structure = {
            "document_structure": "<!DOCTYPE html><html><head><title>Business Website</title></head><body></body></html>",
            "head_section": {
                "meta_tags": '<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">',
                "structured_data": '{"@context": "https://schema.org", "@type": "Organization"}',
                "preload_directives": '<link rel="preload" href="/css/styles.css" as="style">',
                "social_meta": '<meta property="og:title" content="Business Website">'
            },
            "body_components": {
                "header": "<header><nav></nav></header>",
                "main_content": "<main></main>",
                "footer": "<footer></footer>"
            },
            "navigation": {
                "primary_nav": '<nav><ul><li><a href="#home">Home</a></li></ul></nav>',
                "breadcrumbs": '<nav aria-label="breadcrumb"></nav>',
                "skip_links": '<a href="#main-content" class="skip-link">Skip to main content</a>'
            },
            "content_sections": {
                "hero": '<section class="hero"><h1>Welcome</h1></section>',
                "about": '<section class="about"><h2>About Us</h2></section>',
                "services": '<section class="services"><h2>Our Services</h2></section>',
                "testimonials": '<section class="testimonials"><h2>Testimonials</h2></section>',
                "contact": '<section class="contact"><h2>Contact Us</h2></section>'
            },
            "forms": {
                "contact_form": '<form><label for="name">Name</label><input type="text" id="name" required></form>',
                "newsletter": '<form><label for="email">Email</label><input type="email" id="email" required></form>'
            },
            "accessibility_features": {
                "aria_landmarks": 'role="main", role="navigation", role="banner"',
                "focus_management": 'tabindex management and focus indicators',
                "screen_reader_content": '<span class="sr-only">Screen reader content</span>'
            },
            "performance_optimization": {
                "lazy_loading": 'loading="lazy" attributes on images',
                "resource_hints": '<link rel="dns-prefetch" href="//example.com">',
                "critical_path": 'Critical CSS and above-fold optimization'
            },
            "html_structure": "<!DOCTYPE html><html><head></head><body><header></header><main></main><footer></footer></body></html>",
            "meta_tags": '<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">'
        }
        
        try:
            # Try to extract JSON structure first
            json_blocks = re.findall(r'```json\s*([\s\S]*?)\s*```|({[\s\S]*})', response, re.IGNORECASE)
            
            for json_block in json_blocks:
                json_str = json_block[0] if json_block[0] else json_block[1]
                if not json_str:
                    continue
                    
                try:
                    parsed_json = json.loads(json_str)
                    if isinstance(parsed_json, dict) and ("document_structure" in parsed_json or "body_components" in parsed_json):
                        # Fill in missing fields with defaults
                        for key, default_value in default_structure.items():
                            if key not in parsed_json:
                                parsed_json[key] = default_value
                        logger.info("Successfully parsed enhanced JSON structure from response")
                        return parsed_json
                except json.JSONDecodeError:
                    continue
            
            # Fallback to HTML extraction
            logger.info("No valid JSON found, attempting HTML extraction")
            extracted_html = EnhancedResponseParser._extract_html_sections(response)
            
            # Merge with defaults
            final_structure = default_structure.copy()
            final_structure.update(extracted_html)
            
            return final_structure
            
        except Exception as e:
            logger.error(f"Failed to parse enhanced structure response: {e}")
            return default_structure

    @staticmethod
    def _extract_html_sections(response: str) -> dict:
        """Extract HTML sections from response text"""
        sections = {}
        
        # Extract complete HTML document
        html_match = re.search(r'<!DOCTYPE html>[\s\S]*?</html>', response, re.IGNORECASE)
        if html_match:
            sections["html_structure"] = html_match.group(0)
            sections["document_structure"] = html_match.group(0)
        
        # Extract specific components
        component_patterns = {
            "header": r'<header[\s\S]*?</header>',
            "nav": r'<nav[\s\S]*?</nav>',
            "main": r'<main[\s\S]*?</main>',
            "footer": r'<footer[\s\S]*?</footer>'
        }
        
        for component, pattern in component_patterns.items():
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                sections[component] = match.group(0)
        
        return sections
