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
    Chat with your documents using RAG + Chat History
    
    Send a question and get an AI-powered answer based on:
    1. Your uploaded documents (70% weight)
    2. Previous conversation context (30% weight)
    
    The system will:
    1. Find relevant chunks from documents AND past conversations
    2. Use them as context for GPT
    3. Generate an accurate, context-aware answer
    4. Store this conversation for future context
    
    Provide conversation_id to maintain conversation continuity.
    """
    try:
        result = ChatService.chat(
            db=db,
            user_id=user_id,
            query=request.query,
            document_id=None,  # Can be added to request if needed
            conversation_id=request.conversation_id
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
            conversation_id=result["conversation_id"],
            chat_context_used=result.get("chat_context_used", False)
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

