"""create votes table

Revision ID: 0f395e74a08c
Revises: d1c6de341c31
Create Date: 2022-12-21 15:59:49.540941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f395e74a08c'
down_revision = 'd1c6de341c31'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('votes',
                    sa.Column('user_id', sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True,),
                    sa.Column('post_id', sa.Integer, sa.ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
                    )
    pass


def downgrade() -> None:
    op.drop_table('votes')
    pass