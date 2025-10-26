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
    allow_origins=settings.CORS_ORIGINS,
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


# TODO: Add API routes here
# from app.api.routes import auth, upload, chat
# app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
# app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
# app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

