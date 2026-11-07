"""Change ext_pay_id to nuallabe=true  type column in transactions table

Revision ID: 26a43e3d1941
Revises: ae27f46aaa4b
Create Date: 2026-10-20 05:50:39.225370

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26a43e3d1941'
down_revision: Union[str, Sequence[str], None] = 'ae27f46aaa4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("transactions","ext_pay_id",existing_type=sa.UUID(),nullable=True)



def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("transactions","ext_pay_id",existing_type=sa.UUID(),nullable=False)

