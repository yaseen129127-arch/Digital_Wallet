"""Add currency column to users table 

Revision ID: d3db06dd2359
Revises: 4219189092a8
Create Date: 2026-10-16 11:41:04.478764

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3db06dd2359'
down_revision: Union[str, Sequence[str], None] = '4219189092a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users",sa.Column("currency",sa.Enum("USD", name="Currency"),nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "currency")
