"""fix Enum type 

Revision ID: 4219189092a8
Revises: edcc56d0769b
Create Date: 2026-10-16 10:43:23.037617

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4219189092a8'
down_revision: Union[str, Sequence[str], None] = 'edcc56d0769b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        DROP TYPE IF EXISTS "Astatus";
        DROP TYPE IF EXISTS "Currency";
        DROP TYPE IF EXISTS "Estatus";
        DROP TYPE IF EXISTS "Ldirection";
        DROP TYPE IF EXISTS "Otype";
        DROP TYPE IF EXISTS "Tstatus";
        DROP TYPE IF EXISTS "Ttype";
    """)
    op.execute("""
        CREATE TYPE "Currency" AS ENUM ('USD');
        CREATE TYPE "EntryType" AS ENUM ('DEBIT', 'CREDIT');
        CREATE TYPE "TransactionType" AS ENUM ('DEPOSIT', 'WITHDRAWAL', 'TRANSFER');
        CREATE TYPE "LedgerAccountType" AS ENUM ('USER_WALLET', 'PROVIDER_ESCROW', 'PLATFORM_REVENUE');
        CREATE TYPE "TransactionStatus" AS ENUM ('SUCCESS', 'FAILED', 'PENDING');
        """)



def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        DROP TYPE IF EXISTS "TransactionStatus";
        DROP TYPE IF EXISTS "LedgerAccountType";
        DROP TYPE IF EXISTS "TransactionType";
        DROP TYPE IF EXISTS "EntryType";
        DROP TYPE IF EXISTS "Currency";
    """)
