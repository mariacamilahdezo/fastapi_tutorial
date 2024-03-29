"""add last few columns to posts table

Revision ID: df36f93f6045
Revises: 19ab0ebd1381
Create Date: 2022-02-07 14:39:13.364976

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "df36f93f6045"
down_revision = "19ab0ebd1381"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )
    pass


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
