"""add auth table

Revision ID: b6a1b074f564
Revises: 
Create Date: 2020-03-14 22:39:30.709959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6a1b074f564'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('demands',
    sa.Column('d_id', sa.Integer(), nullable=False),
    sa.Column('d_title', sa.String(length=32), nullable=True),
    sa.Column('d_content', sa.String(length=512), nullable=True),
    sa.Column('d_publisher', sa.String(length=256), nullable=True),
    sa.Column('d_pub_time', sa.DateTime(), nullable=True),
    sa.Column('d_is_review', sa.Boolean(), nullable=True),
    sa.Column('d_reviewer', sa.Integer(), nullable=True),
    sa.Column('d_review_time', sa.DateTime(), nullable=True),
    sa.Column('d_is_cancel', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('d_id'),
    sa.UniqueConstraint('d_id'),
    schema='app'
    )
    op.create_table('roles',
    sa.Column('r_id', sa.Integer(), nullable=False),
    sa.Column('r_name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('r_id'),
    sa.UniqueConstraint('r_id'),
    schema='app'
    )
    op.create_table('users',
    sa.Column('u_id', sa.Integer(), nullable=False),
    sa.Column('u_pwd', sa.String(length=255), nullable=True),
    sa.Column('u_name', sa.String(length=255), nullable=True),
    sa.Column('u_gender', sa.String(length=2), nullable=True),
    sa.Column('u_phone', sa.String(length=255), nullable=True),
    sa.Column('u_email', sa.String(length=255), nullable=True),
    sa.Column('u_last_login_time', sa.DateTime(), nullable=True),
    sa.Column('u_modify_time', sa.DateTime(), nullable=True),
    sa.Column('u_create_time', sa.DateTime(), nullable=True),
    sa.Column('u_role', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('u_id'),
    sa.UniqueConstraint('u_id'),
    schema='app'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users', schema='app')
    op.drop_table('roles', schema='app')
    op.drop_table('demands', schema='app')
    # ### end Alembic commands ###
