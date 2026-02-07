from pydantic import BaseModel, Field
from typing import List, Optional


class ChatRequest(BaseModel):
    user_id: str
    message: str
    location: str = "unknown"


class ChatResponse(BaseModel):
    reply: str
    level: int
    confidence: float
    similar_cases: List[str] = []
    tracking_id: Optional[str] = None


class ComplaintRequest(BaseModel):
    user_id: str
    text: str
    location: str


class ComplaintResponse(BaseModel):
    tracking_id: str
    level: int
    authority: str
    status: str


class FeedbackRequest(BaseModel):
    user_id: str
    tracking_id: str
    rating: int = Field(ge=1, le=5)
    comment: str = ""


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
