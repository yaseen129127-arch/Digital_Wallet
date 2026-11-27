"""Re-drop card_info column from external_payments table

Revision ID: 146633cbaaaf
Revises: f9ff577a5162
Create Date: 2026-11-18 06:34:03.565736

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '146633cbaaaf'
down_revision: Union[str, Sequence[str], None] = 'f9ff577a5162'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("external_payments","card_info")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column("external_payments", sa.Column("card_info", sa.VARCHAR(255), nullable=True))
