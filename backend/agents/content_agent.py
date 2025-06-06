"""
Content Agent - Uses Llama 3.1 70B for content generation
"""

import httpx
from core.config import settings
import logging

logger = logging.getLogger(__name__)


class ContentAgent:
    """Agent responsible for generating business content and copy"""
    
    def __init__(self):
        self.model = settings.CONTENT_MODEL
        self.ollama_url = settings.CONTENT_MODEL_OLLAMA_BASE_URL # Use the specific URL for content model
    
    async def generate_content(self, business_info: dict) -> dict:
        """
        Generate website content based on business information
        
        Args:
            business_info: Dictionary containing business details
            
        Returns:
            Dictionary containing generated content
        """        
        try:
            prompt = self._build_content_prompt(business_info)
            
            # Set a reasonable timeout for AI model calls
            timeout = httpx.Timeout(300.0, connect=30.0)  # 5 minutes total, 30 seconds connect
            
            async with httpx.AsyncClient(timeout=timeout) as client:
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
                    return self._parse_content_response(result["response"])
                else:
                    raise Exception(f"Ollama API error: {response.status_code}")
                    
        except Exception as e:
            logger.error(f"Content generation failed: {e}")
            raise
    
    def _build_content_prompt(self, business_info: dict) -> str:
        """Build prompt for content generation"""
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
        Return the content in JSON format with clear section labels.
        """
    
    def _parse_content_response(self, response: str) -> dict:
        """Parse and structure the content response"""
        # TODO: Implement proper JSON parsing and validation
        # For now, return a structured placeholder
        return {
            "hero_headline": "Professional Business Solutions",
            "hero_subtitle": "Delivering excellence in every project",
            "about_content": "Generated about content...",
            "services": ["Service 1", "Service 2", "Service 3"],
            "contact_content": "Get in touch with us today",
            "meta_title": "Business Name - Professional Services",
            "meta_description": "Professional business services description"
        }
