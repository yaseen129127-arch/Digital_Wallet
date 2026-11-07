"""change transaction_type TYPE  from text to TransactionType 

Revision ID: b58c16ab8790
Revises: 91f002cda6ca
Create Date: 2026-10-19 22:57:49.971656

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b58c16ab8790'
down_revision: Union[str, Sequence[str], None] = '91f002cda6ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(""""
        ALTER TABLE public.transactions
        ALTER COLUMN transaction_type
        TYPE public."TransactionType"
        USING transaction_type::public."TransactionType";
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        ALTER TABLE public.transactions
        ALTER COLUMN transaction_type
        TYPE TEXT
        USING transaction_type::TEXT;
    """)
