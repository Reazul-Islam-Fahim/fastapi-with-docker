"""sub categories and relations with categories

Revision ID: d5632be6aa34
Revises: 1ba0d116ac14
Create Date: 2025-05-22 15:14:11.982097
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'd5632be6aa34'
down_revision: Union[str, None] = '1ba0d116ac14'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'sub_categories',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('description', sa.String(length=511), nullable=True),
        sa.Column('image', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.String(length=50), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.String(length=50), nullable=False, server_default=sa.text('now()')),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('categories.id'), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('sub_categories')
