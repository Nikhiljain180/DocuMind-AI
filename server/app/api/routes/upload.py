"""
Document Upload Routes
"""

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.api.dependencies import get_current_user_id
from app.schemas.document import DocumentResponse
from app.services.document_service import DocumentService

router = APIRouter()


@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    """
    Upload and process a document
    
    Supported formats: PDF, DOCX, TXT, MD, CSV
    Maximum file size: 10MB
    """
    document = await DocumentService.upload_document(db, file, user_id)
    return DocumentResponse.model_validate(document)


@router.get("/", response_model=List[DocumentResponse])
def get_documents(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    """
    Get all documents for the current user
    """
    documents = DocumentService.get_user_documents(db, user_id)
    return [DocumentResponse.model_validate(doc) for doc in documents]


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    """
    Delete a document
    """
    DocumentService.delete_document(db, document_id, user_id)
    return None

