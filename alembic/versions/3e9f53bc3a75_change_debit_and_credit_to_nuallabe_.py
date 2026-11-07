"""Change debit and credit to nuallabe=true  type column in ledger table

Revision ID: 3e9f53bc3a75
Revises: c869e927eacf
Create Date: 2026-10-20 05:20:21.060401

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e9f53bc3a75'
down_revision: Union[str, Sequence[str], None] = 'c869e927eacf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("ledger_entry","credit",existing_type=sa.BigInteger(),nullable=True)
    op.alter_column("ledger_entry","debit",existing_type=sa.BigInteger(),nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("ledger_entry","credit",existing_type=sa.BigInteger(),nullable=False)
    op.alter_column("ledger_entry","debit",existing_type=sa.BigInteger(),nullable=False)
