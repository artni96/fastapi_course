"""m2m facilities for rooms

Revision ID: 05
Revises: 04
Create Date: 2024-10-22 10:25:48.744556

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "05"
down_revision: Union[str, None] = "04"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "facilitiesmolel",
        sa.Column("title", sa.String(length=64), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "roomfacilitiesmodel",
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("facility_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["facility_id"],
            ["facilitiesmolel.id"],
        ),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["roomsmodel.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("roomfacilitiesmodel")
    op.drop_table("facilitiesmolel")
