"""added created_at column to posts

Revision ID: 95d812e92714
Revises: b04d93adf7bd
Create Date: 2022-04-07 22:06:37.006918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95d812e92714'
down_revision = 'b04d93adf7bd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade():
    op.drop_column('posts', 'created_at')
    pass
