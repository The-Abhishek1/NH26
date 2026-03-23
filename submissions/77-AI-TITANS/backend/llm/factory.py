from config import settings, LLMProvider
from .base import BaseLLMProvider
from .openai_provider import OpenAIProvider
from .gemini_provider import GeminiProvider
from .local_provider import LocalLLMProvider

_llm_instance = None

def get_llm_provider() -> BaseLLMProvider:
    """Factory method to get the appropriate LLM provider"""
    global _llm_instance
    
    if _llm_instance is None:
        if settings.LLM_PROVIDER == LLMProvider.OPENAI:
            _llm_instance = OpenAIProvider()
        elif settings.LLM_PROVIDER == LLMProvider.GEMINI:
            _llm_instance = GeminiProvider()
        elif settings.LLM_PROVIDER == LLMProvider.LOCAL:
            _llm_instance = LocalLLMProvider()
        else:
            raise ValueError(f"Unknown LLM provider: {settings.LLM_PROVIDER}")
    
    return _llm_instance