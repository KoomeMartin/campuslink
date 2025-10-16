
"""
Configuration management for the CMU-Africa Information Assistant
"""
import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4-mini")
    
    # Pinecone Configuration
    PINECONE_API_KEY: Optional[str] = os.getenv("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT: Optional[str] = os.getenv("PINECONE_ENVIRONMENT")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "cmu-africa-knowledge-base")
    
    # Application Configuration
    APP_TITLE: str = os.getenv("APP_TITLE", "CMU-Africa Information Assistant")
    APP_LANGUAGE: str = os.getenv("APP_LANGUAGE", "en")
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "False").lower() == "true"
    
    # RAG Configuration
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    TOP_K_RESULTS: int = 5
    TEMPERATURE: float = 0.3
    MAX_TOKENS: int = 500
    
    @classmethod
    def validate(cls) -> tuple[bool, list[str]]:
        """Validate configuration"""
        errors = []
        
        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is not set")
        
        if not cls.PINECONE_API_KEY:
            errors.append("PINECONE_API_KEY is not set")
            
        if not cls.PINECONE_ENVIRONMENT:
            errors.append("PINECONE_ENVIRONMENT is not set")
        
        return len(errors) == 0, errors
    
    @classmethod
    def is_configured(cls) -> bool:
        """Check if basic configuration is present"""
        return bool(cls.OPENAI_API_KEY and cls.PINECONE_API_KEY)
