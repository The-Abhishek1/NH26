from pydantic_settings import BaseSettings
from typing import Optional
from enum import Enum

class LLMProvider(str, Enum):
    OPENAI = "openai"
    GEMINI = "gemini"
    LOCAL = "local"

class Settings(BaseSettings):
    # LLM Configuration
    LLM_PROVIDER: LLMProvider = LLMProvider.OPENAI
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    LOCAL_LLM_URL: str = "http://localhost:11434"  # Ollama default
    
    # Model Names
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    GEMINI_MODEL: str = "gemini-1.5-pro"
    LOCAL_MODEL: str = "Qwen2.5:3B"
    
    # Agent Configuration
    AGENT_TEMPERATURE: float = 0.3
    MAX_RETRIES: int = 3
    
    # Security
    API_RATE_LIMIT: int = 100
    JWT_SECRET: str = "your-secret-key-change-in-production"
    
    class Config:
        env_file = ".env"

settings = Settings()