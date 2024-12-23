from datetime import date, timedelta

from fastapi import APIRouter, Body, Query, status, HTTPException

from src.api.dependencies import DBDep, PaginationDep
from src.exceptions import DateToLaterThanDateFromException, HotelNotFoundException
from src.schemas.hotels import (
    HotelAddRequest,
    HotelPatch,
    HotelPutRequest,
    HotelResponse,
)
from src.services.hotels import HotelService

hotels_router = APIRouter(
    prefix="/hotels",
    tags=[
        "Отели",
    ],
)


@hotels_router.get(
    "", summary="Получение отелей с свободными номерами в указанный период"
)
async def get_hotels(
    db: DBDep,
    pagination: PaginationDep,
    date_from: date = Query(
        default=f"{date.today() + timedelta(days=1)}",
    ),
    date_to: date = Query(
        default=f"{date.today() + timedelta(days=2)}",
    ),
    title: str | None = Query(default=None, description="Название отеля"),
    location: str | None = Query(default=None, description="Расположение"),
):
    try:
        result = await HotelService(db).get_hotels(
            pagination=pagination,
            date_from=date_from,
            date_to=date_to,
            title=title,
            location=location
        )
    except DateToLaterThanDateFromException as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.detail)
    return result


@hotels_router.get("/{hotel_id}", summary='Получение информации об отеле по "hotel_id"')
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id=hotel_id)
    except HotelNotFoundException as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.detail(hotel_id))


@hotels_router.delete(
    "/{hotel_id}",
    summary='Удаление отеля по "hotel_id"',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_hotel(hotel_id: int, db: DBDep):
    return await HotelService(db).delete_hotel(hotel_id=hotel_id)


@hotels_router.post(
    "", summary="Создание нового отеля", status_code=status.HTTP_201_CREATED
)
async def post_hotel(
    *,
    hotel_data: HotelAddRequest = Body(
        openapi_examples=HotelResponse.model_config["json_schema_extra"],
    ),
    db: DBDep,
):
    new_hotel = await HotelService(db).post_hotel(hotel_data=hotel_data)

    return {"status": "OK", "data": new_hotel}


@hotels_router.put(
    "/{hotel_id}", summary='Полное обновление информации об отеле "hotel_id"'
)
async def update_hotel(
    hotel_id: int, hotel_data: HotelPutRequest, db: DBDep
) -> HotelResponse:
    return await HotelService(db).update_hotel(hotel_id=hotel_id, hotel_data=hotel_data)


@hotels_router.patch(
    "/{hotel_id}", summary='Частичное обновление информации об отеле "hotel_id"'
)
async def update_hotel_partially(
    hotel_id: int, hotel_data: HotelPatch, db: DBDep
) -> HotelResponse:
    return await HotelService(db).update_hotel_partially(hotel_id=hotel_id, hotel_data=hotel_data)
