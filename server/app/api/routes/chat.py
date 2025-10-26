"""
Chat Routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.dependencies import get_current_user_id
from app.schemas.chat import ChatRequest, ChatResponse, ChatSource
from app.services.chat_service import ChatService

router = APIRouter()


@router.post("/", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    """
    Chat with your documents using RAG
    
    Send a question and get an AI-powered answer based on your uploaded documents.
    The system will:
    1. Find relevant chunks from your documents
    2. Use them as context for GPT
    3. Generate an accurate, context-aware answer
    
    You can optionally filter by document_id to search in a specific document.
    """
    try:
        # Get document_id from conversation_id if provided (future enhancement)
        document_id = None  # Can be extracted from request if needed
        
        result = ChatService.chat(
            user_id=user_id,
            query=request.query,
            document_id=document_id,
            conversation_history=None  # Future: store conversation history
        )
        
        # Format response
        sources = [
            ChatSource(
                document_id=src["document_id"],
                filename=src["filename"],
                chunk_index=src["chunk_index"],
                relevance_score=src["relevance_score"]
            )
            for src in result["sources"]
        ]
        
        return ChatResponse(
            answer=result["answer"],
            sources=sources,
            conversation_id=request.conversation_id
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}"
        )

