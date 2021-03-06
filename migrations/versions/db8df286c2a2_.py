"""empty message

Revision ID: db8df286c2a2
Revises: 1671eb4d955e
Create Date: 2020-03-27 17:04:09.714551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db8df286c2a2'
down_revision = '1671eb4d955e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'post', 'organization', ['organization_id'], ['id'])
    op.add_column('volunteer', sa.Column('post_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'volunteer', 'post', ['post_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'volunteer', type_='foreignkey')
    op.drop_column('volunteer', 'post_id')
    op.drop_constraint(None, 'post', type_='foreignkey')
    # ### end Alembic commands ###
