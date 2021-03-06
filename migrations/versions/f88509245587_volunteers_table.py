"""volunteers table

Revision ID: f88509245587
Revises: 
Create Date: 2020-03-12 18:07:20.231334

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f88509245587'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('volunteer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('dob', sa.String(length=120), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('street_name', sa.String(length=128), nullable=True),
    sa.Column('street_number', sa.String(length=128), nullable=True),
    sa.Column('post_code', sa.String(length=128), nullable=True),
    sa.Column('country', sa.String(length=128), nullable=True),
    sa.Column('phone', sa.String(length=128), nullable=True),
    sa.Column('days_of_availability', sa.String(length=128), nullable=True),
    sa.Column('areas_of_interest', sa.String(length=128), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_volunteer_email'), 'volunteer', ['email'], unique=True)
    op.create_index(op.f('ix_volunteer_name'), 'volunteer', ['name'], unique=True)

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_volunteer_name'), table_name='volunteer')
    op.drop_index(op.f('ix_volunteer_email'), table_name='volunteer')
    op.drop_table('volunteer')
    # ### end Alembic commands ###
