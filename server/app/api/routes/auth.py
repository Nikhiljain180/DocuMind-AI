"""
Authentication Routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Any

from app.database import get_db
from app.schemas.auth import UserSignup, UserLogin, Token, UserResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/signup", response_model=dict[str, Any], status_code=status.HTTP_201_CREATED)
def signup(
    user_data: UserSignup,
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    """
    Register a new user
    
    Returns:
        Token and user information
    """
    token, user_response = AuthService.signup(db, user_data)
    
    return {
        "access_token": token.access_token,
        "token_type": token.token_type,
        "user": user_response.model_dump()
    }


@router.post("/signin", response_model=dict[str, Any])
def signin(
    user_data: UserLogin,
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    """
    Authenticate user and return token
    
    Returns:
        Token and user information
    """
    token, user_response = AuthService.signin(db, user_data)
    
    return {
        "access_token": token.access_token,
        "token_type": token.token_type,
        "user": user_response.model_dump()
    }


@router.post("/logout")
def logout():
    """
    Logout user (client should discard token)
    
    Note: Since we use JWT, there's no server-side logout needed.
    Client should simply discard the token.
    """
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Get current authenticated user information
    """
    from app.services.auth_service import AuthService
    from app.models.user import User
    import uuid
    
    token = credentials.credentials
    user_id_str = AuthService.get_current_user_id(token)
    user_id = uuid.UUID(user_id_str)
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        created_at=user.created_at
    )

