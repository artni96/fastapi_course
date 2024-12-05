"""custom auth manager

Revision ID: 10
Revises: 09
Create Date: 2024-12-05 20:42:23.850108

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "10"
down_revision: Union[str, None] = "09"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "user",
        "email",
        existing_type=sa.VARCHAR(length=320),
        type_=sa.String(length=100),
        existing_nullable=False,
    )
    op.drop_index("ix_user_email", table_name="user")
    op.create_unique_constraint(None, "user", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "user", type_="unique")
    op.create_index("ix_user_email", "user", ["email"], unique=True)
    op.alter_column(
        "user",
        "email",
        existing_type=sa.String(length=100),
        type_=sa.VARCHAR(length=320),
        existing_nullable=False,
    )
