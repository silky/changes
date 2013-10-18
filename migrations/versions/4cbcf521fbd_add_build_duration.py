"""Add build.duration

Revision ID: 4cbcf521fbd
Revises: 1727bbb8da2e
Create Date: 2013-10-17 16:24:37.141304

"""

# revision identifiers, used by Alembic.
revision = '4cbcf521fbd'
down_revision = '1727bbb8da2e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('build', sa.Column('duration', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('build', 'duration')
    ### end Alembic commands ###