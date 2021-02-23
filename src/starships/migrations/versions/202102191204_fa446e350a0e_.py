"""add `starships` table

Revision ID: fa446e350a0e
Revises: 
Create Date: 2021-02-21 12:04:38.429849

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "fa446e350a0e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "starships",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("hyperdrive_rating", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("name"),
    )


def downgrade():
    op.drop_table("starships")
