"""
Document Model
"""

from sqlalchemy import Column, String, DateTime, BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.database import Base


class Document(Base):
    """
    Document model for uploaded files
    """
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    filename = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_size = Column(BigInteger, nullable=False)  # Size in bytes
    mime_type = Column(String(100), nullable=True)
    
    # Qdrant collection for this document's embeddings
    vector_collection_id = Column(String(255), nullable=True)
    
    # Processing status for async uploads
    processing_status = Column(String(50), default="pending", nullable=False)  # pending, processing, completed, failed
    processing_error = Column(String(512), nullable=True)
    task_id = Column(String(255), nullable=True)  # Celery task ID
    
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship (optional, for future use)
    # user = relationship("User", back_populates="documents")

    def __repr__(self):
        return f"<Document(id={self.id}, filename={self.filename}, user_id={self.user_id})>"


