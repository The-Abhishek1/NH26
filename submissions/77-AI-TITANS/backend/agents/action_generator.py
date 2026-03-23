from .base import BaseAgent
from typing import Dict, Any
import json

class ActionGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__("ActionGeneratorAgent")
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        email = input_data.get("email", {})
        action_type = input_data.get("action_type", "reply")
        
        if action_type == "reply":
            return await self._generate_reply(email)
        elif action_type == "meeting":
            return await self._generate_meeting(email)
        elif action_type == "task":
            return await self._generate_task(email)
        else:
            return {"type": "unknown", "content": "No action generated"}
    
    async def _generate_reply(self, email: Dict) -> Dict:
        prompt = f"""
        Draft a professional email reply to:
        
        From: {email.get('sender')}
        Subject: {email.get('subject')}
        Content: {email.get('body')}
        
        Write a concise, professional reply.
        """
        
        draft = await self.llm.generate_with_retry(prompt)
        
        return {
            "type": "reply",
            "content": draft,
            "metadata": {
                "to": email.get("sender"),
                "subject": f"Re: {email.get('subject')}"
            }
        }
    
    async def _generate_meeting(self, email: Dict) -> Dict:
        prompt = f"""
        Extract meeting details from this email:
        
        {email.get('body')}
        
        Return JSON:
        {{
            "title": "Meeting title",
            "date": "YYYY-MM-DD",
            "time": "HH:MM",
            "participants": ["email1", "email2"],
            "duration_minutes": 60
        }}
        """
        
        response = await self.llm.generate_with_retry(prompt)
        
        try:
            meeting_details = json.loads(response)
        except:
            meeting_details = {
                "title": "Meeting",
                "date": "TBD",
                "time": "TBD",
                "participants": []
            }
        
        return {
            "type": "meeting",
            "content": meeting_details,
            "calendar_event": meeting_details
        }
    
    async def _generate_task(self, email: Dict) -> Dict:
        prompt = f"""
        Extract tasks and deadlines from this email:
        
        {email.get('body')}
        
        Return JSON:
        {{
            "tasks": [
                {{"name": "Task 1", "deadline": "YYYY-MM-DD", "priority": "high"}},
                {{"name": "Task 2", "deadline": "YYYY-MM-DD", "priority": "medium"}}
            ]
        }}
        """
        
        response = await self.llm.generate_with_retry(prompt)
        
        try:
            task_details = json.loads(response)
        except:
            task_details = {"tasks": [{"name": "Review email", "deadline": "ASAP"}]}
        
        return {
            "type": "task",
            "content": task_details,
            "todo_list": task_details.get("tasks", [])
        }