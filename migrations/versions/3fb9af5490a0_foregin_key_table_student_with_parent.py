"""foregin key table student with parent

Revision ID: 3fb9af5490a0
Revises: 39b8e42033df
Create Date: 2019-01-27 14:58:38.064635

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3fb9af5490a0'
down_revision = '39b8e42033df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student', sa.Column('parent_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'student', 'parent', ['parent_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'student', type_='foreignkey')
    op.drop_column('student', 'parent_id')
    # ### end Alembic commands ###
