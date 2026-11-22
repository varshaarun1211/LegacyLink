
"""Add enhanced alumni profile fields

Revision ID: 58340e53b69e
Revises: 8f3a91c2d740
Create Date: 2026-11-22 14:10:27.219649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58340e53b69e'
down_revision = '8f3a91c2d740'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('alumni', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('linkedin_url', sa.String(length=255), nullable=True)
        )
        batch_op.add_column(
            sa.Column('github_url', sa.String(length=255), nullable=True)
        )
        batch_op.add_column(
            sa.Column('portfolio_url', sa.String(length=255), nullable=True)
        )
        batch_op.add_column(
            sa.Column('career_interests', sa.Text(), nullable=True)
        )
        batch_op.add_column(
            sa.Column(
                'available_for_mentorship',
                sa.Boolean(),
                nullable=False,
                server_default=sa.false()
            )
        )


def downgrade():
    with op.batch_alter_table('alumni', schema=None) as batch_op:
        batch_op.drop_column('available_for_mentorship')
        batch_op.drop_column('career_interests')
        batch_op.drop_column('portfolio_url')
        batch_op.drop_column('github_url')
        batch_op.drop_column('linkedin_url')
