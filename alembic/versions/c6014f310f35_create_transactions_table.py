"""Create transactions table

Revision ID: c6014f310f35
Revises: 4142835e3005
Create Date: 2026-10-02 04:45:42.341616

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c6014f310f35'
down_revision: Union[str, Sequence[str], None] = '1c0a2d2c4237'
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("transactions",
            sa.Column("transaction_id", sa.UUID, primary_key=True, server_default=sa.func.uuidv7()),
            sa.Column("initiated_by_user_id",sa.UUID, sa.ForeignKey("users.user_id")),
            sa.Column("transaction_type", sa.Enum( "INTERNAL","TOPUP", name="Ttype")),
            sa.Column("status", sa.Enum("SUCCEEDED","FAILED", name="Tstatus")),
            sa.Column("currency",sa.Enum("USD", "EUR", name="Currency")),
            sa.Column("amount", sa.BigInteger, nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
            )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("transactions")
