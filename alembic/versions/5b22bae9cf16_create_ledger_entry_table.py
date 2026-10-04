"""Create ledger_entry table

Revision ID: 5b22bae9cf16
Revises: 1c0a2d2c4237
Create Date: 2026-10-01 03:27:00.736914

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b22bae9cf16'
down_revision: Union[str, Sequence[str], None] = 'c6014f310f35'
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("ledger_entry",
        sa.Column("entry_id", sa.UUID(), primary_key=True, server_default=sa.func.uuidv7()),
        sa.Column("account_id", sa.UUID(), sa.ForeignKey("accounts.account_id")),
        sa.Column("transaction_id", sa.UUID(), sa.ForeignKey("transactions.transaction_id")),
        sa.Column("direction", sa.Enum("DEBIT","CREDIT",name="Ldirection")),
        sa.Column("amount", sa.BigInteger, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now())
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("ledger_entry")