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


@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    """
    Upload document and queue for async processing
    
    Returns immediately with task_id for status checking
    Supported formats: PDF, DOCX, TXT, MD, CSV
    Maximum file size: 10MB
    """
    document, task_id = await DocumentService.upload_document(db, file, user_id)
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


@router.get("/{document_id}/status")
def get_document_status(
    document_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    """
    Get processing status of a document
    
    Returns: {status: "pending" | "processing" | "completed" | "failed", error: str | null}
    """
    from app.celery_app import celery_app
    from app.models.document import Document
    import uuid
    
    # Get document
    document = db.query(Document).filter(
        Document.id == uuid.UUID(document_id),
        Document.user_id == uuid.UUID(user_id)
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check Celery task status if available
    task_status = None
    if document.task_id:
        task = celery_app.AsyncResult(document.task_id)
        task_status = {
            "task_state": task.state,
            "task_info": task.info if task.info else None
        }
    
    return {
        "document_id": str(document.id),
        "filename": document.filename,
        "status": document.processing_status,
        "error": document.processing_error,
        "task": task_status
    }


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

