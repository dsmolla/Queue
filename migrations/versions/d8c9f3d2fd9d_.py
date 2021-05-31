"""empty message

Revision ID: d8c9f3d2fd9d
Revises: 
Create Date: 2021-05-30 20:47:58.766435

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8c9f3d2fd9d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('questions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question', sa.Text(), nullable=True),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('asked_by', sa.Integer(), nullable=True),
    sa.Column('answered_by', sa.Integer(), nullable=True),
    sa.Column('answer', sa.Text(), nullable=True),
    sa.Column('time_asked', sa.DateTime(), nullable=True),
    sa.Column('time_answered', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fname', sa.Text(), nullable=True),
    sa.Column('lname', sa.Text(), nullable=True),
    sa.Column('email', sa.Text(), nullable=True),
    sa.Column('password', sa.Text(), nullable=True),
    sa.Column('role', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('questions')
    # ### end Alembic commands ###
