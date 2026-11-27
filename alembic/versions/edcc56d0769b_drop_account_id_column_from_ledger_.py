"""drop account_id column from ledger_entry table 

Revision ID: edcc56d0769b
Revises: 7424fe0aa2ea
Create Date: 2026-10-16 09:51:34.194577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'edcc56d0769b'
down_revision: Union[str, Sequence[str], None] = '7424fe0aa2ea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("ledger_entry", "account_id")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column("ledger_entry",sa.Column("account_id", sa.UUID(), sa.ForeignKey("accounts.account_id")))
