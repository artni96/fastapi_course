from fastapi import APIRouter, Query, status, HTTPException
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.exceptions import FacilityNotFoundException
from src.schemas.facilities import FacilityBaseRequest, FacilityResponse
from src.services.facility import FacilityService

facilities_router = APIRouter(prefix="/facilities", tags=["Удобства"])


@facilities_router.get("", summary="Получение списка доступных удобств")
@cache(expire=5)
async def get_all_facilities(
    db: DBDep, title: str | None = Query(default=None, max_length=64)
) -> list[FacilityResponse]:
    return await db.facilities.get_filtered(title=title)


@facilities_router.get("/{facility_id}", summary='Получение удобства по "facility_id"')
async def get_facility_by_id(
    facility_id: int,
    db: DBDep,
) -> FacilityResponse:
    try:
        return await FacilityService(db).get_facility_by_id(facility_id=facility_id)
    except FacilityNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.detail)


@facilities_router.post(
    "", status_code=status.HTTP_201_CREATED, summary="Создание нового удобства"
)
async def create_facility(
    db: DBDep, facility_data: FacilityBaseRequest
) -> FacilityResponse:
    new_facility = await db.facilities.add(facility_data)
    await db.commit()
    return new_facility


@facilities_router.put(
    "/{facility_id}", summary='Обновление данных удобства по "facility_id"'
)
async def update_facility(
    facility_id: int, db: DBDep, facility_data: FacilityBaseRequest
) -> FacilityResponse:
    updated_facility = await db.facilities.change(id=facility_id, data=facility_data)
    await db.commit()
    return updated_facility


@facilities_router.delete(
    "/{facility_id}", summary='Удаление удобства по "facility_id"'
)
async def delete_facility(facility_id: int, db: DBDep) -> dict:
    result = await db.facilities.remove(id=facility_id)
    await db.commit()
    return result
