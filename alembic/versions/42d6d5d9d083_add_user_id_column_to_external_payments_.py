"""Add user_id column to external_payments table

Revision ID: 42d6d5d9d083
Revises: b8b2176ca5ce
Create Date: 2026-10-16 12:47:19.963004

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '42d6d5d9d083'
down_revision: Union[str, Sequence[str], None] = 'b8b2176ca5ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("external_payments", sa.Column("user_id",sa.UUID, sa.ForeignKey("users.user_id")))



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("external_payments", "user_id")
