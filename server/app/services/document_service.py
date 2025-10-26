"""
Document Service
Handle document upload, processing, and storage
"""

import os
import uuid
from pathlib import Path
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status

from app.models.document import Document
from app.config import settings
from app.utils.file_parser import FileParser, chunk_text
from app.utils.embeddings import generate_embeddings
from app.services.qdrant_service import QdrantService


class DocumentService:
    """Service for handling document operations"""
    
    @staticmethod
    def validate_file(file: UploadFile) -> None:
        """
        Validate uploaded file
        
        Args:
            file: Uploaded file
            
        Raises:
            HTTPException: If file is invalid
        """
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No filename provided"
            )
        
        # Check file extension
        ext = Path(file.filename).suffix.lower()
        if ext not in settings.allowed_extensions_list:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type {ext} not supported. Allowed types: {', '.join(settings.allowed_extensions_list)}"
            )
    
    @staticmethod
    async def save_file(file: UploadFile, user_id: str) -> tuple[str, int]:
        """
        Save uploaded file to disk
        
        Args:
            file: Uploaded file
            user_id: User ID
            
        Returns:
            Tuple of (file_path, file_size)
        """
        # Create user directory
        user_dir = Path(settings.UPLOAD_DIR) / str(user_id)
        user_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        ext = Path(file.filename).suffix
        safe_filename = f"{file_id}{ext}"
        file_path = user_dir / safe_filename
        
        # Save file
        content = await file.read()
        file_size = len(content)
        
        # Check file size
        if file_size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE / 1024 / 1024}MB"
            )
        
        with open(file_path, 'wb') as f:
            f.write(content)
        
        return str(file_path), file_size
    
    @staticmethod
    def parse_and_chunk_document(file_path: str) -> list[str]:
        """
        Parse document and split into chunks
        
        Args:
            file_path: Path to document
            
        Returns:
            List of text chunks
        """
        try:
            # Parse file
            text = FileParser.parse_file(file_path)
            
            if not text:
                raise ValueError("No text extracted from document")
            
            # Split into chunks
            chunks = chunk_text(
                text,
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP
            )
            
            return chunks
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing document: {str(e)}"
            )
    
    @staticmethod
    async def upload_document(
        db: Session,
        file: UploadFile,
        user_id: str
    ) -> Document:
        """
        Handle complete document upload process
        
        Args:
            db: Database session
            file: Uploaded file
            user_id: User ID
            
        Returns:
            Created document record
        """
        # Validate file
        DocumentService.validate_file(file)
        
        # Save file
        file_path, file_size = await DocumentService.save_file(file, user_id)
        
        # Parse and chunk
        chunks = DocumentService.parse_and_chunk_document(file_path)
        
        # Create document record
        document = Document(
            user_id=uuid.UUID(user_id),
            filename=file.filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=file.content_type
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        
        # Generate embeddings and store in Qdrant
        try:
            embeddings = generate_embeddings(chunks)
            collection_name = QdrantService.create_user_collection(user_id)
            QdrantService.store_document_embeddings(
                user_id=user_id,
                document_id=document.id,
                chunks=chunks,
                embeddings=embeddings,
                filename=file.filename
            )
            
            # Update document with collection ID
            document.vector_collection_id = collection_name
            db.commit()
            db.refresh(document)
        except Exception as e:
            # If embedding fails, still return document but log error
            print(f"Error generating embeddings: {e}")
        
        return document
    
    @staticmethod
    def get_user_documents(db: Session, user_id: str) -> list[Document]:
        """
        Get all documents for a user
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            List of user documents
        """
        return db.query(Document).filter(
            Document.user_id == uuid.UUID(user_id)
        ).order_by(Document.uploaded_at.desc()).all()
    
    @staticmethod
    def delete_document(db: Session, document_id: str, user_id: str) -> bool:
        """
        Delete a document
        
        Args:
            db: Database session
            document_id: Document ID
            user_id: User ID
            
        Returns:
            True if deleted successfully
            
        Raises:
            HTTPException: If document not found or unauthorized
        """
        document = db.query(Document).filter(
            Document.id == uuid.UUID(document_id),
            Document.user_id == uuid.UUID(user_id)
        ).first()
        
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        
        # Delete embeddings from Qdrant
        try:
            QdrantService.delete_document_embeddings(user_id, document.id)
        except Exception as e:
            print(f"Error deleting embeddings: {e}")
        
        # Delete file from disk
        try:
            if os.path.exists(document.file_path):
                os.remove(document.file_path)
        except Exception as e:
            print(f"Error deleting file: {e}")
        
        # Delete from database
        db.delete(document)
        db.commit()
        
        return True

