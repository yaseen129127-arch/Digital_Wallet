"""Change nuallabe type for columns in tables

Revision ID: c869e927eacf
Revises: a629b0f59583
Create Date: 2026-10-20 03:08:21.045053

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c869e927eacf'
down_revision: Union[str, Sequence[str], None] = 'a629b0f59583'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("users","currency",existing_type=sa.Enum("USD", name="Currency"),nullable=False)
    op.alter_column("transactions","initiated_by_user_id",existing_type=sa.UUID(),nullable=False)
    op.alter_column("transactions","ext_pay_id",existing_type=sa.UUID(),nullable=False)
    op.alter_column("transactions", "transaction_type", existing_type=sa.Enum("DEPOSIT", "WITHDRAWAL", "TRANSFER",name="TransactionType"),nullable=False)
    op.alter_column("transactions","status",existing_type=sa.Enum("SUCCESS", "FAILED", "PENDING",name="TransactionStatus"),nullable=False)
    op.alter_column("transactions","provider_tx_id",existing_type=sa.VARCHAR(length=255),nullable=False)
    op.alter_column("ledger_entry","user_id",existing_type=sa.UUID(),nullable=False)
    op.alter_column("ledger_entry","transaction_id",existing_type=sa.UUID(),nullable=False)
    op.alter_column("ledger_entry","account_type",existing_type=sa.Enum("USER_WALLET","PROVIDER_ESCROW","PLATFORM_REVENUE",name="LedgerAccountType"),nullable=False)
    op.alter_column("ledger_entry","credit",existing_type=sa.BigInteger(),nullable=False)
    op.alter_column("ledger_entry","debit",existing_type=sa.BigInteger(),nullable=False)
    op.alter_column("external_payments","user_id",existing_type=sa.UUID(),nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("users","currency", existing_type=sa.Enum("USD", name="Currency"),nullable=True)
    op.alter_column("transactions","status",existing_type=sa.Enum("SUCCESS", "FAILED", "PENDING",name="TransactionStatus"),nullable=True)
    op.alter_column("transactions","transaction_type",existing_type=sa.Enum("DEPOSIT", "WITHDRAWAL", "TRANSFER",name="TransactionType"),nullable=True)
    op.alter_column("transactions","initiated_by_user_id",existing_type=sa.UUID(),nullable=True)
    op.alter_column("transactions","provider_tx_id",existing_type=sa.VARCHAR(length=255),nullable=True)
    op.alter_column("transactions","ext_pay_id",existing_type=sa.UUID(),nullable=True)
    op.alter_column("ledger_entry","user_id",existing_type=sa.UUID(),nullable=True)
    op.alter_column("ledger_entry","transaction_id",existing_type=sa.UUID(),nullable=True)
    op.alter_column("ledger_entry","account_type",existing_type=sa.Enum("USER_WALLET","PROVIDER_ESCROW","PLATFORM_REVENUE",name="LedgerAccountType"),nullable=True)
    op.alter_column("ledger_entry","credit",existing_type=sa.BigInteger(),nullable=True)
    op.alter_column("ledger_entry","debit",existing_type=sa.BigInteger(),nullable=True)
    op.alter_column("external_payments","user_id",existing_type=sa.UUID(),nullable=True)