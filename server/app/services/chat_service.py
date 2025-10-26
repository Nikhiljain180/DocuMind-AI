"""
Chat Service
RAG (Retrieval-Augmented Generation) chat functionality
WITH CHAT HISTORY SUPPORT
"""

from typing import List, Optional
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from openai import OpenAI

from app.config import settings
from app.utils.embeddings import generate_embedding
from app.services.qdrant_service import QdrantService
from app.models.chat_history import ChatHistory

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)


class ChatService:
    """Service for handling RAG-powered chat"""
    
    @staticmethod
    def retrieve_relevant_chunks(
        user_id: str,
        query: str,
        limit: int = 5,
        document_id: Optional[str] = None
    ) -> List[dict]:
        """
        Retrieve relevant document chunks for a query
        
        Args:
            user_id: User ID
            query: User's question
            limit: Maximum number of chunks to retrieve
            document_id: Optional document ID to filter by
            
        Returns:
            List of relevant chunks with metadata
        """
        # Generate embedding for query
        query_embedding = generate_embedding(query)
        
        # Search in Qdrant
        results = QdrantService.search_similar_chunks(
            user_id=user_id,
            query_embedding=query_embedding,
            limit=limit,
            document_id=document_id
        )
        
        return results
    
    @staticmethod
    def build_context(chunks: List[dict]) -> str:
        """
        Build context string from retrieved chunks
        
        Args:
            chunks: List of retrieved chunks
            
        Returns:
            Formatted context string
        """
        if not chunks:
            return "No relevant documents found."
        
        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            context_parts.append(
                f"[Document: {chunk['filename']}, Chunk {chunk['chunk_index']}]\n"
                f"{chunk['chunk_text']}\n"
            )
        
        return "\n".join(context_parts)
    
    @staticmethod
    def generate_answer(
        query: str,
        context: str,
        conversation_history: Optional[List[dict]] = None
    ) -> str:
        """
        Generate answer using GPT with RAG context
        
        Args:
            query: User's question
            context: Retrieved context from documents
            conversation_history: Optional previous messages
            
        Returns:
            Generated answer
        """
        # Build system prompt
        system_prompt = (
            "You are a helpful AI assistant that answers questions based on the provided context. "
            "Use the context below to answer the user's question accurately. "
            "If the answer cannot be found in the context, say so politely and provide general information if appropriate. "
            "Always cite which document the information comes from when possible.\n\n"
            f"Context:\n{context}"
        )
        
        # Build messages
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add current query
        messages.append({"role": "user", "content": query})
        
        try:
            # Call OpenAI
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise ValueError(f"Error generating answer: {str(e)}")
    
    @staticmethod
    def chat(
        db: Session,
        user_id: str,
        query: str,
        document_id: Optional[str] = None,
        conversation_id: Optional[str] = None
    ) -> dict:
        """
        Complete RAG chat pipeline WITH CHAT HISTORY
        
        Args:
            db: Database session
            user_id: User ID
            query: User's question
            document_id: Optional document ID to search in
            conversation_id: Optional conversation ID for grouping messages
            
        Returns:
            Dict with answer, sources, and conversation_id
        """
        # Generate embedding for query
        query_embedding = generate_embedding(query)
        
        # 1. Search both documents AND chat history
        combined_results = QdrantService.search_combined(
            user_id=user_id,
            query_embedding=query_embedding,
            limit=10,
            document_weight=0.7,  # 70% weight to documents
            chat_weight=0.3       # 30% weight to chat history
        )
        
        document_chunks = combined_results["document_results"]
        chat_chunks = combined_results["chat_results"]
        
        # 2. Build context from documents
        doc_context = ChatService.build_context(document_chunks)
        
        # 3. Build context from chat history
        chat_context = ""
        if chat_chunks:
            chat_context = "\n\nPrevious conversation context:\n"
            for i, chat in enumerate(chat_chunks, 1):
                chat_context += f"[Previous conversation {i}]: {chat['text']}\n"
        
        # Combine contexts
        full_context = doc_context + chat_context
        
        # 4. Generate answer
        answer = ChatService.generate_answer(
            query=query,
            context=full_context,
            conversation_history=None  # Context already included above
        )
        
        # 5. Store this interaction in database and Qdrant
        conv_id = UUID(conversation_id) if conversation_id else uuid4()
        
        # Create chat history record
        chat_record = ChatHistory(
            user_id=UUID(user_id),
            user_message=query,
            assistant_message=answer,
            conversation_id=conv_id
        )
        
        db.add(chat_record)
        db.commit()
        db.refresh(chat_record)
        
        # Generate embedding for this conversation
        conversation_text = f"User: {query}\nAssistant: {answer}"
        conversation_embedding = generate_embedding(conversation_text)
        
        # Store in Qdrant
        vector_id = QdrantService.store_chat_history_embedding(
            user_id=user_id,
            chat_id=chat_record.id,
            conversation_text=conversation_text,
            embedding=conversation_embedding,
            conversation_id=conv_id
        )
        
        # Update chat record with vector ID
        chat_record.vector_id = vector_id
        db.commit()
        
        # 6. Format sources (only from documents, not chat history)
        sources = [
            {
                "document_id": chunk["document_id"],
                "filename": chunk["filename"],
                "chunk_index": chunk["chunk_index"],
                "relevance_score": chunk["similarity_score"]
            }
            for chunk in document_chunks
        ]
        
        return {
            "answer": answer,
            "sources": sources,
            "conversation_id": str(conv_id),
            "chat_context_used": len(chat_chunks) > 0
        }

