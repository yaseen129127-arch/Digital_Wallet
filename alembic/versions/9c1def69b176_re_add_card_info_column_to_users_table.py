"""Re-add card_info column to users table

Revision ID: 9c1def69b176
Revises: 03bfc1ed6f09
Create Date: 2026-11-18 06:40:13.034236

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c1def69b176'
down_revision: Union[str, Sequence[str], None] = '03bfc1ed6f09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("card_info", sa.VARCHAR(255), nullable=True))



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users","card_info")
