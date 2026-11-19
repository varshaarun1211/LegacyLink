
"""Add is_public to alumni

Revision ID: 26221d59437c
Revises: 133df062cf08
"""

from alembic import op
import sqlalchemy as sa

revision = '26221d59437c'
down_revision = '133df062cf08'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('alumni') as batch_op:
        batch_op.add_column(
            sa.Column(
                'is_public',
                sa.Boolean(),
                nullable=False,
                server_default=sa.true()
            )
        )


def downgrade():
    with op.batch_alter_table('alumni') as batch_op:
        batch_op.drop_column('is_public')