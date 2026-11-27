"""change size of card_inf column from 255 to 19 in users table

Revision ID: 698fb27fe743
Revises: e7b827232c4d
Create Date: 2026-11-18 07:40:21.260537

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '698fb27fe743'
down_revision: Union[str, Sequence[str], None] = 'e7b827232c4d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("users","card_info",existing_type=sa.VARCHAR(length=255),existing_nullable=True,type_=sa.VARCHAR(length=19),nullable=True)



def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("users","card_info",existing_type=sa.VARCHAR(length=19),type_=sa.VARCHAR(length=255),existing_nullable=True)
