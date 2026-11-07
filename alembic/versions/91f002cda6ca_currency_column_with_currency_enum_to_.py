"""currency column with Currency enum to  users table

Revision ID: 91f002cda6ca
Revises: 4aaef3830464
Create Date: 2026-10-19 22:15:46.265491

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91f002cda6ca'
down_revision: Union[str, Sequence[str], None] = '4aaef3830464'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users",sa.Column("currency",sa.Enum("USD", name="Currency")))



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "currency")

