"""drop accounts table

Revision ID: 7424fe0aa2ea
Revises: 27f97077b18d
Create Date: 2026-10-16 09:25:56.999651

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7424fe0aa2ea'
down_revision: Union[str, Sequence[str], None] = '27f97077b18d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_table("accounts", postgresql_with="CASCADE")


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table("accounts",
        sa.Column("account_id", sa.UUID(), primary_key=True, server_default=sa.func.uuidv7()),
        sa.Column("user_id", sa.UUID(), sa.ForeignKey("users.user_id"), nullable=False),
        sa.Column("currency", sa.Enum("USD", "EUR", name="currency"), nullable=False),
        sa.Column("account_status", sa.Enum("ACTIVE", "DISABLED", name="astatus")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
