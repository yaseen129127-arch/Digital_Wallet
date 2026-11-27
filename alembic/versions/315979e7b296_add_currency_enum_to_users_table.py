""" Add Currency enum to users table

Revision ID: 315979e7b296
Revises: 0bb0ec6925c2
Create Date: 2026-10-19 20:59:18.191127

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '315979e7b296'
down_revision: Union[str, Sequence[str], None] = '0bb0ec6925c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users",sa.Column("currency",sa.Enum("USD", "EUR", name="Currency"), nullable= False))



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "currency")

