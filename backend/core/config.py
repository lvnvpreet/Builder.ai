"""
Core configuration settings for the AI Website Builder
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    MONGODB_URL: str = "mongodb://localhost:27017/ai_website_builder"
    MONGODB_DB_NAME: str = "ai_website_builder"
    
    # Ollama Configuration
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    CONTENT_MODEL_OLLAMA_BASE_URL: str = "http://175.111.130.242:11434"
    CONTENT_MODEL: str = "llama3.1:70b"
    DESIGN_MODEL: str = "codellama:34b"    
    STRUCTURE_MODEL: str = "mistral:7b-instruct"
    
    # External APIs
    UNSPLASH_ACCESS_KEY: str = ""
    UNSPLASH_SECRET_KEY: str = ""
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    JWT_SECRET: str = "dev-jwt-secret-change-in-production"

    # CORS
    CORS_ORIGINS: str = "http://localhost:3001,http://localhost:5173"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert CORS_ORIGINS string to list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    # WebSocket
    WEBSOCKET_PATH: str = "/ws"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    AGENT_LOG_FILE: str = "logs/agent_output.log"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # File Storage
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10485760  # 10MB
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
