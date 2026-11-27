"""change columns Type of  external_reference and provider in external_payments table

Revision ID: 7f2aaf879159
Revises: 78b93ba7dd87
Create Date: 2026-11-14 18:32:00.407468

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f2aaf879159'
down_revision: Union[str, Sequence[str], None] = '78b93ba7dd87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("external_payments","provider",existing_type=sa.VARCHAR(length=50),type_=sa.Enum("STRIPE", name="Provider"),existing_nullable=False)
    op.alter_column("external_payments","external_reference",existing_type=sa.VARCHAR(length=255),type_=sa.Uuid(as_uuid=True),existing_nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("external_payments","provider",existing_type=sa.Enum("STRIPE", name="Provider"),type_=sa.VARCHAR(length=50),existing_nullable=False)
    op.alter_column("external_payments","external_reference",existing_type=sa.Uuid(as_uuid=True),type_=sa.VARCHAR(length=255),existing_nullable=False)