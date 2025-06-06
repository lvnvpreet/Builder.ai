"""
Logging configuration for the AI Website Builder
"""

import logging
import structlog
import sys
import datetime
from pathlib import Path
from core.config import settings


def setup_logging():
    """Setup structured logging configuration"""
    
    # Create logs directory if it doesn't exist
    log_dir = Path(settings.LOG_FILE).parent
    log_dir.mkdir(exist_ok=True)
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Setup standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL.upper())
    )
    
    # File handler
    file_handler = logging.FileHandler(settings.LOG_FILE)
    file_handler.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    
    # Add handler to root logger
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    
    # Setup agent logging
    setup_agent_logging()


def setup_agent_logging():
    """Setup agent-specific logging to a dedicated file"""
    # Create agent logger
    agent_logger = logging.getLogger('agents')
    agent_logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    agent_logger.propagate = False  # Don't propagate to root logger
    
    # Create formatter with more details
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(process)d] - %(message)s'
    )
    
    # Create file handler for agent output
    agent_handler = logging.FileHandler(settings.AGENT_LOG_FILE)
    agent_handler.setFormatter(formatter)
    agent_handler.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    
    # Add handler to agent logger
    agent_logger.addHandler(agent_handler)


def get_agent_logger(agent_name):
    """
    Get a logger specifically for agent output
    
    Args:
        agent_name: Name of the agent (e.g., 'structure', 'content')
        
    Returns:
        Logger instance for the specific agent
    """
    # Ensure we use consistent names by removing '_agent' suffix if present
    clean_name = agent_name.replace('_agent', '')
    return logging.getLogger(f'agents.{clean_name}')


def log_generation_separator(website_name=None, session_id=None):
    """
    Add a clear separator to the agent log file between website generations
    
    Args:
        website_name: Name of the website being generated
        session_id: Unique session ID for this generation
    """
    separator = f"\n{'=' * 80}\n"
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    website_info = f"Website: {website_name}" if website_name else ""
    session_info = f"Session ID: {session_id}" if session_id else ""
    
    message = f"{separator}NEW WEBSITE GENERATION - {timestamp}\n{website_info}\n{session_info}\n{separator}"
    
    logger = logging.getLogger('agents')
    logger.info(message)
