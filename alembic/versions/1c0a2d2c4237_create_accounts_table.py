"""Create accounts table

Revision ID: 1c0a2d2c4237
Revises: 2081c6f1db9b
Create Date: 2026-10-01 02:35:20.362111

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c0a2d2c4237'
down_revision: Union[str, Sequence[str], None] = '2081c6f1db9b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("accounts",
        sa.Column("account_id",sa.UUID(),primary_key=True,server_default=sa.func.uuidv7()),
        sa.Column("user_id",sa.UUID(),sa.ForeignKey("users.user_id"),nullable=False),
        sa.Column("currency",sa.Enum("USD", "EUR", name="currency"),nullable=False),
        sa.Column("account_status",sa.Enum("ACTIVE", "DISABLED", name="astatus")),
        sa.Column("created_at",sa.DateTime(timezone=True),server_default=sa.func.now()),
        )
def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("accounts")