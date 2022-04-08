"""create posts table

Revision ID: 44edcab034ad
Revises: 
Create Date: 2022-04-07 20:43:05.605478

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44edcab034ad'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts", sa.Column('id', sa.Integer(), nullable = False, primary_key = True),
        sa.Column('title', sa.String(), nullable = False))
    pass


def downgrade():
    op.drop_column('posts')
    pass
