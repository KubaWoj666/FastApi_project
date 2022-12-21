"""create users table

Revision ID: d1c6de341c31
Revises: 846f5a1beb6e
Create Date: 2022-12-21 15:58:54.067756

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1c6de341c31'
down_revision = '846f5a1beb6e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer, primary_key=True, nullable=False ),
                    sa.Column('email', sa.String, unique=True, nullable=False),
                    sa.Column('password', sa.String, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")
                              ))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass