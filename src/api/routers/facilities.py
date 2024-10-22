from fastapi import APIRouter, Query
from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityBaseRequest, FacilityResponse


facilities_router = APIRouter(
    prefix='/facilities',
    tags=['Удобства']
)


@facilities_router.get(
    '/',
    summary='Получение списка доступных удобств'
)
async def get_all_facilities(
    db: DBDep,
    title: str | None = Query(default=None, max_length=64)
) -> list[FacilityResponse]:
    result = await db.facilities.get_filtered(
        title=title
    )
    return result


@facilities_router.get(
    '/{facility_id}',
    summary='Получение удобства по "facility_id"'
)
async def get_facility_by_id(
    facility_id: int,
    db: DBDep,
) -> FacilityResponse:
    result = await db.facilities.get_one_or_none(
        id=facility_id
    )
    return result

@facilities_router.post(
    '/',
    summary='Создание нового удобства'
)
async def create_facility(
    db: DBDep,
    facility_data: FacilityBaseRequest
) -> FacilityResponse:
    new_facility = await db.facilities.add(facility_data)
    await db.commit()
    return new_facility


@facilities_router.put(
    '/{facility_id}',
    summary='Обновление данных удобства по "facility_id"')
async def update_facility(
    facility_id: int,
    db: DBDep,
    facility_data: FacilityBaseRequest
) -> FacilityResponse:
    updated_facility = await db.facilities.change(
        id=facility_id,
        data=facility_data
    )
    await db.commit()
    return updated_facility


@facilities_router.delete(
    '/{facility_id}',
    summary='Удаление удобства по "facility_id"')
async def delete_facility(
    facility_id: int,
    db: DBDep
) -> dict:
    result = await db.facilities.remove(id=facility_id)
    await db.commit()
    return result
