"""empty message

Revision ID: 5e03e4e5a458
Revises: e280cf0f2174
Create Date: 2019-05-14 12:46:04.596732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e03e4e5a458'
down_revision = 'e280cf0f2174'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('column_set', sa.Column('total', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'column_set', 'column', ['total'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'column_set', type_='foreignkey')
    op.drop_column('column_set', 'total')
    # ### end Alembic commands ###