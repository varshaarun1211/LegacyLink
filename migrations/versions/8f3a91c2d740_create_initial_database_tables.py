
"""Create the initial LegacyLink database tables."""

from alembic import op
import sqlalchemy as sa

revision = "8f3a91c2d740"
down_revision = "26221d59437c"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = inspector.get_table_names()

    if "users" not in existing_tables:
        op.create_table(
            "users",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("email", sa.String(255), nullable=False, unique=True),
            sa.Column("password_hash", sa.String(256), nullable=False),
            sa.Column("role", sa.String(20), nullable=False, server_default="alumni"),
            sa.Column("email_verified", sa.Boolean(), nullable=False, server_default=sa.false()),
            sa.Column("created_at", sa.DateTime(), nullable=True),
        )

    inspector = sa.inspect(bind)
    existing_tables = inspector.get_table_names()

    if "alumni" not in existing_tables:
        op.create_table(
            "alumni",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True, unique=True),
            sa.Column("full_name", sa.String(150), nullable=False),
            sa.Column("department", sa.String(120), nullable=False),
            sa.Column("degree", sa.String(120), nullable=False),
            sa.Column("graduation_year", sa.Integer(), nullable=False),
            sa.Column("occupation", sa.String(150), nullable=True),
            sa.Column("company", sa.String(150), nullable=True),
            sa.Column("skills", sa.Text(), nullable=True),
            sa.Column("bio", sa.Text(), nullable=True),
            sa.Column("verification_status", sa.String(20), nullable=False, server_default="pending"),
            sa.Column("verified_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
            sa.Column("verified_at", sa.DateTime(), nullable=True),
            sa.Column("is_visible", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column("is_public", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
        )

    inspector = sa.inspect(bind)
    alumni_columns = {column["name"] for column in inspector.get_columns("alumni")}

    if "department" in alumni_columns:
        existing_indexes = {index["name"] for index in inspector.get_indexes("alumni")}
        if "ix_alumni_department" not in existing_indexes:
            op.create_index("ix_alumni_department", "alumni", ["department"])

    if "graduation_year" in alumni_columns:
        existing_indexes = {index["name"] for index in inspector.get_indexes("alumni")}
        if "ix_alumni_graduation_year" not in existing_indexes:
            op.create_index("ix_alumni_graduation_year", "alumni", ["graduation_year"])


def downgrade():
    op.drop_table("alumni")
    op.drop_table("users")
