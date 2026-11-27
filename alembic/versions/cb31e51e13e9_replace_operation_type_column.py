"""replace operation type column

Revision ID: cb31e51e13e9
Revises: 57aa218ca9ad
Create Date: 2026-10-14 10:24:47.917404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb31e51e13e9'
down_revision: Union[str, Sequence[str], None] = '57aa218ca9ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("external_payments","operation_type")
    op.add_column("external_payments",sa.Column("operation_type", sa.Enum("DEBIT","CREDIT", name="Ldirection"), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("external_payments","operation_type")

    op.add_column("external_payments",sa.Column("operation_type",sa.Enum("DEPOSIT","CASHOUT",name="otype",)))
