from fastapi import Body, Query, APIRouter
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.db import async_session_maker

from src.repositories.hotels import HotelsRepository


hotels_router = APIRouter(prefix='/hotels')


@hotels_router.get('/')
async def get_hotels(
    *,
    title: str | None = Query(
        default=None,
        description='Название отеля'
    ),
    location: str | None = Query(
        default=None,
        description='Расположение'
    ),
    pagination: PaginationDep
):
    per_page = pagination.per_page or 3
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            limit=per_page,
            offset=per_page * (pagination.page - 1),
            title=title,
            location=location
        )


@hotels_router.delete('/')
async def delete_hotels(
    hotel_id: int = None,
    title: str = None,
    location: str = None
):
    async with async_session_maker() as session:
        obj_to_del = await HotelsRepository(session).remove(
            id=hotel_id, title=title, location=location
        )
        await session.commit()
        return obj_to_del


@hotels_router.post('/')
async def post_hotel(
    hotel: Hotel = Body(
        openapi_examples=Hotel.Config.schema_extra['examples']
    ),
):
    async with async_session_maker() as session:
        new_hotel = await HotelsRepository(session).add(hotel)
        await session.commit()

    return {'status': 'OK', 'data': {new_hotel}}


@hotels_router.put('/')
async def update_hotel(
    *,
    hotel_id: int = None,
    hotel_title: str = None,
    hotel_location: str = None,
    hotel_data: Hotel
):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).change(
            id=hotel_id,
            hotel_title=hotel_title,
            hotel_location=hotel_location,
            data=hotel_data
        )
        if result['status'] == 'OK':
            await session.commit()
        return result


@hotels_router.patch('/')
async def update_hotel_partially(
    *,
    hotel_id: int = None,
    hotel_title: str = None,
    hotel_location: str = None,
    hotel_data: HotelPATCH
):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).change(
            hotel_id=hotel_id,
            hotel_title=hotel_title,
            hotel_location=hotel_location,
            data=hotel_data
        )
        if result['status'] == 'OK':
            await session.commit()
        return result
