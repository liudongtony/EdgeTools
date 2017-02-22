"""added token

Revision ID: 758995731b53
Revises: 0fb4ec81303f
Create Date: 2017-02-19 20:32:12.697608

"""

# revision identifiers, used by Alembic.
revision = '758995731b53'
down_revision = '0fb4ec81303f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###