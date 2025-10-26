"""
FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="DocuMind AI - RAG-powered document Q&A API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to DocuMind AI API",
        "version": "0.1.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# API Routes
from app.api.routes import auth, upload, chat

# Authentication routes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

# Document upload routes
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])

# Chat routes (RAG)
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

