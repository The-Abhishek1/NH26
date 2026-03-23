from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Optional
from pydantic import BaseModel, Field
from agents.factory import AgentOrchestrator
import logging

router = APIRouter(prefix="/api/email", tags=["email"])
logger = logging.getLogger(__name__)

# Initialize orchestrator (singleton)
orchestrator = AgentOrchestrator()

class EmailRequest(BaseModel):
    subject: str = Field(..., min_length=1, max_length=500)
    sender: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+$')
    body: str = Field(..., min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "subject": "Project Update",
                "sender": "john@company.com",
                "body": "We need to discuss the timeline..."
            }
        }

class ActionExecute(BaseModel):
    action_type: str
    content: dict
    approved: bool = True

@router.post("/analyze")
async def analyze_email(email: EmailRequest):
    """Analyze email using multi-agent system"""
    try:
        result = await orchestrator.process_email(email.dict())
        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        logger.error(f"Error processing email: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/execute")
async def execute_action(action: ActionExecute):
    """Execute approved action"""
    try:
        # Log execution (could connect to real services)
        logger.info(f"Executing {action.action_type}: {action.content}")
        
        # Simulate execution
        return {
            "status": "success",
            "message": f"Action {action.action_type} executed successfully",
            "execution_id": "mock-id-123"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "llm_provider": settings.LLM_PROVIDER,
        "agents": ["classifier", "summarizer", "action_decider", "action_generator"]
    }