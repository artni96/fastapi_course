from fastapi import HTTPException

from src.api.dependencies import DBDep


async def check_facilities_existence(facility_ids: set[int], db: DBDep):
    result = await db.facilities.get_by_ids(ids=facility_ids)
    if len(facility_ids) != len(result):
        accessible_facilities = await db.facilities.get_all()
        raise HTTPException(
            status_code=404,
            detail=(
                'Удобства с указанными id не найдены. '
                f'Доступные удобства: {"; ".join(accessible_facilities)}'
            ),
        )
