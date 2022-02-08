"""create posts table

Revision ID: 75dae89ffca0
Revises: 
Create Date: 2022-02-07 12:34:35.130378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "75dae89ffca0"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )
    pass


def downgrade():
    op.drop_table("posts")
    pass
