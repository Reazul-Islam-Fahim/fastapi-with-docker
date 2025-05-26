"""sub categories and relations with categories model updated

Revision ID: 5f20bcf7b66b
Revises: d5632be6aa34
Create Date: 2025-05-22 16:58:40.534999

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f20bcf7b66b'
down_revision: Union[str, None] = 'd5632be6aa34'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
