"""Create Provider Enum

Revision ID: 78b93ba7dd87
Revises: fc2ec9860e4a
Create Date: 2026-11-14 15:20:46.214821

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import enum


# revision identifiers, used by Alembic.
revision: str = '78b93ba7dd87'
down_revision: Union[str, Sequence[str], None] = 'fc2ec9860e4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


class Provider(enum.Enum):
    STRIPE = "STRIPE"
    
def upgrade() -> None:
    """Upgrade schema."""
    sa.Enum(Provider,name="Provider").create(op.get_bind(),checkfirst=True)

def downgrade() -> None:
    """Downgrade schema."""
    sa.Enum(Provider,name="Provider").drop(op.get_bind(),checkfirst=True)