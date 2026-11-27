"""remove currency column and enum from users table

Revision ID: 0bb0ec6925c2
Revises: e30db610ffa2
Create Date: 2026-10-17 03:12:28.560127

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0bb0ec6925c2'
down_revision: Union[str, Sequence[str], None] = 'e30db610ffa2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("users", "currency")
    op.execute("DROP TYPE IF EXISTS.Currency")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column("users",sa.Column("currency",sa.Enum("USD", name="Currency"),nullable=False))

