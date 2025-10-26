"""
Chat History Model
Store user conversations for context-aware chat
"""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.database import Base


class ChatHistory(Base):
    """
    Chat history model for storing user conversations
    """
    __tablename__ = "chat_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Chat messages
    user_message = Column(Text, nullable=False)
    assistant_message = Column(Text, nullable=False)
    
    # Qdrant vector ID for this conversation
    vector_id = Column(String(255), nullable=True)
    
    # Metadata
    conversation_id = Column(UUID(as_uuid=True), nullable=True, index=True)  # For grouping related messages
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<ChatHistory(id={self.id}, user_id={self.user_id}, created_at={self.created_at})>"

