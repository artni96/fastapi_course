"""updated_at field added to Booking model

Revision ID: 04
Revises: 03
Create Date: 2024-10-16 17:46:26.699281

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "04"
down_revision: Union[str, None] = "03"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "bookingmodel", sa.Column("updated_at", sa.DateTime(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("bookingmodel", "updated_at")
