from abc import ABC, abstractmethod
from typing import Dict, Any
from llm.factory import get_llm_provider
import logging
import time

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Abstract base class for all agents"""
    
    def __init__(self, name: str):
        self.name = name
        self.llm = get_llm_provider()
        self.logs = []
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return result"""
        pass
    
    async def execute_with_logging(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent with logging and timing"""
        start_time = time.time()
        try:
            result = await self.process(input_data)
            execution_time = time.time() - start_time
            
            self.logs.append({
                "agent": self.name,
                "status": "success",
                "execution_time": execution_time,
                "timestamp": time.time()
            })
            
            return result
        except Exception as e:
            self.logs.append({
                "agent": self.name,
                "status": "failed",
                "error": str(e),
                "timestamp": time.time()
            })
            raise
    
    def get_logs(self):
        return self.logs