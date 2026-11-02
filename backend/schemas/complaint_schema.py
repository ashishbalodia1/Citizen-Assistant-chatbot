from pydantic import BaseModel, Field
from typing import Optional

class ComplaintCreateSchema(BaseModel):
    category: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=5, max_length=1000)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    image_path: Optional[str] = None
    severity: Optional[str] = "MEDIUM"

class ComplaintConfirmSchema(BaseModel):
    session_id: str
    confirm: bool = True

