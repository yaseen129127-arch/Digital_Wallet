"""Change status TYPE  from text to TransactionStatus in transactions table 

Revision ID: a629b0f59583
Revises: efd3c0f2d3df
Create Date: 2026-10-19 23:23:23.270666

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a629b0f59583'
down_revision: Union[str, Sequence[str], None] = 'efd3c0f2d3df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        ALTER TABLE public.transactions
        ALTER COLUMN status
        TYPE public."TransactionStatus"
        USING status::text::public."TransactionStatus";
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        ALTER TABLE public.transactions
        ALTER COLUMN status
        TYPE TEXT
        USING status::text;
    """)