from abc import ABC, abstractmethod
from typing import List, Dict, Any
import asyncio

class BaseLLMProvider(ABC):
    """Abstract base class for all LLM providers"""
    
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from prompt"""
        pass
    
    @abstractmethod
    async def generate_with_retry(self, prompt: str, max_retries: int = 3) -> str:
        """Generate with automatic retry logic"""
        pass
    
    @abstractmethod
    async def batch_generate(self, prompts: List[str]) -> List[str]:
        """Generate multiple prompts in parallel"""
        pass