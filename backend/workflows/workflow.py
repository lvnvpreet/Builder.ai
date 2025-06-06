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

    def _generate_final_html(self, state: GenerationState) -> str:
        """Generate the final HTML document"""
        business_name = state['business_info'].get('business_name', 'Professional Website')
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{business_name} - {state['content_data'].get('meta_title', 'Professional Website')}</title>
    <meta name="description" content="{state['content_data'].get('meta_description', '')}">
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
                <h2>{state['content_data'].get('headline', 'Welcome to our website')}</h2>
                <p>{state['content_data'].get('tagline', 'Professional services for your needs')}</p>
            </div>
        </section>
        
        <section id="about" class="about">
            <div class="container">
                <h2>About Us</h2>
                <p>{state['content_data'].get('about_content', 'Information about our business')}</p>
            </div>
        </section>
        
        <section id="services" class="services">
            <div class="container">
                <h2>Our Services</h2>
                <div class="services-grid">
                    {state['content_data'].get('services_content', '<p>Our services information</p>')}
                </div>
            </div>
        </section>
        
        <section id="contact" class="contact">
            <div class="container">
                <h2>Contact Us</h2>
                <p>{state['content_data'].get('contact_content', 'Contact information')}</p>
                <form>
                    <input type="text" placeholder="Your Name">
                    <input type="email" placeholder="Your Email">
                    <textarea placeholder="Your Message"></textarea>
                    <button type="submit">Send Message</button>
                </form>
            </div>
        </section>
    </main>
    
    <footer class="footer">
        <div class="container">
            <p>&copy; {datetime.datetime.now().year} {business_name}. All rights reserved.</p>
        </div>
    </footer>
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
    background-color: #333;
    color: #fff;
    padding: 2rem 0;
    text-align: center;
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
    
    # Fallback methods have been removed as we now use retry logic instead

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
