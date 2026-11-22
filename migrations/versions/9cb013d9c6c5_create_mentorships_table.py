
"""Create mentorships table."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision = "9cb013d9c6c5"
down_revision = "f94e75be7db9"
branch_labels = None
depends_on = None


def upgrade():
    # The table may already exist locally because app.py calls db.create_all().
    bind = op.get_bind()
    inspector = inspect(bind)

    if "mentorships" not in inspector.get_table_names():
        op.create_table(
            "mentorships",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("mentor_id", sa.Integer(), nullable=False),
            sa.Column("mentee_id", sa.Integer(), nullable=False),
            sa.Column("message", sa.Text(), nullable=True),
            sa.Column(
                "status",
                sa.String(length=20),
                server_default="pending",
                nullable=False,
            ),
            sa.Column("requested_at", sa.DateTime(), nullable=False),
            sa.Column("updated_at", sa.DateTime(), nullable=False),
            sa.CheckConstraint(
                "mentor_id != mentee_id",
                name="check_different_mentor_and_mentee",
            ),
            sa.ForeignKeyConstraint(["mentor_id"], ["alumni.id"]),
            sa.ForeignKeyConstraint(["mentee_id"], ["alumni.id"]),
            sa.PrimaryKeyConstraint("id"),
        )

        op.create_index(
            "ix_mentorships_mentor_id",
            "mentorships",
            ["mentor_id"],
            unique=False,
        )
        op.create_index(
            "ix_mentorships_mentee_id",
            "mentorships",
            ["mentee_id"],
            unique=False,
        )


def downgrade():
    bind = op.get_bind()
    inspector = inspect(bind)

    if "mentorships" in inspector.get_table_names():
        op.drop_table("mentorships")
