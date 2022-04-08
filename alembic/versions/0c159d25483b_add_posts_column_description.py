"""add posts column description

Revision ID: 0c159d25483b
Revises: 44edcab034ad
Create Date: 2022-04-07 21:25:58.154099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c159d25483b'
down_revision = '44edcab034ad'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('description', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'description')
    pass
