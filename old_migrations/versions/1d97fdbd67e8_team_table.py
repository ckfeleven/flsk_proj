"""team table

Revision ID: 1d97fdbd67e8
Revises: 98b5f301db7a
Create Date: 2018-08-08 20:44:27.879589

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d97fdbd67e8'
down_revision = '98b5f301db7a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('team',
    sa.Column('team', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('team')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('team')
    # ### end Alembic commands ###
