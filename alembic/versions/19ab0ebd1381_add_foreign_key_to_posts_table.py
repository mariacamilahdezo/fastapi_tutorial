"""add foreign-key to posts table

Revision ID: 19ab0ebd1381
Revises: a7b06d3cb249
Create Date: 2022-02-07 14:33:28.364642

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "19ab0ebd1381"
down_revision = "a7b06d3cb249"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade():
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
