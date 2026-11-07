""" create Cureeency enum 

Revision ID: 16fd4ada3af3
Revises: 315979e7b296
Create Date: 2026-10-19 21:16:44.279993

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16fd4ada3af3'
down_revision: Union[str, Sequence[str], None] = '315979e7b296'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE TYPE 'Currency' AS ENUM ('USD')")



def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TYPE IF EXISTS 'Currency'")

