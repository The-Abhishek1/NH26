from .base import BaseAgent
from typing import Dict, Any
import json

class SummarizerAgent(BaseAgent):
    def __init__(self):
        super().__init__("SummarizerAgent")
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        email = input_data.get("email", {})
        
        prompt = f"""
        Summarize the following email into 3 key bullet points.
        
        Email:
        {email.get('body', '')}
        
        Return JSON format:
        {{
            "summary": [
                "Key point 1",
                "Key point 2",
                "Key point 3"
            ],
            "key_entities": ["person1", "projectX"],
            "tone": "professional/urgent/friendly"
        }}
        """
        
        response = await self.llm.generate_with_retry(prompt)
        
        try:
            result = json.loads(response)
        except:
            result = {
                "summary": ["Error generating summary"],
                "key_entities": [],
                "tone": "unknown"
            }
        
        return result