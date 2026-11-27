"""change type of column in User table to be nullable=false

Revision ID: fc2ec9860e4a
Revises: 7555aa299e22
Create Date: 2026-11-12 09:01:50.314841

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc2ec9860e4a'
down_revision: Union[str, Sequence[str], None] = '7555aa299e22'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("users","user_id",existing_type=sa.UUID(),existing_nullable=False,server_default=None,)
    op.alter_column("transactions","transaction_id",existing_type=sa.UUID(),existing_nullable=False,server_default=None,)
    op.alter_column("ledger_entry","entry_id",existing_type=sa.UUID(),existing_nullable=False,server_default=None,)
    op.alter_column("external_payments","external_payment_id",existing_type=sa.UUID(),existing_nullable=False,server_default=None,)



def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("users","user_id",existing_type=sa.UUID(),existing_nullable=False,server_default=sa.func.uuidv7(),)
    op.alter_column("transactions","transaction_id",existing_type=sa.UUID(),existing_nullable=False,server_default=sa.func.uuidv7(),)
    op.alter_column("ledger_entry","entry_id",existing_type=sa.UUID(),existing_nullable=False,server_default=sa.func.uuidv7(),)
    op.alter_column("external_payments","external_payment_id",existing_type=sa.UUID(),existing_nullable=False,server_default=sa.func.uuidv7(),)

