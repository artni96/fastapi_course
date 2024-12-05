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
    return await FacilityService(db).get_all_facilities(title=title)


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
    return await FacilityService(db).create_facility(facility_data)

@facilities_router.put(
    "/{facility_id}", summary='Обновление данных удобства по "facility_id"'
)
async def update_facility(
    facility_id: int, db: DBDep, facility_data: FacilityBaseRequest
) -> FacilityResponse:
    try:
        return await FacilityService(db).update_facility(facility_id, facility_data)
    except FacilityNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.detail)


@facilities_router.delete(
    "/{facility_id}", summary='Удаление удобства по "facility_id"'
)
async def delete_facility(facility_id: int, db: DBDep) -> dict:
    try:
        return await FacilityService(db).delete_facility(facility_id)
    except FacilityNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.detail)
