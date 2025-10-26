"""
API Dependencies
Shared dependencies for route protection
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.auth_service import AuthService

# HTTP Bearer scheme for token extraction
security = HTTPBearer()


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> str:
    """
    Dependency to get current authenticated user ID
    
    Usage:
        @app.get("/protected")
        def protected_route(user_id: str = Depends(get_current_user_id)):
            return {"user_id": user_id}
    
    Args:
        credentials: HTTP Authorization credentials from header
        db: Database session
        
    Returns:
        User ID as string
        
    Raises:
        HTTPException: If token is invalid
    """
    token = credentials.credentials
    user_id = AuthService.get_current_user_id(token)
    return user_id

