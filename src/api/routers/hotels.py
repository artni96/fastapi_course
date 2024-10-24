from datetime import date, datetime

from fastapi import APIRouter, Body, Query, HTTPException

from src.api.dependencies import DBDep, PaginationDep
from src.schemas.hotels import HotelResponse, HotelAddPut, HotelPatch

hotels_router = APIRouter(prefix='/hotels', tags=['Отели',])


@hotels_router.get(
    '/',
    summary='Получение отелей с свободными номерами в указанный период'
)
async def get_hotels(
    db: DBDep,
    pagination: PaginationDep,
    date_from: date | str = Query(example='18.10.2024'),
    date_to: date | str = Query(example='21.10.2024'),
    title: str | None = Query(
        default=None,
        description='Название отеля'
    ),
    location: str | None = Query(
        default=None,
        description='Расположение'
    ),
) -> list[HotelResponse] | str | None:
    try:
        date_to = datetime.strptime(date_to, '%d.%m.%Y').date()
        date_from = datetime.strptime(date_from, '%d.%m.%Y').date()
    except ValueError:
        return 'Укажите даты в формате dd.mm.yyyy'
    per_page = pagination.per_page or 3
    result = await db.hotels.get_filtered_hotels(
        date_to=date_to,
        date_from=date_from,
        title=title,
        location=location,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )
    return result


@hotels_router.get(
    '/{hotel_id}',
    summary='Получение информации об отеле по "hotel_id"'
)
async def get_hotel(
    hotel_id: int,
    db: DBDep
):
    return await db.hotels.get_one_or_none(id=hotel_id)


@hotels_router.delete(
    '/{hotel_id}',
    summary='Удаление отеля по "hotel_id"'
)
async def delete_hotel(
    hotel_id: int,
    db: DBDep
) -> dict:
    result = await db.hotels.remove(id=hotel_id)
    await db.commit()
    return result


@hotels_router.post(
    '/',
    summary='Создание нового отеля'
)
async def post_hotel(
    *,
    hotel_data: HotelAddPut = Body(
        openapi_examples=HotelResponse.Config.schema_extra['examples'],
    ),
    db: DBDep
):
    new_hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {'status': 'OK', 'data': new_hotel}


@hotels_router.put(
    '/{hotel_id}',
    summary='Полное обновление информации об отеле "hotel_id"'
)
async def update_hotel(
    hotel_id: int,
    hotel_data: HotelAddPut,
    db: DBDep
) -> HotelResponse:
    result = await db.hotels.change(id=hotel_id, data=hotel_data)
    await db.commit()
    return result


@hotels_router.patch(
    '/{hotel_id}',
    summary='Частичное обновление информации об отеле "hotel_id"'
)
async def update_hotel_partially(
    hotel_id: int,
    hotel_data: HotelPatch,
    db: DBDep
) -> HotelResponse:
    result = await db.hotels.change(
        id=hotel_id,
        exclude_unset=True,
        data=hotel_data
    )
    await db.commit()
    return result
