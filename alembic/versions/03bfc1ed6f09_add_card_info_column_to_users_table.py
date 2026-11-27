"""add card_info column to users table

Revision ID: 03bfc1ed6f09
Revises: 146633cbaaaf
Create Date: 2026-11-18 06:36:26.752817

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '03bfc1ed6f09'
down_revision: Union[str, Sequence[str], None] = '146633cbaaaf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("card_info", sa.VARCHAR(255), nullable=True))



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users","card_info")

