"""add column school_id for foreignkey bill table with school table

Revision ID: 602010d747d3
Revises: 4014863e296b
Create Date: 2019-01-27 23:00:55.542049

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '602010d747d3'
down_revision = '4014863e296b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bill', sa.Column('school_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'bill', 'school', ['school_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'bill', type_='foreignkey')
    op.drop_column('bill', 'school_id')
    # ### end Alembic commands ###