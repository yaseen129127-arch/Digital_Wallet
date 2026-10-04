"""Create users table

Revision ID: 2081c6f1db9b
Revises: 
Create Date: 2026-10-01 00:08:30.271159

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision: str = '2081c6f1db9b'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("users",
    sa.Column("user_id", sa.UUID(), primary_key=True, server_default=sa.func.uuidv7()),
    sa.Column("first_name", sa.VARCHAR(50), nullable=False),
    sa.Column("last_name" , sa.VARCHAR(50), nullable=False),
    sa.Column("email_address", sa.VARCHAR(255), unique=True, nullable=False),
    sa.Column("phone_number", sa.VARCHAR(30), unique=True, nullable=False),
    sa.Column("password_hash", sa.VARCHAR(255), nullable=False), 
    sa.Column("created_at", sa.DateTime(timezone=True),server_default=sa.func.now())
    )
    
def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
