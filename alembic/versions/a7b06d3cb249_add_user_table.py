"""add user table

Revision ID: a7b06d3cb249
Revises: 2e50badc1709
Create Date: 2022-02-07 13:07:39.643097

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a7b06d3cb249"
down_revision = "2e50badc1709"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    pass


def downgrade():
    op.drop_table("users")
    pass
