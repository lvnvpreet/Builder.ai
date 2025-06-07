"""
Content Agent - Uses Llama 3.1 70B for content generation
"""

import httpx
from core.config import settings
import logging
from core.logging import get_agent_logger
from .enhanced_prompts import DynamicPromptManager
from .enhanced_parsers import EnhancedResponseParser

logger = logging.getLogger(__name__)
agent_logger = get_agent_logger('content')


class ContentAgent:
    """Agent responsible for generating business content and copy"""
    
    def __init__(self):
        self.model = settings.CONTENT_MODEL
        self.ollama_url = settings.CONTENT_MODEL_OLLAMA_BASE_URL # Use the specific URL for content model
        self.prompt_manager = DynamicPromptManager()
    
    async def generate_content(self, business_info: dict) -> dict:
        """
        Generate website content based on business information
        
        Args:
            business_info: Dictionary containing business details
            
        Returns:
            Dictionary containing generated content
        """          
        try:
            agent_logger.info(f"Starting content generation for {business_info['business_name']}")
            prompt = self.prompt_manager.get_enhanced_content_prompt(business_info)
            agent_logger.debug(f"Enhanced content prompt: {prompt[:500]}...")  # Log first 500 chars
            
            # Set a reasonable timeout for AI model calls
            timeout = httpx.Timeout(300.0, connect=30.0)  # 5 minutes total, 30 seconds connect
            
            async with httpx.AsyncClient(timeout=timeout) as client:
                agent_logger.info(f"Sending request to Ollama model: {self.model}")
                response = await client.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False
                    }
                )                  
                if response.status_code == 200:
                    result = response.json()
                    agent_logger.info(f"Successfully received raw content from model for {business_info['business_name']}")
                    raw_response = result["response"]
                    # Log a small snippet of the raw response for debugging
                    agent_logger.debug(f"Raw model response snippet: {raw_response[:200]}...")
                    
                    parsed_response = EnhancedResponseParser.parse_enhanced_content_response(raw_response)
                    # Log the actual structured output (truncated for log readability)
                    agent_logger.info(f"Successfully parsed enhanced content with fields: {', '.join(parsed_response.keys())}")
                    agent_logger.info(f"Enhanced content output sample: {str(parsed_response)[:500]}...")
                    return parsed_response
                else:
                    agent_logger.error(f"Ollama API error: {response.status_code}")                    
                    raise Exception(f"Ollama API error: {response.status_code}")
                    
        except httpx.ConnectError as e:
            agent_logger.error(f"Content generation failed - Connection error: {e} - Server: {self.ollama_url}")
            agent_logger.debug(f"Connection details: Model={self.model}, URL={self.ollama_url}")
            raise
        except httpx.ReadTimeout as e:
            agent_logger.error(f"Content generation failed - Timeout error: {e} - Model response took too long")
            raise
        except Exception as e:
            agent_logger.error(f"Content generation failed: {type(e).__name__} - {e}")
            raise

    def _build_content_prompt(self, business_info: dict) -> str:
        """Build prompt for content generation"""
        # Define the JSON template separately to avoid f-string formatting issues
        json_template = '''{
          "hero_headline": "Your compelling headline here",
          "hero_subtitle": "Brief description of the business",
          "about_content": "Information about the business...",
          "services": ["Service 1", "Service 2", "Service 3"],
          "contact_content": "Contact information and call to action",
          "meta_title": "SEO Title for the website",
          "meta_description": "SEO description for search engines"
        }'''
        
        return f"""
        Generate professional website content for the following business:
        
        Business Name: {business_info['business_name']}
        Category: {business_info['business_category']}
        Description: {business_info['business_description']}
        Target Audience: {business_info.get('target_audience', 'General audience')}
        
        Generate the following content sections:
        1. Hero headline (compelling and attention-grabbing)
        2. Hero subtitle (brief description)
        3. About section (2-3 paragraphs)
        4. Services/Products section (3-4 key offerings)
        5. Contact section content
        6. SEO meta title and description
        
        Make the content professional, engaging, and SEO-optimized.
        
        IMPORTANT: Return the content in proper JSON format with the following structure:
        ```json
        {json_template}
        ```
        
        Follow this format exactly and ensure all fields are included in your response.
        """
    def _parse_content_response(self, response: str) -> dict:
        """Parse and structure the content response"""
        import json
        import re
        
        # Log the raw response for debugging (truncated for log readability)
        agent_logger.debug(f"Raw content response (first 500 chars): {response[:500]}...")
        
        # Default content that will be used if parsing fails or fields are missing
        default_content = {
            "hero_headline": "Professional Business Solutions",
            "hero_subtitle": "Quality service you can trust",
            "about_content": "We are a professional business dedicated to providing excellent services to our clients. With years of experience in the industry, our team is committed to delivering high-quality results that exceed expectations.",
            "services": ["Professional Service 1", "Quality Service 2", "Expert Service 3"],
            "contact_content": "Get in touch with us today to learn more about our services and how we can help you.",
            "meta_title": "Professional Business Services",
            "meta_description": "We provide high-quality professional services tailored to your business needs."
        }
        
        # List of field names to look for, with alternatives
        field_mapping = {
            "hero_headline": ["hero_headline", "headline", "title", "heroHeadline", "hero-headline"],
            "hero_subtitle": ["hero_subtitle", "subtitle", "tagline", "heroSubtitle", "hero-subtitle"],
            "about_content": ["about_content", "about", "aboutContent", "about-content", "about_section", "aboutSection"],
            "services": ["services", "service", "offerings", "products", "servicesList", "services_list"],
            "contact_content": ["contact_content", "contact", "contactContent", "contact-content", "contactInfo"],
            "meta_title": ["meta_title", "metaTitle", "seo_title", "seoTitle", "title"],
            "meta_description": ["meta_description", "metaDescription", "seo_description", "seoDescription", "description"]
        }
        
        try:
            # Method 1: Try to extract and parse JSON from the response
            content_data = {}
            json_blocks = re.findall(r'```json\s*([\s\S]*?)\s*```|({[\s\S]*})', response)
            
            # Process all potential JSON blocks found
            for json_block in json_blocks:
                # Handle both regex capture groups
                json_str = json_block[0] if json_block[0] else json_block[1]
                if not json_str:
                    continue
                    
                try:
                    parsed_json = json.loads(json_str)
                    if isinstance(parsed_json, dict) and len(parsed_json) > 1:
                        # We found what looks like valid content JSON
                        content_data = parsed_json
                        agent_logger.info("Successfully parsed JSON content from response")
                        break
                except json.JSONDecodeError:
                    # This block wasn't valid JSON, continue to the next one
                    continue
            
            # Method 2: If no JSON found or parsing failed, try regex extraction
            if not content_data:
                agent_logger.info("No valid JSON found in response, trying regex extraction")
                content_data = {}
                
                # Try to extract sections using various regex patterns
                # Process each field using its possible names
                for field, alternatives in field_mapping.items():
                    # Skip services as they need special handling
                    if field == "services":
                        continue
                        
                    # Create pattern to match any of the alternative field names
                    pattern = '|'.join(alternatives)
                    regex = fr'(?:{pattern})[:\s]+"?([^"]+?)"?(?:\n|\r|,|$)'
                    
                    # Try to find the field
                    match = re.search(regex, response, re.IGNORECASE)
                    if match:
                        content_data[field] = match.group(1).strip()
                
                # Handle services/offerings specially as they can be multiple items
                services = []
                service_pattern = r'(?:service|offering|product)\s*\d*[:\s]+"?([^"]+?)"?(?:\n|\r|,|$)'
                service_matches = re.findall(service_pattern, response, re.IGNORECASE)
                if service_matches:
                    services = [s.strip() for s in service_matches]
                    content_data["services"] = services
            
            # Final assembly: Use extracted content and fill in missing fields with defaults
            final_content = {}
            
            # Map fields from the extracted content to our standard field names
            for target_field, source_fields in field_mapping.items():
                # First check if our standard field name exists in the extracted content
                if target_field in content_data:
                    final_content[target_field] = content_data[target_field]
                    continue
                    
                # If not, check all alternative field names
                found = False
                for alt_field in source_fields:
                    if alt_field in content_data:
                        final_content[target_field] = content_data[alt_field]
                        found = True
                        break
                        
                # If field not found under any name, use default
                if not found:
                    agent_logger.warning(f"Field '{target_field}' not found in model response, using default")
                    final_content[target_field] = default_content[target_field]
            
            # Log the final content structure
            agent_logger.info(f"Successfully parsed content with {len(final_content)} fields")
            return final_content
                
        except Exception as e:
            agent_logger.error(f"Failed to parse content response: {e}")
            agent_logger.debug(f"Using default content due to parsing failure")
            # Instead of failing, return default content
            return default_content
