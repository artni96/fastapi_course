"""images model added

Revision ID: 06
Revises: 05
Create Date: 2024-11-10 11:46:05.792328

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "06"
down_revision: Union[str, None] = "05"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "imagesmodel",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.add_column("hotelsmodel", sa.Column("image", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "hotelsmodel", "imagesmodel", ["image"], ["id"])


def downgrade() -> None:
    op.drop_constraint(None, "hotelsmodel", type_="foreignkey")
    op.drop_column("hotelsmodel", "image")
    op.drop_table("imagesmodel")
