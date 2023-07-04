"""add aditional fiel for user

Revision ID: 65a85a767493
Revises: b95c63435611
Create Date: 2023-07-04 23:18:46.323625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65a85a767493'
down_revision = 'b95c63435611'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('full_name', sa.String(), nullable=True))
    op.add_column('user', sa.Column('given_name', sa.String(), nullable=True))
    op.add_column('user', sa.Column('family_name', sa.String(), nullable=True))
    op.add_column('user', sa.Column('location', sa.String(), nullable=True))
    op.add_column('user', sa.Column('avatar', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'avatar')
    op.drop_column('user', 'location')
    op.drop_column('user', 'family_name')
    op.drop_column('user', 'given_name')
    op.drop_column('user', 'full_name')
    # ### end Alembic commands ###