"""
OpenAI Embeddings Utilities
Generate embeddings for text using OpenAI API
"""

from typing import List
from openai import OpenAI

from app.config import settings

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_embedding(text: str) -> List[float]:
    """
    Generate embedding for a single text
    
    Args:
        text: Text to embed
        
    Returns:
        Embedding vector
    """
    try:
        response = client.embeddings.create(
            model=settings.OPENAI_EMBEDDING_MODEL,
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        raise ValueError(f"Error generating embedding: {str(e)}")


def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for multiple texts
    
    Args:
        texts: List of texts to embed
        
    Returns:
        List of embedding vectors
    """
    if not texts:
        return []
    
    try:
        response = client.embeddings.create(
            model=settings.OPENAI_EMBEDDING_MODEL,
            input=texts
        )
        return [item.embedding for item in response.data]
    except Exception as e:
        raise ValueError(f"Error generating embeddings: {str(e)}")


def get_embedding_dimension() -> int:
    """
    Get the dimension of embeddings for the current model
    
    Returns:
        Embedding dimension
    """
    # text-embedding-3-small: 1536 dimensions
    # text-embedding-ada-002: 1536 dimensions
    # text-embedding-3-large: 3072 dimensions
    return 1536

