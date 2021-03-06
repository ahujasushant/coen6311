"""empty message

Revision ID: 1671eb4d955e
Revises: 77ce474a475c
Create Date: 2020-03-27 17:01:27.612358

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1671eb4d955e'
down_revision = '77ce474a475c'
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
