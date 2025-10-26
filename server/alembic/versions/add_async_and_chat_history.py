"""add async processing and chat history

Revision ID: add_async_chat
Revises: init
Create Date: 2025-10-26

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = 'add_async_chat'
down_revision = '4859628215bc'  # Previous migration
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add async processing fields to documents table
    op.add_column('documents', sa.Column('processing_status', sa.String(50), nullable=False, server_default='completed'))
    op.add_column('documents', sa.Column('processing_error', sa.String(512), nullable=True))
    op.add_column('documents', sa.Column('task_id', sa.String(255), nullable=True))
    
    # Create chat_history table
    op.create_table(
        'chat_history',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('user_message', sa.Text, nullable=False),
        sa.Column('assistant_message', sa.Text, nullable=False),
        sa.Column('vector_id', sa.String(255), nullable=True),
        sa.Column('conversation_id', UUID(as_uuid=True), nullable=True, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)
    )


def downgrade() -> None:
    # Drop chat_history table
    op.drop_table('chat_history')
    
    # Remove async processing fields from documents table
    op.drop_column('documents', 'task_id')
    op.drop_column('documents', 'processing_error')
    op.drop_column('documents', 'processing_status')

