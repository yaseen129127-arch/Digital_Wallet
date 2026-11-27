"""Add user_id column to ledger_entry table 

Revision ID: b8b2176ca5ce
Revises: d3db06dd2359
Create Date: 2026-10-16 12:30:00.208017

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8b2176ca5ce'
down_revision: Union[str, Sequence[str], None] = 'd3db06dd2359'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("ledger_entry", sa.Column("user_id",sa.UUID, sa.ForeignKey("users.user_id")))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("ledger_entry", "user_id")
