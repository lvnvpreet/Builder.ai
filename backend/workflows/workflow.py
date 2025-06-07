"""
LangGraph workflow for AI website generation
Multi-agent orchestration using LangGraph
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict, Any
import asyncio
import datetime
import logging
import random

from agents.content_agent import ContentAgent
from agents.design_agent import DesignAgent
from agents.structure_agent import StructureAgent
from agents.image_agent import ImageAgent
from agents.quality_agent import QualityAgent

logger = logging.getLogger(__name__)


class GenerationState(TypedDict):
    """State shared between agents in the workflow"""
    generation_id: str
    business_info: dict
    content_data: dict
    design_data: dict
    structure_data: dict
    images_data: dict
    quality_report: dict
    current_step: str
    progress: int
    errors: List[str]
    final_website: dict


class WebsiteGenerationWorkflow:
    """LangGraph workflow for orchestrating website generation"""
    def __init__(self):
        self.content_agent = ContentAgent()
        self.design_agent = DesignAgent()
        self.structure_agent = StructureAgent()
        self.image_agent = ImageAgent()
        self.quality_agent = QualityAgent()
        
        # Get agent logger for workflow
        from core.logging import get_agent_logger
        self.agent_logger = get_agent_logger('workflow')
        
        # Build the workflow graph
        self.workflow = self._build_workflow()
  # First generate_website method removed to avoid duplication
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        
        # Create workflow graph
        workflow = StateGraph(GenerationState)
        
        # Add nodes (agent functions)
        workflow.add_node("content_generation", self._content_generation_node)
        workflow.add_node("parallel_generation", self._parallel_generation_node)
        workflow.add_node("quality_validation", self._quality_validation_node)
        workflow.add_node("final_assembly", self._final_assembly_node)
        
        # Define the flow
        workflow.set_entry_point("content_generation")
        workflow.add_edge("content_generation", "parallel_generation")
        workflow.add_edge("parallel_generation", "quality_validation")
        workflow.add_edge("quality_validation", "final_assembly")
        workflow.add_edge("final_assembly", END)
        
        return workflow.compile()
    async def _content_generation_node(self, state: GenerationState) -> GenerationState:
        """Generate content using Content Agent"""
        from api.routes.websocket import manager
        import datetime
        
        try:
            logger.info(f"Starting content generation for {state['generation_id']}")
            state["current_step"] = "Content Generation"
            state["progress"] = 20
            
            # Send progress update via WebSocket
            await manager.send_generation_update(state["generation_id"], {
                "type": "progress_update",
                "progress": state["progress"],
                "step": state["current_step"],
                "timestamp": datetime.datetime.now().isoformat()
            })
            
            # Implement retry logic instead of falling back
            max_retries = 3
            retry_count = 0
            last_exception = None
            
            while retry_count < max_retries:
                try:
                    content_data = await self.content_agent.generate_content(state["business_info"])
                    state["content_data"] = content_data
                    logger.info(f"Content generation completed for {state['generation_id']} on attempt {retry_count + 1}")
                    return state
                except Exception as e:
                    retry_count += 1
                    last_exception = e
                    logger.warning(f"Content generation attempt {retry_count} failed: {e}. {'Retrying...' if retry_count < max_retries else 'Max retries reached.'}")
                    await asyncio.sleep(2)  # Wait before retry
            
            # If we get here, all retries failed
            logger.error(f"Content generation failed after {max_retries} attempts: {last_exception}")
            state["errors"].append(f"Content generation error after {max_retries} attempts: {str(last_exception)}")
            
            # Send error update via WebSocket
            await manager.send_generation_update(state["generation_id"], {
                "type": "error",
                "message": f"Content generation failed after {max_retries} attempts: {str(last_exception)}",
                "timestamp": datetime.datetime.now().isoformat()
            })
            
            # Raise the exception instead of returning state with error
            # This will cause the workflow to fail and prevent fallbacks
            raise Exception(f"Content generation failed after {max_retries} attempts: {last_exception}")
            
            # No longer returning state with errors - we want the generation to fail
            # return state
        except asyncio.CancelledError:
            logger.warning(f"Content generation cancelled for {state['generation_id']}")
            raise
        
    async def _parallel_generation_node(self, state: GenerationState) -> GenerationState:
        """Run design, structure, and image generation in parallel"""
        from api.routes.websocket import manager
        import datetime
        
        try:
            logger.info(f"Starting parallel generation for {state['generation_id']}")
            state["current_step"] = "Design & Structure Generation"
            state["progress"] = 60
            
            # Send progress update via WebSocket
            await manager.send_generation_update(state["generation_id"], {
                "type": "progress_update",
                "progress": state["progress"],
                "step": state["current_step"],
                "timestamp": datetime.datetime.now().isoformat()
            })
            
            # Define retry function for each agent
            async def retry_agent_with_backoff(agent_func, max_retries=3, base_timeout=300.0):
                retry_count = 0
                last_exception = None
                
                while retry_count < max_retries:
                    try:
                        result = await asyncio.wait_for(
                            agent_func(),
                            timeout=base_timeout
                        )
                        # If we reach here, the agent succeeded
                        return result
                    except Exception as e:
                        retry_count += 1
                        last_exception = e
                        logger.warning(f"Agent attempt {retry_count} failed: {e}")
                        if retry_count < max_retries:
                            # Exponential backoff with jitter
                            delay = (2 ** retry_count) + random.uniform(0, 1)
                            await asyncio.sleep(delay)  
                
                # If we reach here, all retries failed
                logger.error(f"Agent failed after {max_retries} attempts: {last_exception}")
                # Re-raise the exception instead of using fallbacks
                raise last_exception
            
            # Define agent functions
            async def design_task():
                return await self.design_agent.generate_design(state["business_info"], state["content_data"])
                
            async def structure_task():
                return await self.structure_agent.generate_structure(state["business_info"], state["content_data"])
                
            async def image_task():
                return await self.image_agent.generate_images(state["business_info"], state["content_data"])
            
            # Run agents in parallel with retry logic
            tasks = [
                retry_agent_with_backoff(design_task, max_retries=3, base_timeout=300.0),
                retry_agent_with_backoff(structure_task, max_retries=3, base_timeout=300.0),
                retry_agent_with_backoff(image_task, max_retries=3, base_timeout=60.0)
            ]
            
            try:
                # Wait for all tasks to complete or fail
                design_data, structure_data, images_data = await asyncio.gather(*tasks)
                
                # Store results in state
                state["design_data"] = design_data
                state["structure_data"] = structure_data
                state["images_data"] = images_data
                
            except asyncio.CancelledError:
                logger.warning(f"Parallel generation cancelled for {state['generation_id']}")
                raise
            except Exception as e:
                # If any agent fails after retries, the entire generation fails
                logger.error(f"Parallel generation component failed after retries: {e}")
                await manager.send_generation_update(state["generation_id"], {
                    "type": "error",
                    "message": f"Generation component failed: {str(e)}",
                    "timestamp": datetime.datetime.now().isoformat()
                })
                # Re-raise the exception to fail the workflow
                raise
            
            logger.info(f"Parallel generation completed successfully for {state['generation_id']}")
            return state
            
        except asyncio.CancelledError:
            logger.warning(f"Parallel generation cancelled for {state['generation_id']}")
            raise
        except Exception as e:
            logger.error(f"Parallel generation failed: {e}")
            # Re-raise the exception to fail the workflow instead of returning state with error
            raise
    async def _quality_validation_node(self, state: GenerationState) -> GenerationState:
        """Validate quality using Quality Agent"""
        from api.routes.websocket import manager
        import datetime
        
        try:
            logger.info(f"Starting quality validation for {state['generation_id']}")
            state["current_step"] = "Quality Validation"
            state["progress"] = 80
            
            # Send progress update via WebSocket
            await manager.send_generation_update(state["generation_id"], {
                "type": "progress_update",
                "progress": state["progress"],
                "step": state["current_step"],
                "timestamp": datetime.datetime.now().isoformat()
            })
            
            quality_report = await self.quality_agent.validate_generation(
                state["content_data"],
                state["design_data"],
                state["structure_data"],
                state["images_data"]
            )
            state["quality_report"] = quality_report
            
            logger.info(f"Quality validation completed for {state['generation_id']}")
            return state
            
        except Exception as e:
            logger.error(f"Quality validation failed: {e}")
            state["errors"].append(f"Quality validation error: {str(e)}")
            
            # Send error update via WebSocket
            await manager.send_generation_update(state["generation_id"], {
                "type": "error",
                "message": str(e),
                "timestamp": datetime.datetime.now().isoformat()
            })
            return state

    async def _final_assembly_node(self, state: GenerationState) -> GenerationState:
        """Assemble final website"""
        from api.routes.websocket import manager
        import datetime
        import os
        
        try:
            logger.info(f"Starting final assembly for {state['generation_id']}")
            state["current_step"] = "Final Assembly"
            state["progress"] = 95
            
            # Send progress update via WebSocket
            await manager.send_generation_update(state["generation_id"], {
                "type": "progress_update",
                "progress": state["progress"],
                "step": state["current_step"],
                "timestamp": datetime.datetime.now().isoformat()
            })
            
            # Combine all components into final website
            current_time = datetime.datetime.now().isoformat()
            
            # Save the generated website files to disk
            website_dir = os.path.join("uploads", "websites", state["generation_id"])
            os.makedirs(website_dir, exist_ok=True)
              # Generate HTML and CSS content
            html_content = self._generate_final_html(state)
            css_content = self._generate_final_css(state)
            
            # Log the final assembled website (partial content for readability)
            self.agent_logger.info(f"Final HTML (first 500 chars): {html_content[:500]}...")
            self.agent_logger.info(f"Final CSS (first 500 chars): {css_content[:500]}...")
            
            # Save HTML file
            with open(os.path.join(website_dir, "index.html"), "w", encoding="utf-8") as f:
                f.write(html_content)
            
            # Save CSS file
            with open(os.path.join(website_dir, "styles.css"), "w", encoding="utf-8") as f:
                f.write(css_content)
              # Create website URL - use full URL for previews
            relative_url = f"/uploads/websites/{state['generation_id']}/index.html"
            # This ensures the URL works both for API responses and for serving static files
            website_url = relative_url
            
            final_website = {
                "websiteUrl": website_url,
                "htmlContent": html_content,
                "cssContent": css_content,
                "pages": [
                    {
                        "id": "home",
                        "name": "Home",
                        "path": "/"
                    }
                ],
                "images": state.get("images_data", {}).get("images", []),
                "metadata": {
                    "generation_id": state["generation_id"],
                    "business_info": state["business_info"],
                    "quality_score": state["quality_report"].get("overall_score", 0),
                    "generated_at": current_time
                }
            }
            
            state["final_website"] = final_website
            state["progress"] = 100
            state["current_step"] = "Completed"
            
            # Send final progress update via WebSocket
            await manager.send_generation_update(state["generation_id"], {
                "type": "progress_update",
                "progress": 100,
                "step": "Completed",
                "timestamp": datetime.datetime.now().isoformat()
            })
            
            logger.info(f"Website generation completed for {state['generation_id']}")
            return state
            
        except Exception as e:
            logger.error(f"Final assembly failed: {e}")
            state["errors"].append(f"Final assembly error: {str(e)}")
            
            # Send error update via WebSocket
            await manager.send_generation_update(state["generation_id"], {
                "type": "error",
                "message": str(e),
                "timestamp": datetime.datetime.now().isoformat()
            })
            return state

    def _generate_footer_content(self, content_data: dict, business_info: dict) -> str:
        """Generate enhanced footer with comprehensive business information"""
        business_name = business_info.get('business_name', 'Your Business')
        business_category = business_info.get('business_category', 'Business')
        business_location = business_info.get('location', '')
        business_description = business_info.get('business_description', '')
        
        # Use content data if available, otherwise create basic info from business_info
        footer_info = content_data.get('footer_contact_info', {})
        footer_services = content_data.get('footer_services', [])
        footer_areas = content_data.get('footer_areas', [])
        footer_social = content_data.get('footer_social_links', {})
        footer_description = content_data.get('footer_company_description', business_description)
        
        # If no footer content was generated, create basic info from business_info
        if not footer_info:
            footer_info = {
                'address': business_location if business_location else f'{business_name} Location',
                'phone': '(555) 123-4567',  # Default phone
                'email': f'info@{business_name.lower().replace(" ", "").replace(",", "")}.com',
                'hours': 'Mon-Fri 9AM-6PM'
            }
        
        if not footer_services:
            # Create basic services based on business category
            footer_services = self._get_default_services_for_category(business_category)
        
        if not footer_areas and business_location:
            # Use the business location as a service area
            footer_areas = [business_location]
        
        # Company info section
        company_section = f"""
            <div class="footer-section">
                <h3>{business_name}</h3>
                <p>{footer_description}</p>
                {f'<p><strong>Location:</strong> {footer_info.get("address", "")}</p>' if footer_info.get("address") else ''}
            </div>
        """
        
        # Services section
        services_section = ""
        if footer_services:
            services_list = ''.join([f'<li><a href="#services">{service}</a></li>' for service in footer_services[:4]])
            services_section = f"""
            <div class="footer-section">
                <h3>Our Services</h3>
                <ul>
                    {services_list}
                </ul>
            </div>
            """
        
        # Service areas section
        areas_section = ""
        if footer_areas:
            areas_list = ''.join([f'<li>{area}</li>' for area in footer_areas[:4]])
            areas_section = f"""
            <div class="footer-section">
                <h3>Service Areas</h3>
                <ul>
                    {areas_list}
                </ul>
            </div>
            """
        
        # Contact section
        contact_section = f"""
            <div class="footer-section">
                <h3>Contact Info</h3>
                {f'<p><strong>Phone:</strong> <a href="tel:{footer_info.get("phone", "")}">{footer_info.get("phone", "")}</a></p>' if footer_info.get("phone") else ''}
                {f'<p><strong>Email:</strong> <a href="mailto:{footer_info.get("email", "")}">{footer_info.get("email", "")}</a></p>' if footer_info.get("email") else ''}
                {f'<p><strong>Hours:</strong> {footer_info.get("hours", "")}</p>' if footer_info.get("hours") else ''}
                
                <div class="social-links">
                    {f'<a href="{footer_social.get("facebook", "#")}" aria-label="Facebook"><span>📘</span></a>' if footer_social.get("facebook") else ''}
                    {f'<a href="{footer_social.get("twitter", "#")}" aria-label="Twitter"><span>🐦</span></a>' if footer_social.get("twitter") else ''}
                    {f'<a href="{footer_social.get("linkedin", "#")}" aria-label="LinkedIn"><span>💼</span></a>' if footer_social.get("linkedin") else ''}
                    {f'<a href="{footer_social.get("instagram", "#")}" aria-label="Instagram"><span>📷</span></a>' if footer_social.get("instagram") else ''}
                </div>
            </div>
        """
        
        return f"""
        <footer class="footer">
            <div class="container">
                <div class="footer-content">
                    {company_section}
                    {services_section}
                    {areas_section}
                    {contact_section}
                </div>
                <div class="footer-bottom">
                    <p>&copy; {datetime.datetime.now().year} {business_name}. All rights reserved.</p>
                </div>
            </div>
        </footer>
        """

    def _get_default_services_for_category(self, category: str) -> list:
        """Generate default services based on business category"""
        default_services = {
            'plumbing': ['Emergency Repair', 'Drain Cleaning', 'Water Heater Service', 'Bathroom Plumbing'],
            'restaurant': ['Dine In', 'Takeout', 'Catering', 'Private Events'],
            'healthcare': ['Consultations', 'Check-ups', 'Emergency Care', 'Specialized Treatment'],
            'legal': ['Consultation', 'Document Review', 'Court Representation', 'Legal Advice'],
            'fitness': ['Personal Training', 'Group Classes', 'Nutrition Coaching', 'Membership Plans'],
            'technology': ['Software Development', 'Consulting', 'Support', 'Custom Solutions'],
            'finance': ['Financial Planning', 'Investment Advice', 'Tax Services', 'Insurance'],
            'real estate': ['Buying', 'Selling', 'Rentals', 'Property Management'],
            'education': ['Courses', 'Tutoring', 'Online Learning', 'Certification'],
            'automotive': ['Repair', 'Maintenance', 'Inspection', 'Parts'],
            'construction': ['Residential', 'Commercial', 'Renovation', 'Maintenance'],
            'retail': ['Sales', 'Customer Service', 'Returns', 'Special Orders']
        }
        
        return default_services.get(category.lower(), ['Service 1', 'Service 2', 'Service 3', 'Service 4'])

    def _generate_final_html(self, state: GenerationState) -> str:
        """Generate the final HTML document"""
        business_name = state['business_info'].get('business_name', 'Professional Website')
        content_data = state.get('content_data', {})
        
        # Generate services HTML from the services array
        services_html = self._generate_services_html(content_data.get('services', []))
        
        # Get hero content with proper fallbacks
        hero_headline = content_data.get('hero_headline', 'Welcome to our website')
        hero_subtitle = content_data.get('hero_subtitle', 'Professional services for your needs')
        hero_cta = content_data.get('hero_cta', 'Get Started')
        
        # Get about content - could be multiple paragraphs
        about_content = self._generate_about_html(content_data)
        
        # Get contact content
        contact_headline = content_data.get('contact_headline', 'Contact Us')
        contact_content = content_data.get('contact_content', 'Get in touch with us today.')
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{content_data.get('meta_title', f'{business_name} - Professional Website')}</title>
    <meta name="description" content="{content_data.get('meta_description', 'Professional services for your business needs')}">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header class="header">
        <div class="container">
            <h1>{business_name}</h1>
            <nav>
                <ul>
                    <li><a href="#">Home</a></li>
                    <li><a href="#about">About</a></li>
                    <li><a href="#services">Services</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>
            </nav>
        </div>
    </header>
    
    <main>
        <section class="hero">
            <div class="container">
                <h2>{hero_headline}</h2>
                <p>{hero_subtitle}</p>
                <div class="hero-cta">
                    <a href="#contact" class="cta-button">{hero_cta}</a>
                </div>
            </div>
        </section>
        
        <section id="about" class="about">
            <div class="container">
                <h2>{content_data.get('about_headline', 'About Us')}</h2>
                {about_content}
            </div>
        </section>
        
        <section id="services" class="services">
            <div class="container">
                <h2>{content_data.get('services_headline', 'Our Services')}</h2>
                <div class="services-grid">
                    {services_html}
                </div>
            </div>
        </section>
        
        <section id="contact" class="contact">
            <div class="container">
                <h2>{contact_headline}</h2>
                <p>{contact_content}</p>
                <form>
                    <input type="text" placeholder="Your Name" required>
                    <input type="tel" placeholder="Phone Number">
                    <input type="email" placeholder="Your Email" required>
                    <textarea placeholder="Your Message" required></textarea>
                    <button type="submit">Send Message</button>
                </form>
            </div>        </section>
    </main>
    
    {self._generate_footer_content(content_data, state['business_info'])}
</body>
</html>"""
    def _generate_final_css(self, state: GenerationState) -> str:
        """Generate the final CSS stylesheet"""
        # Get design data if available
        design_data = state.get('design_data', {})
        
        # Use design data if available, otherwise use sensible defaults
        primary_color = design_data.get('colors', {}).get('primary', '#3f51b5')
        secondary_color = design_data.get('colors', {}).get('secondary', '#f50057')
        
        # Generate a complete CSS file with modern styling
        return f"""
/* Global Styles */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
}}

.container {{
    width: 90%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}}

h1, h2, h3 {{
    margin-bottom: 1rem;
    line-height: 1.3;
}}

a {{
    text-decoration: none;
    color: {primary_color};
}}

/* Header */
.header {{
    background-color: #fff;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    padding: 1rem 0;
    position: sticky;
    top: 0;
    z-index: 100;
}}

.header .container {{
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.header h1 {{
    font-size: 1.5rem;
    margin: 0;
    color: {primary_color};
}}

.header nav ul {{
    display: flex;
    list-style: none;
}}

.header nav ul li {{
    margin-left: 1.5rem;
}}

.header nav ul li a {{
    color: #333;
    transition: color 0.3s;
    font-weight: 500;
}}

.header nav ul li a:hover {{
    color: {primary_color};
}}

/* Hero Section */
.hero {{
    background: linear-gradient(135deg, {primary_color}, {secondary_color});
    color: #fff;
    padding: 5rem 0;
    text-align: center;
}}

.hero h2 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
    font-weight: bold;
}}

.hero p {{
    font-size: 1.2rem;
    max-width: 800px;
    margin: 0 auto 2rem;
}}

.hero-cta {{
    margin-top: 2rem;
}}

.cta-button {{
    background-color: rgba(255, 255, 255, 0.2);
    color: #fff;
    padding: 1rem 2rem;
    border-radius: 8px;
    font-weight: bold;
    border: 2px solid rgba(255, 255, 255, 0.3);
    transition: all 0.3s ease;
    display: inline-block;
}}

.cta-button:hover {{
    background-color: rgba(255, 255, 255, 0.3);
    border-color: rgba(255, 255, 255, 0.5);
    transform: translateY(-2px);
}}

/* About Section */
.about {{
    padding: 5rem 0;
    background-color: #f9f9f9;
}}

.about h2 {{
    color: {primary_color};
    font-size: 2rem;
    margin-bottom: 2rem;
}}

.about p {{
    font-size: 1.1rem;
    margin-bottom: 1.5rem;
    color: #555;
}}

/* Services Section */
.services {{
    padding: 5rem 0;
}}

.services h2 {{
    color: {primary_color};
    font-size: 2rem;
    margin-bottom: 3rem;
    text-align: center;
}}

.services-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}}

.service-card {{
    background: #fff;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 1px solid #eee;
}}

.service-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}}

.service-icon {{
    font-size: 3rem;
    margin-bottom: 1rem;
}}

.service-card h3 {{
    color: {primary_color};
    font-size: 1.3rem;
    margin-bottom: 1rem;
}}

.service-card p {{
    color: #666;
    line-height: 1.6;
}}

/* Contact Section */
.contact {{
    padding: 5rem 0;
    background-color: #f9f9f9;
}}

.contact h2 {{
    color: {primary_color};
    font-size: 2rem;
    margin-bottom: 2rem;
}}

.contact p {{
    font-size: 1.1rem;
    margin-bottom: 2rem;
    color: #555;
}}

.contact form {{
    margin-top: 2rem;
    max-width: 600px;
}}

.contact input,
.contact textarea {{
    width: 100%;
    padding: 1rem;
    margin-bottom: 1rem;
    border: 2px solid #ddd;
    border-radius: 8px;
    font-family: inherit;
    font-size: 1rem;
    transition: border-color 0.3s ease;
}}

.contact input:focus,
.contact textarea:focus {{
    outline: none;
    border-color: {primary_color};
}}

.contact textarea {{
    min-height: 150px;
    resize: vertical;
}}

.contact button {{
    background-color: {primary_color};
    color: #fff;
    border: none;
    padding: 1rem 2rem;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: bold;
    transition: background-color 0.3s ease, transform 0.2s ease;
}}

.contact button:hover {{
    background-color: {secondary_color};
    transform: translateY(-2px);
}}

/* Footer */
.footer {{
    background-color: #2c3e50;
    color: #ecf0f1;
    padding: 3rem 0 1rem;
}}

.footer-content {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}}

.footer-section h3 {{
    color: #fff;
    margin-bottom: 1rem;
    font-size: 1.2rem;
    font-weight: 600;
}}

.footer-section p {{
    margin-bottom: 0.5rem;
    line-height: 1.6;
}}

.footer-section ul {{
    list-style: none;
    padding: 0;
}}

.footer-section ul li {{
    margin-bottom: 0.5rem;
}}

.footer-section ul li a {{
    color: #bdc3c7;
    text-decoration: none;
    transition: color 0.3s ease;
}}

.footer-section ul li a:hover {{
    color: {primary_color};
}}

.footer-section a {{
    color: #3498db;
    text-decoration: none;
    transition: color 0.3s ease;
}}

.footer-section a:hover {{
    color: {primary_color};
}}

.social-links {{
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}}

.social-links a {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    background-color: #34495e;
    border-radius: 50%;
    color: #fff;
    text-decoration: none;
    transition: all 0.3s ease;
}}

.social-links a:hover {{
    background-color: {primary_color};
    transform: translateY(-2px);
}}

.footer-bottom {{
    border-top: 1px solid #34495e;
    padding-top: 2rem;
    text-align: center;
}}

.footer-bottom p {{
    margin: 0;
    color: #95a5a6;
}}

/* Responsive Styles */
@media (max-width: 768px) {{
    .header .container {{
        flex-direction: column;
        gap: 1rem;
    }}
    
    .header nav ul {{
        justify-content: center;
    }}
    
    .header nav ul li {{
        margin: 0 0.75rem;
    }}
    
    .hero {{
        padding: 3rem 0;
    }}
    
    .hero h2 {{
        font-size: 2rem;
    }}
    
    .services-grid {{
        grid-template-columns: 1fr;
        gap: 1.5rem;
    }}
}}

@media (max-width: 576px) {{
    .hero h2 {{
        font-size: 1.8rem;
    }}
    
    .about, .services, .contact {{
        padding: 3rem 0;
    }}
    
    .service-card {{
        padding: 1.5rem;
    }}

    color: #333;
    transition: color 0.3s;
}}

.header nav ul li a:hover {{
    color: {primary_color};
}}

/* Hero Section */
.hero {{
    background: linear-gradient(135deg, {primary_color}, {secondary_color});
    color: #fff;
    padding: 5rem 0;
    text-align: center;
}}

.hero h2 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
}}

.hero p {{
    font-size: 1.2rem;
    max-width: 800px;
    margin: 0 auto;
}}

/* About Section */
.about {{
    padding: 5rem 0;
    background-color: #f9f9f9;
}}

/* Services Section */
.services {{
    padding: 5rem 0;
}}

.services-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}}

/* Contact Section */
.contact {{
    padding: 5rem 0;
    background-color: #f9f9f9;
}}

.contact form {{
    margin-top: 2rem;
    max-width: 600px;
}}

.contact input,
.contact textarea {{
    width: 100%;
    padding: 0.8rem;
    margin-bottom: 1rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-family: inherit;
}}

.contact textarea {{
    min-height: 150px;
}}

.contact button {{
    background-color: {primary_color};
    color: #fff;
    border: none;
    padding: 0.8rem 1.5rem;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;
}}

.contact button:hover {{
    background-color: {secondary_color};
}}

/* Footer */
.footer {{
    background-color: #2c3e50;
    color: #ecf0f1;
    padding: 3rem 0 1rem;
}}

.footer-content {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}}

.footer-section h3 {{
    color: #fff;
    margin-bottom: 1rem;
    font-size: 1.2rem;
    font-weight: 600;
}}

.footer-section p {{
    margin-bottom: 0.5rem;
    line-height: 1.6;
}}

.footer-section ul {{
    list-style: none;
    padding: 0;
}}

.footer-section ul li {{
    margin-bottom: 0.5rem;
}}

.footer-section ul li a {{
    color: #bdc3c7;
    text-decoration: none;
    transition: color 0.3s ease;
}}

.footer-section ul li a:hover {{
    color: {primary_color};
}}

.footer-section a {{
    color: #3498db;
    text-decoration: none;
    transition: color 0.3s ease;
}}

.footer-section a:hover {{
    color: {primary_color};
}}

.social-links {{
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}}

.social-links a {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    background-color: #34495e;
    border-radius: 50%;
    color: #fff;
    text-decoration: none;
    transition: all 0.3s ease;
}}

.social-links a:hover {{
    background-color: {primary_color};
    transform: translateY(-2px);
}}

.footer-bottom {{
    border-top: 1px solid #34495e;
    padding-top: 2rem;
    text-align: center;
}}

.footer-bottom p {{
    margin: 0;
    color: #95a5a6;
}}

/* Responsive Styles */
@media (max-width: 768px) {{
    .header .container {{
        flex-direction: column;
    }}
    
    .header nav {{
        margin-top: 1rem;
    }}
    
    .header nav ul {{
        justify-content: center;
    }}
    
    .header nav ul li {{
        margin: 0 0.75rem;
    }}
    
    .hero h2 {{
        font-size: 2rem;
    }}
}}

@media (max-width: 576px) {{
    .hero {{
        padding: 3rem 0;
    }}
    
    .hero h2 {{
        font-size: 1.8rem;
    }}
    
    .about, .services, .contact {{
        padding: 3rem 0;
    }}
}}
"""

    def _generate_services_html(self, services_data) -> str:

        """Generate HTML for services section from services array"""
        if not services_data:
            return '<p>Our services information will be available soon.</p>'
        
        # If services_data is a list of service objects
        if isinstance(services_data, list):
            services_html = ""
            for service in services_data:
                if isinstance(service, dict):
                    name = service.get('name', 'Service')
                    description = service.get('description', 'Service description')
                    icon = service.get('icon_suggestion', 'service')
                    
                    # Generate icon based on suggestion
                    icon_html = self._get_service_icon(icon)
                    
                    services_html += f"""
                    <div class="service-card">
                        <div class="service-icon">{icon_html}</div>
                        <h3>{name}</h3>
                        <p>{description}</p>
                    </div>
                    """
                else:
                    # If it's just a string
                    services_html += f"""
                    <div class="service-card">
                        <h3>{service}</h3>
                    </div>
                    """
            return services_html
        
        # If services_data is a string, just return it wrapped
        return f'<div class="service-content">{services_data}</div>'
    
    def _generate_about_html(self, content_data) -> str:
        """Generate HTML for about section from content data"""
        about_parts = []
        
        # Check for multiple about content fields
        if content_data.get('about_content'):
            about_parts.append(f"<p>{content_data['about_content']}</p>")
        
        if content_data.get('about_content_second'):
            about_parts.append(f"<p>{content_data['about_content_second']}</p>")
        
        if content_data.get('about_content_third'):
            about_parts.append(f"<p>{content_data['about_content_third']}</p>")
        
        # If no specific about content, use a default
        if not about_parts:
            about_parts.append("<p>We are a professional business dedicated to providing excellent services to our clients.</p>")
        
        return "\n                ".join(about_parts)
    
    def _get_service_icon(self, icon_suggestion) -> str:
        """Generate appropriate icon based on suggestion"""
        icon_map = {
            'clock': '🕐',
            'emergency': '🚨', 
            'repair': '🔧',
            'wrench': '🔧',
            'drain': '🚿',
            'water': '💧',
            'plumbing': '🔧',
            'home': '🏠',
            'service': '⚙️',
            'tool': '🛠️',
            'phone': '📞',
            'help': '❓',
            'check': '✅',
            'star': '⭐'
        }
        
        # Return matching icon or default
        return icon_map.get(icon_suggestion.lower(), '⚙️')

    async def generate_website(self, generation_id: str, business_info: dict) -> dict:
        """
        Execute the complete website generation workflow

        Args:
            generation_id: Unique identifier for this generation
            business_info: Business information from the request
            
        Returns:
            Final generation state with website data
        """
        from api.routes.websocket import manager
        import datetime
        
        try:
            # Initialize state
            initial_state = GenerationState(
                generation_id=generation_id,
                business_info=business_info,
                content_data={},
                design_data={},
                structure_data={},
                images_data={},
                quality_report={},
                current_step="Initializing",
                progress=0,
                errors=[],
                final_website={}
            )
            
            # Send initial progress update
            await manager.send_generation_update(generation_id, {
                "type": "progress_update",
                "progress": 0,
                "step": "Initializing",
                "timestamp": datetime.datetime.now().isoformat()
            })
            
            # Execute workflow
            final_state = await self.workflow.ainvoke(initial_state)
            
            # Send final progress update
            await manager.send_generation_update(generation_id, {
                "type": "progress_update",
                "progress": final_state["progress"],
                "step": final_state["current_step"],
                "timestamp": datetime.datetime.now().isoformat()
            })
            
            return final_state
            
        except Exception as e:
            logger.error(f"Workflow execution failed for {generation_id}: {e}")
            # Send error update via WebSocket
            await manager.send_generation_update(generation_id, {
                "type": "error",
                "message": str(e),
                "timestamp": datetime.datetime.now().isoformat()
            })
            raise
