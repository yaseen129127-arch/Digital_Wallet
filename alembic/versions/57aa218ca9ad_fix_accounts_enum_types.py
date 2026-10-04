"""fix accounts enum types

Revision ID: 57aa218ca9ad
Revises: f01a3ba3b541
Create Date: 2026-10-02 07:31:22.553295

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '57aa218ca9ad'
down_revision: Union[str, Sequence[str], None] = '97c443e79c84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema"""
    """Fix accounts enum types."""

    op.execute(""" ALTER TABLE accounts ALTER COLUMN currency TYPE "Currency" USING currency::text::"Currency" """) 
    op.execute(""" DROP TYPE currency """)
    op.execute('ALTER TYPE astatus RENAME TO "Astatus"')
    op.execute('ALTER TYPE "Astatus" RENAME VALUE \'active\' TO \'ACTIVE\'' )
    op.execute('ALTER TYPE "Astatus" RENAME VALUE \'disabled\' TO \'DISABLED\'')
    op.execute('AlTER TYPE "Ldirection" RENAME VALUE \'debit\'TO\'DEBIT\'')
    op.execute('AlTER TYPE "Ldirection" RENAME VALUE \'credit\'TO\'CREDIT\'')
    op.execute('AlTER TYPE "Tstatus" RENAME VALUE \'succeeded\'TO\'COMPLETED\'')
    op.execute('AlTER TYPE "Tstatus" RENAME VALUE \'failed\'TO\'FAILURE\'')
    op.execute('AlTER TYPE "Ttype" RENAME VALUE \'internal\'TO\'INTERNAL\'')
    op.execute('AlTER TYPE "Ttype" RENAME VALUE \'topup\'TO\'TOPUP\'')
    
def downgrade() -> None:
    """Downgrade schema."""
    op.execute(""" CREATE TYPE currency AS ENUM ('USD', 'EUR') """) 
    op.execute(""" ALTER TABLE accounts ALTER COLUMN currency TYPE currency USING currency::text::currency """)
    op.execute('ALTER TYPE Astatus RENAME TO "astatus"')
    op.execute('ALTER TYPE "Astatus" RENAME VALUE \'ACTIVE\' TO \'active\'' )
    op.execute('ALTER TYPE "Astatus" RENAME VALUE \'DISABLED\' TO \'disabled\'')
    op.execute('AlTER TYPE "Ldirection" RENAME VALUE \'DEBIT\'TO\'debit\'')
    op.execute('AlTER TYPE "Ldirection" RENAME VALUE \'CREDIT\'TO\'credit\'')
    op.execute('AlTER TYPE "Tstatus" RENAME VALUE \'SUCCEEDED\'TO\'succeeded\'')
    op.execute('AlTER TYPE "Tstatus" RENAME VALUE \'FAILED\'TO\'failed\'')
    op.execute('AlTER TYPE "Ttype" RENAME VALUE \'INTERNAL\'TO\'internal\'')
    op.execute('AlTER TYPE "Ttype" RENAME VALUE \'TOPUP\'TO\'topup\'')
    
