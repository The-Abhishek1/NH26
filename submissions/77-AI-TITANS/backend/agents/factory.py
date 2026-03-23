from typing import Dict, Any, List
from .base import BaseAgent
from .classifier import ClassifierAgent
from .summarizer import SummarizerAgent
from .action_decider import ActionDeciderAgent
from .action_generator import ActionGeneratorAgent
import asyncio

class AgentOrchestrator:
    """Orchestrates multiple agents to process email"""
    
    def __init__(self):
        self.agents = {
            "classifier": ClassifierAgent(),
            "summarizer": SummarizerAgent(),
            "action_decider": ActionDeciderAgent(),
            "action_generator": ActionGeneratorAgent()
        }
        self.execution_logs = []
    
    async def process_email(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """Run all agents in sequence with shared context"""
        context = {"email": email}
        
        # Step 1: Classify priority
        priority_result = await self.agents["classifier"].execute_with_logging(context)
        context["priority"] = priority_result
        self.execution_logs.extend(self.agents["classifier"].get_logs())
        
        # Step 2: Generate summary
        summary_result = await self.agents["summarizer"].execute_with_logging(context)
        context["summary"] = summary_result
        self.execution_logs.extend(self.agents["summarizer"].get_logs())
        
        # Step 3: Decide action
        action_decision = await self.agents["action_decider"].execute_with_logging(context)
        context["action_type"] = action_decision
        self.execution_logs.extend(self.agents["action_decider"].get_logs())
        
        # Step 4: Generate action content
        context["action_type_value"] = action_decision.get("action_type")
        action_content = await self.agents["action_generator"].execute_with_logging(context)
        context["action"] = action_content
        self.execution_logs.extend(self.agents["action_generator"].get_logs())
        
        # Calculate overall confidence (average of all agents)
        confidences = [
            priority_result.get("confidence", 0.5),
            action_decision.get("confidence", 0.5)
        ]
        overall_confidence = sum(confidences) / len(confidences)
        
        return {
            "summary": summary_result.get("summary", []),
            "priority": priority_result.get("priority", "FYI"),
            "priority_reasoning": priority_result.get("reasoning", ""),
            "action": action_content,
            "confidence": overall_confidence,
            "agent_logs": self.execution_logs,
            "tone": summary_result.get("tone", "neutral"),
            "key_entities": summary_result.get("key_entities", [])
        }