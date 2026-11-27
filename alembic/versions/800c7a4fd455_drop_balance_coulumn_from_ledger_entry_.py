"""drop balance coulumn from ledger_entry table

Revision ID: 800c7a4fd455
Revises: a776a9104416
Create Date: 2026-11-15 09:05:54.013827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '800c7a4fd455'
down_revision: Union[str, Sequence[str], None] = 'a776a9104416'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("ledger_entry","balance")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column("ledger_entry",sa.Column("balance",sa.BigInteger,nullable=False))
