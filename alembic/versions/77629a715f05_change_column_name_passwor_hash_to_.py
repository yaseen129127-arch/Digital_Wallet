"""change column name passwor_hash to password in users table

Revision ID: 77629a715f05
Revises: 698fb27fe743
Create Date: 2026-11-19 21:09:02.169211

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '77629a715f05'
down_revision: Union[str, Sequence[str], None] = '698fb27fe743'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("users","password_hash",new_column_name="password",existing_type=sa.LargeBinary(),existing_nullable=True,)


def downgrade() -> None:
    op.alter_column("users","password",new_column_name="password_hash",existing_type=sa.LargeBinary(),existing_nullable=True,)
