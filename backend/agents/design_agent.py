"""
Design Agent - Uses CodeLlama 34B for CSS and design generation
"""

import httpx
from core.config import settings
import logging
from core.logging import get_agent_logger

logger = logging.getLogger(__name__)
agent_logger = get_agent_logger('design')


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
            agent_logger.info(f"Starting design generation for {business_info['business_name']}")
            prompt = self._build_design_prompt(business_info, content_data)
            agent_logger.debug(f"Design prompt: {prompt}")
            
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
                    agent_logger.info(f"Successfully generated design for {business_info['business_name']}")
                    parsed_design = self._parse_design_response(result["response"])
                    # Log the actual output (truncated for log readability)
                    agent_logger.info(f"Design output: {str(parsed_design)[:500]}...")
                    return parsed_design
                else:
                    agent_logger.error(f"Ollama API error: {response.status_code}")
                    raise Exception(f"Ollama API error: {response.status_code}")
        except Exception as e:
            agent_logger.error(f"Design generation failed: {e}")
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
        try:
            import re
            
            # Extract CSS from response
            css_content = response
            
            # Extract different CSS sections
            sections = {
                "global_css": re.search(r'/\*\s*Global\s*Styles\s*\*/[\s\S]*?(?=/\*|$)', css_content, re.IGNORECASE),
                "header_css": re.search(r'/\*\s*Header[\s\S]*?\*/[\s\S]*?(?=/\*|$)', css_content, re.IGNORECASE),
                "hero_css": re.search(r'/\*\s*Hero[\s\S]*?\*/[\s\S]*?(?=/\*|$)', css_content, re.IGNORECASE),
                "about_css": re.search(r'/\*\s*About[\s\S]*?\*/[\s\S]*?(?=/\*|$)', css_content, re.IGNORECASE),
                "services_css": re.search(r'/\*\s*Services[\s\S]*?\*/[\s\S]*?(?=/\*|$)', css_content, re.IGNORECASE),
                "contact_css": re.search(r'/\*\s*Contact[\s\S]*?\*/[\s\S]*?(?=/\*|$)', css_content, re.IGNORECASE),
                "footer_css": re.search(r'/\*\s*Footer[\s\S]*?\*/[\s\S]*?(?=/\*|$)', css_content, re.IGNORECASE),
                "responsive_css": re.search(r'/\*\s*Responsive[\s\S]*?\*/[\s\S]*?(?=/\*|$)|@media[\s\S]*?}[\s\S]*?}', css_content, re.IGNORECASE)
            }
            
            # Extract colors from CSS
            color_scheme = {
                "primary": "#3f51b5",  # Default values
                "secondary": "#f50057",
                "accent": "#2196f3"
            }
            
            # Try to extract actual colors from the CSS
            color_vars = re.findall(r'--([a-zA-Z0-9_-]+):\s*(#[a-fA-F0-9]{3,6})', css_content)
            color_props = re.findall(r'(background|color):\s*(#[a-fA-F0-9]{3,6})', css_content)
            
            if color_vars:
                for var, color in color_vars:
                    if 'primary' in var.lower():
                        color_scheme["primary"] = color
                    elif 'secondary' in var.lower():
                        color_scheme["secondary"] = color
                    elif 'accent' in var.lower():
                        color_scheme["accent"] = color
            
            if color_props and 'primary' not in ' '.join([v[0] for v in color_vars]):
                # Use first few colors found if no explicit naming
                for i, (_, color) in enumerate(color_props[:3]):
                    if i == 0:
                        color_scheme["primary"] = color
                    elif i == 1:
                        color_scheme["secondary"] = color
                    elif i == 2:
                        color_scheme["accent"] = color
            
            # Compile the parsed CSS sections
            result = {
                "global_css": sections["global_css"].group(0) if sections["global_css"] else "",
                "header_css": sections["header_css"].group(0) if sections["header_css"] else "",
                "hero_css": sections["hero_css"].group(0) if sections["hero_css"] else "",
                "about_css": sections["about_css"].group(0) if sections["about_css"] else "",
                "services_css": sections["services_css"].group(0) if sections["services_css"] else "",
                "contact_css": sections["contact_css"].group(0) if sections["contact_css"] else "",
                "footer_css": sections["footer_css"].group(0) if sections["footer_css"] else "",
                "responsive_css": sections["responsive_css"].group(0) if sections["responsive_css"] else "",
                "color_scheme": color_scheme
            }
            
            # If we don't have enough CSS sections, or if they're all empty, fail
            non_empty_sections = [k for k, v in result.items() if k != "color_scheme" and v]
            if len(non_empty_sections) < 4:  # Need at least a few sections for a valid result
                raise ValueError("Not enough CSS sections could be extracted from response")
                
            return result
            
        except Exception as e:
            agent_logger.error(f"Failed to parse design response: {e}")
            agent_logger.debug(f"Design parsing error with raw response: {response[:500]}...")
            # Raise error instead of returning placeholder
            raise ValueError(f"Design parsing failed: {str(e)}")
            
        # No longer returning placeholders - if parsing fails, we raise an exception
