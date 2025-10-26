"""
Qdrant Client Configuration
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.config import settings


def get_qdrant_client() -> QdrantClient:
    """
    Create and return Qdrant client instance
    """
    client = QdrantClient(
        host=settings.QDRANT_HOST,
        port=settings.QDRANT_PORT,
        https=False
    )
    return client


def create_collection_if_not_exists(collection_name: str, vector_size: int = 1536):
    """
    Create a Qdrant collection if it doesn't exist
    
    Args:
        collection_name: Name of the collection
        vector_size: Size of the embedding vectors (default: 1536 for text-embedding-3-small)
    """
    client = get_qdrant_client()
    
    try:
        # Check if collection exists
        collections = client.get_collections()
        existing_collections = [col.name for col in collections.collections]
        
        if collection_name not in existing_collections:
            # Create collection
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )
            return True
        return False
    except Exception as e:
        print(f"Error creating Qdrant collection: {e}")
        raise


def get_collection_name(user_id: str) -> str:
    """
    Generate collection name for a user
    
    Args:
        user_id: User's UUID
        
    Returns:
        Collection name in format: user_{user_id}_documents
    """
    return f"user_{user_id}_documents"

