"""create users table

Revision ID: 0506d71444c8
Revises: 0c159d25483b
Create Date: 2022-04-07 21:31:04.369148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0506d71444c8'
down_revision = '0c159d25483b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer(), nullable= False),
                    sa.Column('name', sa.String(), nullable= False),
                    sa.Column('email', sa.String(), nullable= False),
                    sa.Column('password', sa.String(), nullable= False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable= False, server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
