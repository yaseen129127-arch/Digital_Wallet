"""Drop operation_type and status columns fom external_payments table 

Revision ID: 160f39d2d006
Revises: bdaea24577c2
Create Date: 2026-10-16 22:57:59.779762

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '160f39d2d006'
down_revision: Union[str, Sequence[str], None] = 'bdaea24577c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("external_payments","operation_type")
    op.drop_column("external_payments","status")
    op.add_column("external_payments", sa.Column("card_info", sa.VARCHAR(255), nullable=False))



def downgrade() -> None:
    """Downgrade schema."""
    op.add_column("external_payments", sa.Column("operation_type", sa.Enum("DEPOSIT","CASHOUT", name="Otype")))
    op.add_column("external_payments", sa.Column("status", sa.Enum("SUCCEEDED","FAILED",name="Estatus")))
