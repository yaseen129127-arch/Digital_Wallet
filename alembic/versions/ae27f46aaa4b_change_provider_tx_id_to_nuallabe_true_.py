"""Change provider_tx_id to nuallabe=true  type column in transactions table

Revision ID: ae27f46aaa4b
Revises: 694de7cfd553
Create Date: 2026-10-20 05:38:15.478988

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae27f46aaa4b'
down_revision: Union[str, Sequence[str], None] = '694de7cfd553'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("transactions","provider_tx_id",existing_type=sa.VARCHAR(length=255),nullable=True)



def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("transactions","provider_tx_id",existing_type=sa.VARCHAR(length=255),nullable=False)

