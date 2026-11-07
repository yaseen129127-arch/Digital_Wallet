"""change type in column password_hash to LargeBinary User table

Revision ID: 3d39a402d611
Revises: 644fbf05532d
Create Date: 2026-11-07 05:37:38.937788

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d39a402d611'
down_revision: Union[str, Sequence[str], None] = '644fbf05532d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
