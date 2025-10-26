"""
Celery Tasks
"""

from app.tasks.document_tasks import process_document_async

__all__ = ["process_document_async"]

