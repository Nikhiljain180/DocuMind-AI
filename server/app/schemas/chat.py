"""
Chat Schemas
"""

from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class ChatRequest(BaseModel):
    """Schema for chat request"""
    query: str
    conversation_id: Optional[UUID] = None


class ChatSource(BaseModel):
    """Schema for chat source document"""
    document_id: UUID
    filename: str
    chunk_index: int
    relevance_score: float


class ChatResponse(BaseModel):
    """Schema for chat response"""
    answer: str
    sources: list[ChatSource]
    conversation_id: Optional[UUID] = None
    chat_context_used: bool = False  # Whether previous conversations were used

