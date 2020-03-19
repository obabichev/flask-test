"""resource

Revision ID: 601e1c140c19
Revises: 731253129be2
Create Date: 2020-03-19 20:16:41.579671

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '601e1c140c19'
down_revision = '731253129be2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('environment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('resource',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('environment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['environment_id'], ['environment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('resource')
    op.drop_table('environment')
    # ### end Alembic commands ###
