"""remove transaction_id column from external_payment table 

Revision ID: 27f97077b18d
Revises: cb31e51e13e9
Create Date: 2026-10-14 15:42:32.916334

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27f97077b18d'
down_revision: Union[str, Sequence[str], None] = 'cb31e51e13e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("external_payments", "transaction_id" )
    op.add_column("transactions", sa.Column("ext_pay_id",sa.UUID, sa.ForeignKey("external_payments.external_payment_id")))


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column("external_payments",sa.Column("transaction_id",sa.UUID, sa.ForeignKey("transactions.transaction_id")))
    op.drop_column("transactions", "ext_pay_id")
