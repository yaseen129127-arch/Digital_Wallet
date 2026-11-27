"""change type in column password_hash to LargeBinary User table

Revision ID: 7555aa299e22
Revises: 3d39a402d611
Create Date: 2026-11-07 05:38:37.385086

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7555aa299e22'
down_revision: Union[str, Sequence[str], None] = '3d39a402d611'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("users","password_hash",existing_type=sa.VARCHAR(length=255),type_=sa.LargeBinary(),nullable=True)



def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("users","password_hash",existing_type=sa.LargeBinary(),type_=sa.VARCHAR(length=255),nullable=True)

