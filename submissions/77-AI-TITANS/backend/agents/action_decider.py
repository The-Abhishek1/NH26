from .base import BaseAgent
from typing import Dict, Any
import json

class ActionDeciderAgent(BaseAgent):
    def __init__(self):
        super().__init__("ActionDeciderAgent")
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        email = input_data.get("email", {})
        summary = input_data.get("summary", {})
        priority = input_data.get("priority", "FYI")
        
        prompt = f"""
        Based on the email analysis, decide the best action to take.
        
        Email Subject: {email.get('subject', '')}
        Priority: {priority}
        Summary: {summary.get('summary', [])}
        
        Choose ONE action type: "reply", "meeting", "task"
        
        Consider:
        - reply: If they're asking questions or need information
        - meeting: If they want to schedule something
        - task: If they're assigning work or there are action items
        
        Return JSON:
        {{
            "action_type": "reply",
            "reasoning": "They're asking about project timeline",
            "confidence": 0.88
        }}
        """
        
        response = await self.llm.generate_with_retry(prompt)
        
        try:
            result = json.loads(response)
        except:
            result = {
                "action_type": "reply",
                "reasoning": "Default action",
                "confidence": 0.5
            }
        
        return result