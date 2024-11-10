"""ondelete cascade for image field of hotel model

Revision ID: 07
Revises: 06
Create Date: 2024-11-10 17:33:44.025596

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "07"
down_revision: Union[str, None] = "06"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "hotelsmodel_image_fkey", "hotelsmodel", type_="foreignkey"
    )
    op.create_foreign_key(
        None,
        "hotelsmodel",
        "imagesmodel",
        ["image"],
        ["id"],
        ondelete="cascade",
    )


def downgrade() -> None:
    op.drop_constraint(None, "hotelsmodel", type_="foreignkey")
    op.create_foreign_key(
        "hotelsmodel_image_fkey",
        "hotelsmodel",
        "imagesmodel",
        ["image"],
        ["id"],
    )
