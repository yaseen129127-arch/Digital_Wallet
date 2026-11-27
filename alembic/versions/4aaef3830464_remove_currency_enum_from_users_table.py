"""remove currency enum from  users table

Revision ID: 4aaef3830464
Revises: 844841995c31
Create Date: 2026-10-19 22:04:04.183839

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4aaef3830464'
down_revision: Union[str, Sequence[str], None] = '844841995c31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(""" DROP TYPE currency """)



def downgrade() -> None:
    """Downgrade schema."""
    op.execute(""" CREATE TYPE currency AS ENUM ('USD', 'EUR') """) 

