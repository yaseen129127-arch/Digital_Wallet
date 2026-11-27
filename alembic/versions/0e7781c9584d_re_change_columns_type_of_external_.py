"""Re-change columns Type of external_reference and provider in external_payments table

Revision ID: 0e7781c9584d
Revises: 7e4c061ab06f
Create Date: 2026-11-14 20:20:47.317927

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e7781c9584d'
down_revision: Union[str, Sequence[str], None] = '7e4c061ab06f'
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
