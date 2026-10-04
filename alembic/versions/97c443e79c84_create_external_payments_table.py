"""Create external_payments table

Revision ID: 97c443e79c84
Revises: 5b22bae9cf16
Create Date: 2026-10-02 05:52:37.069220

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97c443e79c84'
down_revision: Union[str, Sequence[str], None] = '5b22bae9cf16'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("external_payments",
        sa.Column("external_payment_id",sa.UUID, primary_key=True, server_default=sa.func.uuidv7()),
        sa.Column("transaction_id",sa.UUID, sa.ForeignKey("transactions.transaction_id")),
        sa.Column("provider", sa.VARCHAR(50),nullable=False),
        sa.Column("external_reference", sa.VARCHAR(255), nullable=False),
        sa.Column("operation_type", sa.Enum("DEPOSIT","CASHOUT", name="Otype")), 
        sa.Column("status", sa.Enum("SUCCEEDED","FAILED",name="Estatus")),
        sa.Column("created_at",sa.DateTime(timezone=True), server_default=sa.func.now())
        )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("external_payments")
