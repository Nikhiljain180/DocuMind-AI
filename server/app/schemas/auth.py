"""
Authentication Schemas
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID


class UserSignup(BaseModel):
    """Schema for user signup"""
    email: EmailStr
    username: str
    password: str


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for authentication token response"""
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Schema for user information response"""
    id: UUID
    email: str
    username: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class TokenData(BaseModel):
    """Schema for token payload"""
    user_id: UUID
    email: str

