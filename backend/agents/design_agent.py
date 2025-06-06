"""
Design Agent - Uses CodeLlama 34B for CSS and design generation
"""

import httpx
from core.config import settings
import logging

logger = logging.getLogger(__name__)


class DesignAgent:
    """Agent responsible for generating CSS styles and design layouts"""
    
    def __init__(self):
        self.model = settings.DESIGN_MODEL
        self.ollama_url = settings.OLLAMA_BASE_URL
    
    async def generate_design(self, business_info: dict, content_data: dict) -> dict:
        """
        Generate CSS styles and design components
        
        Args:
            business_info: Business information
            content_data: Generated content from content agent
            
        Returns:
            Dictionary containing CSS styles and design specifications
        """        
        try:
            prompt = self._build_design_prompt(business_info, content_data)
            
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
                    return self._parse_design_response(result["response"])
                else:
                    raise Exception(f"Ollama API error: {response.status_code}")
                    
        except Exception as e:
            logger.error(f"Design generation failed: {e}")
            raise
    
    def _build_design_prompt(self, business_info: dict, content_data: dict) -> str:
        """Build prompt for design generation"""
        colors = business_info.get('preferred_colors', ['#2563eb', '#1e40af'])
        
        return f"""
        Generate modern, responsive CSS styles for a {business_info['business_category']} website.
        
        Requirements:
        - Modern, clean design
        - Responsive layout (mobile-first)
        - Professional color scheme using: {colors}
        - Consistent typography
        - Smooth animations and transitions
        - Accessible design (WCAG compliant)
        
        Generate CSS for:
        1. Global styles and CSS variables
        2. Header and navigation
        3. Hero section
        4. About section
        5. Services/Products section
        6. Contact section
        7. Footer
        8. Responsive breakpoints
        
        Return complete CSS code that's production-ready.
        """
    
    def _parse_design_response(self, response: str) -> dict:
        """Parse and structure the design response"""
        # TODO: Implement proper CSS parsing and validation
        # For now, return a structured placeholder
        return {
            "global_css": "/* Global styles placeholder */",
            "header_css": "/* Header styles placeholder */",
            "hero_css": "/* Hero styles placeholder */",
            "about_css": "/* About styles placeholder */",
            "services_css": "/* Services styles placeholder */",
            "contact_css": "/* Contact styles placeholder */",
            "footer_css": "/* Footer styles placeholder */",
            "responsive_css": "/* Responsive styles placeholder */",
            "color_scheme": {
                "primary": "#2563eb",
                "secondary": "#1e40af",
                "accent": "#3b82f6"
            }
        }
