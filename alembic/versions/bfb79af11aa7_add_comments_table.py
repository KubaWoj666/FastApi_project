"""add comments table

Revision ID: bfb79af11aa7
Revises: 929e353ef2de
Create Date: 2022-12-21 16:01:30.813944

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfb79af11aa7'
down_revision = '929e353ef2de'
branch_labels = None
depends_on = None



def upgrade() -> None:
    op.create_table('comments',
                    sa.Column('comment_id', sa.Integer, primary_key=True, nullable=False),
                    sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
                    sa.Column('post_id', sa.Integer, sa.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False),
                    sa.Column('comment', sa.String, nullable=False)
                    )
    pass


def downgrade() -> None:
    op.drop_table('comments')
    pass
