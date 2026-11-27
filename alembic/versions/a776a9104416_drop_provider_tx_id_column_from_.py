"""drop provider_tx_id column from transactions table

Revision ID: a776a9104416
Revises: 0e7781c9584d
Create Date: 2026-11-14 23:09:35.244853

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a776a9104416'
down_revision: Union[str, Sequence[str], None] = '0e7781c9584d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("transactions", "provider_tx_id")



def downgrade() -> None:
    """Downgrade schema."""
    op.add_column("transactions",sa.Column("provider_tx_id",sa.VARCHAR(length=255),nullable=True))

