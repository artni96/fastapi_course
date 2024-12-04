"""ondelete cascade for roomfaciliries model added

Revision ID: 09
Revises: 08
Create Date: 2024-12-04 23:24:01.406702

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "09"
down_revision: Union[str, None] = "08"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "roomfacilitiesmodel_facility_id_fkey",
        "roomfacilitiesmodel",
        type_="foreignkey",
    )
    op.drop_constraint(
        "roomfacilitiesmodel_room_id_fkey",
        "roomfacilitiesmodel",
        type_="foreignkey",
    )
    op.create_foreign_key(
        None,
        "roomfacilitiesmodel",
        "facilitiesmolel",
        ["facility_id"],
        ["id"],
        ondelete="cascade",
    )
    op.create_foreign_key(
        None,
        "roomfacilitiesmodel",
        "roomsmodel",
        ["room_id"],
        ["id"],
        ondelete="cascade",
    )


def downgrade() -> None:
    op.drop_constraint(None, "roomfacilitiesmodel", type_="foreignkey")
    op.drop_constraint(None, "roomfacilitiesmodel", type_="foreignkey")
    op.create_foreign_key(
        "roomfacilitiesmodel_room_id_fkey",
        "roomfacilitiesmodel",
        "roomsmodel",
        ["room_id"],
        ["id"],
    )
    op.create_foreign_key(
        "roomfacilitiesmodel_facility_id_fkey",
        "roomfacilitiesmodel",
        "facilitiesmolel",
        ["facility_id"],
        ["id"],
    )
