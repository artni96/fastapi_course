"""created_at field added to Booking model

Revision ID: 03
Revises: 02
Create Date: 2024-10-16 17:42:20.036263

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "03"
down_revision: Union[str, None] = "02"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "bookingmodel", sa.Column("created_at", sa.DateTime(), nullable=False)
    )


def downgrade() -> None:
    op.drop_column("bookingmodel", "created_at")
