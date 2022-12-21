"""add ovner fk

Revision ID: 929e353ef2de
Revises: 0f395e74a08c
Create Date: 2022-12-21 16:00:51.076013

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '929e353ef2de'
down_revision = '0f395e74a08c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key('posts_users_fkey', source_table='posts', referent_table='users', local_cols=['owner_id'],
                          remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
