"""
Document Schemas
"""

from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional


class DocumentUpload(BaseModel):
    """Schema for document upload"""
    filename: str
    file_size: int
    mime_type: Optional[str] = None


class DocumentResponse(BaseModel):
    """Schema for document information response"""
    id: UUID
    user_id: UUID
    filename: str
    file_size: int
    mime_type: Optional[str]
    vector_collection_id: Optional[str]
    uploaded_at: datetime
    
    class Config:
        from_attributes = True

