"""adding foreign-key to posts

Revision ID: b04d93adf7bd
Revises: 0506d71444c8
Create Date: 2022-04-07 21:58:08.653582

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b04d93adf7bd'
down_revision = '0506d71444c8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts',
         referent_table='users', local_cols=['user_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('post_users_fk', 'posts')
    op.drop_column('posts', 'user_id')
    pass
