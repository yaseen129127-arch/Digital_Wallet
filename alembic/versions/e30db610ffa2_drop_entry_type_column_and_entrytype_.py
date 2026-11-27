"""Drop entry_type column and EntryType enum from ledger_entry table and add balance , debit and credit columns 

Revision ID: e30db610ffa2
Revises: fa2269769fcc
Create Date: 2026-10-17 01:44:17.755158

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e30db610ffa2'
down_revision: Union[str, Sequence[str], None] = 'fa2269769fcc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("ledger_entry", "entry_type")
    op.execute('DROP TYPE IF EXISTS "EntryType"')
    op.add_column("ledger_entry", sa.Column("balance", sa.BigInteger, nullable=False))
    op.add_column("ledger_entry", sa.Column("credit", sa.BigInteger, nullable=False))
    op.add_column("ledger_entry", sa.Column("debit", sa.BigInteger, nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""CREATE TYPE "EntryType" AS ENUM ('DEBIT', 'CREDIT')""")
    op.add_column("ledger_entry",sa.Column("entry_type",sa.Enum("DEBIT", "CREDIT", name="EntryType", create_type=False),nullable=True,))
