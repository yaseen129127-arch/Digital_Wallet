"""Add is_active and closed_at columns to User table

Revision ID: 644fbf05532d
Revises: 26a43e3d1941
Create Date: 2026-11-04 13:39:56.206396

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '644fbf05532d'
down_revision: Union[str, Sequence[str], None] = '26a43e3d1941'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("users","first_name",existing_type=sa.VARCHAR(length=50),nullable=True)
    op.alter_column("users","last_name",existing_type=sa.VARCHAR(length=50),nullable=True)
    op.alter_column("users","email_address",existing_type=sa.VARCHAR(length=255),nullable=True)
    op.alter_column("users","phone_number",existing_type=sa.VARCHAR(length=30),nullable=True)
    op.alter_column("users","password_hash",existing_type=sa.VARCHAR(length=255),nullable=True)
    op.alter_column("external_payments","card_info",existing_type=sa.VARCHAR(length=255),nullable=True)
    op.add_column("users", sa.Column("is_active", sa.BOOLEAN(), server_default=sa.text("true"), nullable=False))
    op.add_column("users", sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True))

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "closed_at")
    op.drop_column("users", "is_active")
    op.alter_column("users","first_name",existing_type=sa.VARCHAR(length=50),nullable=False)
    op.alter_column("users","last_name",existing_type=sa.VARCHAR(length=50),nullable=False)
    op.alter_column("users","email_address",existing_type=sa.VARCHAR(length=255),nullable=False)
    op.alter_column("users","phone_number",existing_type=sa.VARCHAR(length=30),nullable=False)
    op.alter_column("users","password_hash",existing_type=sa.VARCHAR(length=255),nullable=False)
    op.alter_column("external_payments","card_info",existing_type=sa.VARCHAR(length=255),nullable=False)

