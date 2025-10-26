"""
Chat Service
RAG (Retrieval-Augmented Generation) chat functionality
"""

from typing import List, Optional
from openai import OpenAI

from app.config import settings
from app.utils.embeddings import generate_embedding
from app.services.qdrant_service import QdrantService

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
        user_id: str,
        query: str,
        document_id: Optional[str] = None,
        conversation_history: Optional[List[dict]] = None
    ) -> dict:
        """
        Complete RAG chat pipeline
        
        Args:
            user_id: User ID
            query: User's question
            document_id: Optional document ID to search in
            conversation_history: Optional previous messages
            
        Returns:
            Dict with answer and sources
        """
        # 1. Retrieve relevant chunks
        chunks = ChatService.retrieve_relevant_chunks(
            user_id=user_id,
            query=query,
            limit=5,
            document_id=document_id
        )
        
        # 2. Build context
        context = ChatService.build_context(chunks)
        
        # 3. Generate answer
        answer = ChatService.generate_answer(
            query=query,
            context=context,
            conversation_history=conversation_history
        )
        
        # 4. Format sources
        sources = [
            {
                "document_id": chunk["document_id"],
                "filename": chunk["filename"],
                "chunk_index": chunk["chunk_index"],
                "relevance_score": chunk["similarity_score"]
            }
            for chunk in chunks
        ]
        
        return {
            "answer": answer,
            "sources": sources
        }

