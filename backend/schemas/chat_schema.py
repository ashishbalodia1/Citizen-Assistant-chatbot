from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: Optional[str] = None
    language: Optional[str] = "auto"
    coordinates: Optional[Dict[str, float]] = None

class ChatResponse(BaseModel):
    success: bool
    response: str
    type: Optional[str] = "TEXT"
    data: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None

