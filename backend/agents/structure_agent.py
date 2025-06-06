"""
Structure Agent - Uses Mistral 7B for HTML structure generation
"""

import httpx
from core.config import settings
import logging

logger = logging.getLogger(__name__)


class StructureAgent:
    """Agent responsible for generating HTML structure and layout"""
    
    def __init__(self):
        self.model = settings.STRUCTURE_MODEL
        self.ollama_url = settings.OLLAMA_BASE_URL
    
    async def generate_structure(self, business_info: dict, content_data: dict) -> dict:
        """
        Generate HTML structure and navigation
        
        Args:
            business_info: Business information
            content_data: Generated content from content agent
            
        Returns:
            Dictionary containing HTML structure components
        """
        try:
            prompt = self._build_structure_prompt(business_info, content_data)
            
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
                    return self._parse_structure_response(result["response"])
                else:
                    raise Exception(f"Ollama API error: {response.status_code}")
                    
        except Exception as e:
            logger.error(f"Structure generation failed: {e}")
            raise

    def _build_structure_prompt(self, business_info: dict, content_data: dict) -> str:
        """Build prompt for structure generation"""
        return f"""
        Generate semantic HTML structure for a {business_info['business_category']} website.
        
        Content sections to include:
        - Header with navigation
        - Hero section
        - About section
        - Services/Products section
        - Contact section
        - Footer
        
        Requirements:
        - Semantic HTML5 elements
        - Proper heading hierarchy (h1, h2, h3)
        - Accessible structure (ARIA labels, alt text)
        - SEO-friendly markup
        - Clean, well-organized code
        - Responsive-ready structure
        
        Business name: {business_info['business_name']}
        Generate complete HTML structure with proper semantic elements.
        """

    def _parse_structure_response(self, response: str) -> dict:
        """Parse and structure the HTML response"""
        # TODO: Implement proper HTML parsing and validation
        # For now, return a structured placeholder
        return {
            "html_structure": "<!-- HTML structure placeholder -->",
            "navigation": "<!-- Navigation placeholder -->",
            "header": "<!-- Header placeholder -->",
            "main_content": "<!-- Main content placeholder -->",
            "footer": "<!-- Footer placeholder -->",
            "meta_tags": "<!-- Meta tags placeholder -->"
        }
