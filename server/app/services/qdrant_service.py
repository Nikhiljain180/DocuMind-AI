"""
Qdrant Service
Handle vector database operations
"""

from typing import List, Optional
from uuid import UUID, uuid4
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue

from app.config import settings
from app.utils.embeddings import get_embedding_dimension
from app.utils.qdrant_client import get_qdrant_client, get_collection_name


class QdrantService:
    """Service for Qdrant vector database operations"""
    
    @staticmethod
    def create_user_collection(user_id: str) -> str:
        """
        Create a Qdrant collection for a user
        
        Args:
            user_id: User ID
            
        Returns:
            Collection name
        """
        client = get_qdrant_client()
        collection_name = get_collection_name(user_id)
        
        try:
            # Check if collection exists
            collections = client.get_collections()
            existing_collections = [col.name for col in collections.collections]
            
            if collection_name not in existing_collections:
                # Create collection
                client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(
                        size=get_embedding_dimension(),
                        distance=Distance.COSINE
                    )
                )
            
            return collection_name
        except Exception as e:
            raise ValueError(f"Error creating collection: {str(e)}")
    
    @staticmethod
    def store_document_embeddings(
        user_id: str,
        document_id: UUID,
        chunks: List[str],
        embeddings: List[List[float]],
        filename: str
    ) -> None:
        """
        Store document chunk embeddings in Qdrant
        
        Args:
            user_id: User ID
            document_id: Document ID
            chunks: Text chunks
            embeddings: Embedding vectors
            filename: Original filename
        """
        client = get_qdrant_client()
        collection_name = get_collection_name(user_id)
        
        # Ensure collection exists
        QdrantService.create_user_collection(user_id)
        
        try:
            # Create points for each chunk
            points = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                point = PointStruct(
                    id=str(uuid4()),  # Unique UUID for each chunk
                    vector=embedding,
                    payload={
                        "user_id": user_id,
                        "document_id": str(document_id),
                        "chunk_index": i,
                        "chunk_text": chunk,
                        "filename": filename
                    }
                )
                points.append(point)
            
            # Upsert points in batch
            client.upsert(
                collection_name=collection_name,
                points=points
            )
        except Exception as e:
            raise ValueError(f"Error storing embeddings: {str(e)}")
    
    @staticmethod
    def search_similar_chunks(
        user_id: str,
        query_embedding: List[float],
        limit: int = 5,
        document_id: Optional[str] = None
    ) -> List[dict]:
        """
        Search for similar chunks
        
        Args:
            user_id: User ID
            query_embedding: Query embedding vector
            limit: Maximum number of results
            document_id: Optional document ID to filter by
            
        Returns:
            List of similar chunks with metadata
        """
        client = get_qdrant_client()
        collection_name = get_collection_name(user_id)
        
        try:
            # Build filter
            query_filter = None
            if document_id:
                query_filter = Filter(
                    must=[
                        FieldCondition(
                            key="document_id",
                            match=MatchValue(value=document_id)
                        )
                    ]
                )
            
            # Search
            results = client.search(
                collection_name=collection_name,
                query_vector=query_embedding,
                limit=limit,
                query_filter=query_filter
            )
            
            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "document_id": result.payload["document_id"],
                    "filename": result.payload["filename"],
                    "chunk_index": result.payload["chunk_index"],
                    "chunk_text": result.payload["chunk_text"],
                    "similarity_score": result.score
                })
            
            return formatted_results
        except Exception as e:
            raise ValueError(f"Error searching: {str(e)}")
    
    @staticmethod
    def delete_document_embeddings(user_id: str, document_id: UUID) -> None:
        """
        Delete all embeddings for a document
        
        Args:
            user_id: User ID
            document_id: Document ID
        """
        client = get_qdrant_client()
        collection_name = get_collection_name(user_id)
        
        try:
            # Delete points with matching document_id
            client.delete(
                collection_name=collection_name,
                points_selector=Filter(
                    must=[
                        FieldCondition(
                            key="document_id",
                            match=MatchValue(value=str(document_id))
                        )
                    ]
                )
            )
        except Exception as e:
            print(f"Error deleting embeddings: {e}")

