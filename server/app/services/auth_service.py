"""
Authentication Service
Business logic for user authentication
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.auth import UserSignup, UserLogin, Token, UserResponse
from app.utils.security import verify_password, get_password_hash, create_access_token


class AuthService:
    """Service for handling authentication operations"""
    
    @staticmethod
    def signup(db: Session, user_data: UserSignup) -> tuple[Token, UserResponse]:
        """
        Register a new user
        
        Args:
            db: Database session
            user_data: User signup data
            
        Returns:
            Tuple of (Token, UserResponse)
            
        Raises:
            HTTPException: If email or username already exists
        """
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.email == user_data.email) | (User.username == user_data.username)
        ).first()
        
        if existing_user:
            if existing_user.email == user_data.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Generate access token
        access_token = create_access_token(data={"sub": str(new_user.id), "email": new_user.email})
        
        token = Token(access_token=access_token, token_type="bearer")
        user_response = UserResponse(
            id=new_user.id,
            email=new_user.email,
            username=new_user.username,
            created_at=new_user.created_at
        )
        
        return token, user_response
    
    @staticmethod
    def signin(db: Session, user_data: UserLogin) -> tuple[Token, UserResponse]:
        """
        Authenticate a user and return token
        
        Args:
            db: Database session
            user_data: User login data
            
        Returns:
            Tuple of (Token, UserResponse)
            
        Raises:
            HTTPException: If credentials are invalid
        """
        # Find user by email
        user = db.query(User).filter(User.email == user_data.email).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verify password
        if not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Generate access token
        access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
        
        token = Token(access_token=access_token, token_type="bearer")
        user_response = UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            created_at=user.created_at
        )
        
        return token, user_response
    
    @staticmethod
    def get_current_user_id(token: str) -> str:
        """
        Get user ID from JWT token
        
        Args:
            token: JWT token string
            
        Returns:
            User ID as string
        """
        from app.utils.security import decode_access_token
        payload = decode_access_token(token)
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user_id

