import aiohttp
from .base import BaseLLMProvider
from config import settings
import logging

logger = logging.getLogger(__name__)

class LocalLLMProvider(BaseLLMProvider):
    def __init__(self):
        self.url = settings.LOCAL_LLM_URL
        self.model = settings.LOCAL_MODEL
    
    async def generate(self, prompt: str, **kwargs) -> str:
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": kwargs.get("temperature", 0.3)
                }
            }
            async with session.post(f"{self.url}/api/generate", json=payload) as resp:
                result = await resp.json()
                return result.get("response", "")
    
    async def generate_with_retry(self, prompt: str, max_retries: int = 3) -> str:
        # Similar retry logic
        for attempt in range(max_retries):
            try:
                return await self.generate(prompt)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(1)
    
    async def batch_generate(self, prompts: List[str]) -> List[str]:
        tasks = [self.generate(prompt) for prompt in prompts]
        return await asyncio.gather(*tasks)