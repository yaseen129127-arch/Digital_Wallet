"""Drop direction column to ledger table

Revision ID: 1c9fac1b8f26
Revises: 42d6d5d9d083
Create Date: 2026-10-16 22:27:10.651148

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c9fac1b8f26'
down_revision: Union[str, Sequence[str], None] = '42d6d5d9d083'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("ledger_entry", "direction")
    op.add_column("ledger_entry", sa.Column("account_type",sa.Enum("USER_WALLET","PROVIDER_ESCROW","PLATFORM_REVENUE", name="LedgerAccountType"), nullable=True))
    op.add_column("ledger_entry", sa.Column("entry_type",sa.Enum("DEBIT","CREDIT", name="EntryType"),nullable=True)
                  )


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column("ledger_entry", sa.Column("direction", sa.Enum("DEBIT","CREDIT",name="Ldirection")))
