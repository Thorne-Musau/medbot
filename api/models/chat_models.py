from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Message(BaseModel):
    role: str = Field(..., description="Role of the message sender (user or assistant)")
    content: str = Field(..., description="Content of the message")
    timestamp: datetime = Field(default_factory=datetime.now)

class Conversation(BaseModel):
    id: Optional[int] = None
    user_id: int
    title: str = Field(..., max_length=100)
    messages: List[Message] = []
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class ConversationCreate(BaseModel):
    title: str = Field(..., max_length=100)

class ConversationUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)

class ConversationInDB(Conversation):
    id: int

    class Config:
        orm_mode = True

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    message: str
    conversation_id: int
    symptoms: List[str] = []
    diagnosis: Optional[dict] = None 