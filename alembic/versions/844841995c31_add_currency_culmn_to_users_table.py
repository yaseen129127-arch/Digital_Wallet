"""Add currency culmn to users table

Revision ID: 844841995c31
Revises: 16fd4ada3af3
Create Date: 2026-10-19 21:32:36.325457

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '844841995c31'
down_revision: Union[str, Sequence[str], None] = '16fd4ada3af3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users",sa.Column("currency",sa.Enum("USD", name="Currency"),nullable=False))



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "currency")
