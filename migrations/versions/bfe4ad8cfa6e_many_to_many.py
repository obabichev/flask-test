"""many-to-many

Revision ID: bfe4ad8cfa6e
Revises: 601e1c140c19
Create Date: 2020-03-19 20:35:05.364705

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfe4ad8cfa6e'
down_revision = '601e1c140c19'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_environment',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('environment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['environment_id'], ['environment.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'environment_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_environment')
    # ### end Alembic commands ###
