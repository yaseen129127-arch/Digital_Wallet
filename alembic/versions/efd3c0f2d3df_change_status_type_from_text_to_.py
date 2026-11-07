"""Change status TYPE  from text to TransactionStatus in transactions table 

Revision ID: efd3c0f2d3df
Revises: b58c16ab8790
Create Date: 2026-10-19 23:16:00.098697

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'efd3c0f2d3df'
down_revision: Union[str, Sequence[str], None] = 'b58c16ab8790'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(""""
        ALTER TABLE public.transactions
        ALTER COLUMN status
        TYPE public."TransactionStatus"
        USING transaction_type::public."TransactionStatus";
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        ALTER TABLE public.transactions
        ALTER COLUMN status
        TYPE TEXT
        USING transaction_type::TEXT;
    """)
