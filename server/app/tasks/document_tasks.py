"""
Document Processing Tasks
Async background jobs for document upload and processing
"""

import os
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.celery_app import celery_app
from app.config import settings
from app.models.document import Document
from app.utils.file_parser import FileParser, chunk_text
from app.utils.embeddings import generate_embeddings
from app.services.qdrant_service import QdrantService


# Create database session for Celery tasks
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@celery_app.task(bind=True, name="process_document_async")
def process_document_async(self, document_id: str, user_id: str, file_path: str, filename: str):
    """
    Process document asynchronously: parse, chunk, embed, and store in Qdrant
    
    Args:
        self: Celery task instance
        document_id: Document UUID
        user_id: User UUID
        file_path: Path to uploaded file
        filename: Original filename
        
    Returns:
        Dict with status and collection_name
    """
    db = SessionLocal()
    
    try:
        # Update task status
        self.update_state(state='PROCESSING', meta={'status': 'Parsing document...'})
        
        # 1. Parse document
        text = FileParser.parse_file(file_path)
        if not text:
            raise ValueError("No text extracted from document")
        
        # Update task status
        self.update_state(state='PROCESSING', meta={'status': 'Chunking text...'})
        
        # 2. Split into chunks
        chunks = chunk_text(
            text,
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        
        # Update task status
        self.update_state(state='PROCESSING', meta={'status': f'Generating embeddings for {len(chunks)} chunks...'})
        
        # 3. Generate embeddings
        embeddings = generate_embeddings(chunks)
        
        # Update task status
        self.update_state(state='PROCESSING', meta={'status': 'Storing in vector database...'})
        
        # 4. Store in Qdrant
        collection_name = QdrantService.create_user_collection(user_id)
        QdrantService.store_document_embeddings(
            user_id=user_id,
            document_id=uuid.UUID(document_id),
            chunks=chunks,
            embeddings=embeddings,
            filename=filename
        )
        
        # 5. Update document record with collection ID
        document = db.query(Document).filter(Document.id == uuid.UUID(document_id)).first()
        if document:
            document.vector_collection_id = collection_name
            document.processing_status = "completed"
            db.commit()
        
        db.close()
        
        return {
            'status': 'success',
            'collection_name': collection_name,
            'chunks_processed': len(chunks)
        }
        
    except Exception as e:
        # Update document status to failed
        document = db.query(Document).filter(Document.id == uuid.UUID(document_id)).first()
        if document:
            document.processing_status = "failed"
            document.processing_error = str(e)
            db.commit()
        
        db.close()
        
        # Raise exception for Celery to mark task as failed
        raise Exception(f"Document processing failed: {str(e)}")

