"""
Configuration settings for the application
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings"""
    
    # API Configuration
    APP_NAME: str = "Smart Video Learning Tool"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Process YouTube videos to generate summaries, key points, and quizzes using AI"
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # API Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY", "")
    
    # Groq Settings
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    GROQ_TEMPERATURE: float = float(os.getenv("GROQ_TEMPERATURE", "0.7"))
    GROQ_MAX_TOKENS: int = int(os.getenv("GROQ_MAX_TOKENS", "4000"))
    
    # Transcript Processing
    MAX_TRANSCRIPT_TOKENS: int = int(os.getenv("MAX_TRANSCRIPT_TOKENS", "12000"))
    
    # CORS - Allow React frontend
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000,*").split(",")
    
    # Validation
    REQUIRED_KEY_POINTS: int = 5
    REQUIRED_QUIZ_QUESTIONS: int = 10
    QUIZ_OPTIONS_COUNT: int = 4
    
    @classmethod
    def validate(cls):
        """Validate required settings"""
        if not cls.GROQ_API_KEY:
            print("WARNING: GROQ_API_KEY environment variable is not set")
        return True


# Create settings instance
settings = Settings()
