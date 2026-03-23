from .base import BaseAgent
from typing import Dict, Any
import json

class ClassifierAgent(BaseAgent):
    def __init__(self):
        super().__init__("ClassifierAgent")
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        email = input_data.get("email", {})
        
        prompt = f"""
        Analyze the following email and classify its priority.
        
        Subject: {email.get('subject', '')}
        Sender: {email.get('sender', '')}
        Body: {email.get('body', '')}
        
        Classify as one of: "URGENT", "REQUIRES_ACTION", "FYI"
        
        Also provide a brief reasoning for your classification.
        
        Return JSON format:
        {{
            "priority": "URGENT",
            "reasoning": "Because...",
            "confidence": 0.95
        }}
        """
        
        response = await self.llm.generate_with_retry(prompt)
        
        try:
            result = json.loads(response)
        except:
            # Fallback
            result = {
                "priority": "FYI",
                "reasoning": "Could not determine priority",
                "confidence": 0.5
            }
        
        return result