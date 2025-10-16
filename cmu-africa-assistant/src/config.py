
"""
Configuration management for CMU-Africa Information Assistant
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = "gpt-4o-mini"
    
    # Pinecone Configuration
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "cmu-africa-assistant")
    PINECONE_DIMENSION = 1536  # OpenAI embedding dimension
    
    # Application Configuration
    APP_TITLE = os.getenv("APP_TITLE", "CMU-Africa Information Assistant")
    APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", "Ask me anything about CMU-Africa")
    DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")
    
    # RAG Configuration
    TOP_K_RESULTS = 5  # Number of relevant documents to retrieve
    SIMILARITY_THRESHOLD = 0.7  # Minimum similarity score for relevance
    MAX_TOKENS = 1000  # Maximum tokens in response
    TEMPERATURE = 0.7  # Response creativity (0-1)
    
    # Data Storage
    CHAT_HISTORY_FILE = "data/chat_history.json"
    FEEDBACK_FILE = "data/feedback.json"
    
    # Supported Languages
    SUPPORTED_LANGUAGES = {
        "en": "English",
        "fr": "Français",
    }
    
    @staticmethod
    def validate():
        """Validate that required configuration is present"""
        missing = []
        
        if not Config.OPENAI_API_KEY:
            missing.append("OPENAI_API_KEY")
        if not Config.PINECONE_API_KEY:
            missing.append("PINECONE_API_KEY")
        if not Config.PINECONE_ENVIRONMENT:
            missing.append("PINECONE_ENVIRONMENT")
            
        return missing

config = Config()
