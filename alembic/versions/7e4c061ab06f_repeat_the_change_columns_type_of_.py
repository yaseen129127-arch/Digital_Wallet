"""repeat the change columns Type of external_reference and provider in external_payments table

Revision ID: 7e4c061ab06f
Revises: 7f2aaf879159
Create Date: 2026-11-14 19:47:11.346642

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e4c061ab06f'
down_revision: Union[str, Sequence[str], None] = '7f2aaf879159'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("external_payments","provider",existing_type=sa.VARCHAR(length=50),existing_nullable=False,type_=sa.Enum("STRIPE", name="Provider"),nullable=False,postgresql_using='"provider"::"Provider"')
    op.alter_column("external_payments","external_reference",existing_type=sa.VARCHAR(length=255),existing_nullable=False,type_=sa.Uuid(as_uuid=True),nullable=False,postgresql_using='"external_reference"::uuid')

def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("external_payments","provider",existing_type=sa.Enum("STRIPE", name="Provider"),existing_nullable=False,type_=sa.VARCHAR(length=50),nullable=False,postgresql_using='"provider"::varchar')
    op.alter_column("external_payments","external_reference",existing_type=sa.Uuid(as_uuid=True),existing_nullable=False,type_=sa.VARCHAR(length=255),nullable=False,postgresql_using='"external_reference"::varchar')

