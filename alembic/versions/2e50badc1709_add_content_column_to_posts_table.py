"""add content column to posts table

Revision ID: 2e50badc1709
Revises: 75dae89ffca0
Create Date: 2022-02-07 12:46:23.875994

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2e50badc1709"
down_revision = "75dae89ffca0"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
