"""
Structure Agent - Uses Mistral 7B for HTML structure generation
"""

import httpx
from core.config import settings
import logging
from core.logging import get_agent_logger

logger = logging.getLogger(__name__)
agent_logger = get_agent_logger('structure')


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
            agent_logger.info(f"Starting structure generation for {business_info['business_name']}")
            prompt = self._build_structure_prompt(business_info, content_data)
            agent_logger.debug(f"Structure prompt: {prompt}")
            
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
                    agent_logger.info("Structure generation successful")
                    agent_logger.info("Parsing structure response")
                    structured_result = self._parse_structure_response(result["response"])
                    # Log the actual output (truncated for log readability)
                    agent_logger.info(f"Structure output: {str(structured_result)[:500]}...")
                    return structured_result
                else:
                    error_msg = f"Ollama API error: {response.status_code}"
                    agent_logger.error(error_msg)
                    raise Exception(error_msg)
        except Exception as e:
            agent_logger.error(f"Structure generation failed: {e}")
            raise

    def _build_structure_prompt(self, business_info: dict, content_data: dict) -> str:
        """Build prompt for structure generation"""
        prompt = f"""
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
        agent_logger.debug(f"Built structure prompt for {business_info['business_name']}")
        return prompt

    def _parse_structure_response(self, response: str) -> dict:
        """Parse and structure the HTML response"""
        # Log the raw response from the model
        agent_logger.info("Parsing structure response")
        agent_logger.debug(f"Raw structure response: {response}")
        
        try:
            import re
            
            # Extract HTML from response
            html_match = re.search(r'<!DOCTYPE html>[\s\S]*<\/html>', response)
            if html_match:
                html = html_match.group(0)
                
                # Extract navigation
                nav_match = re.search(r'<nav[\s\S]*?<\/nav>', html)
                navigation = nav_match.group(0) if nav_match else None
                
                # Extract header
                header_match = re.search(r'<header[\s\S]*?<\/header>', html)
                header = header_match.group(0) if header_match else None
                
                # Extract main content
                main_match = re.search(r'<main[\s\S]*?<\/main>', html)
                main_content = main_match.group(0) if main_match else None
                
                # Extract footer
                footer_match = re.search(r'<footer[\s\S]*?<\/footer>', html)
                footer = footer_match.group(0) if footer_match else None
                
                # Extract meta tags
                meta_tags = ""
                meta_matches = re.finditer(r'<meta[^>]*>', html)
                for match in meta_matches:
                    meta_tags += match.group(0) + "\n"
                
                # Validate essential components
                if not navigation or not header or not main_content or not footer:
                    raise ValueError("Generated HTML is missing essential components")
                
                return {
                    "html_structure": html,
                    "navigation": navigation,
                    "header": header,
                    "main_content": main_content,
                    "footer": footer,
                    "meta_tags": meta_tags,
                    "sections": ["header", "hero", "about", "services", "contact", "footer"]
                }
            else:
                # If full HTML not found, look for HTML fragments
                sections = {
                    "header": re.search(r'<header[\s\S]*?<\/header>|<div[^>]*class="header"[\s\S]*?<\/div>', response),
                    "navigation": re.search(r'<nav[\s\S]*?<\/nav>', response),
                    "hero": re.search(r'<section[^>]*class="hero"[\s\S]*?<\/section>|<div[^>]*class="hero"[\s\S]*?<\/div>', response),
                    "about": re.search(r'<section[^>]*?id="about"[\s\S]*?<\/section>|<div[^>]*?id="about"[\s\S]*?<\/div>', response),
                    "services": re.search(r'<section[^>]*?id="services"[\s\S]*?<\/section>|<div[^>]*?id="services"[\s\S]*?<\/div>', response),
                    "contact": re.search(r'<section[^>]*?id="contact"[\s\S]*?<\/section>|<div[^>]*?id="contact"[\s\S]*?<\/div>', response),
                    "footer": re.search(r'<footer[\s\S]*?<\/footer>|<div[^>]*class="footer"[\s\S]*?<\/div>', response)
                }
                
                # Check if we have enough sections
                found_sections = [k for k, v in sections.items() if v is not None]
                if len(found_sections) >= 4:  # We have enough sections
                    result = {
                        "html_structure": "",  # Will build this from sections
                        "navigation": sections["navigation"].group(0) if sections["navigation"] else "<nav><ul><li><a href='#'>Home</a></li></ul></nav>",
                        "header": sections["header"].group(0) if sections["header"] else "<header><div>Header</div></header>",
                        "main_content": "",  # Will build this from sections
                        "footer": sections["footer"].group(0) if sections["footer"] else "<footer><div>Footer</div></footer>",
                        "meta_tags": "<meta name='viewport' content='width=device-width, initial-scale=1.0'>",
                        "sections": found_sections
                    }
                    
                    # Build main_content from sections
                    main_content = ""
                    for section in ["hero", "about", "services", "contact"]:
                        if sections[section]:
                            main_content += sections[section].group(0) + "\n"
                    
                    result["main_content"] = main_content if main_content else "<main><div>Main content</div></main>"
                    
                    # Build full HTML
                    result["html_structure"] = """
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        {meta_tags}
                        <title>Website</title>
                    </head>
                    <body>
                        {header}
                        <main>
                            {main_content}
                        </main>
                        {footer}
                    </body>
                    </html>
                    """.format(
                        meta_tags=result["meta_tags"],
                        header=result["header"],
                        main_content=result["main_content"],
                        footer=result["footer"]
                    )
                    
                    return result
                
                # If we couldn't extract enough components, raise an error
                raise ValueError("Failed to extract enough HTML components from response")
                
        except Exception as e:
            agent_logger.error(f"Failed to parse structure response: {e}")
            agent_logger.debug(f"Structure parsing error with raw response: {response[:500]}...")
            # Raise error instead of returning placeholder
            raise ValueError(f"Structure parsing failed: {str(e)}")
            
        # No longer returning placeholders - if parsing fails, we raise an exception
