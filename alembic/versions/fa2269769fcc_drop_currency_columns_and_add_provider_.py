"""Drop currency columns and add provider_tx_id for transactions table 

Revision ID: fa2269769fcc
Revises: 160f39d2d006
Create Date: 2026-10-16 23:41:55.570994

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa2269769fcc'
down_revision: Union[str, Sequence[str], None] = '160f39d2d006'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("transactions", "currency")
    op.add_column("transactions", sa.Column("provider_tx_id", sa.VARCHAR(255), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column("transactions",sa.Column("currency",sa.Enum("USD", "EUR", name="Currency")))

