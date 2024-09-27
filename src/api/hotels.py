from fastapi import Body, Query, APIRouter
from src.schemas.hotels import Hotel, HotelPatch, HotelAddPut
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


@hotels_router.get('/{hotel_id}')
async def get_hotel(
    hotel_id: int
):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).get_one_or_none(
            id=hotel_id
        )
        return result


@hotels_router.delete('/{hotel_id}')
async def delete_hotel(
    hotel_id: int,
):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).remove(
            id=hotel_id
        )
        if result['status'] == 'OK':
            await session.commit()
        return result


@hotels_router.post('/')
async def post_hotel(
    hotel_data: HotelAddPut = Body(
        openapi_examples=Hotel.Config.schema_extra['examples']
    ),
):
    async with async_session_maker() as session:
        new_hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {'status': 'OK', 'data': new_hotel}


@hotels_router.put('/{hotel_id}')
async def update_hotel(
    hotel_id: int,
    hotel_data: HotelAddPut
):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).change(
            id=hotel_id,
            data=hotel_data
        )
        if result['status'] == 'OK':
            await session.commit()
        return result


@hotels_router.patch('/{hotel_id}')
async def update_hotel_partially(
    hotel_id: int,
    hotel_data: HotelPatch
):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).change(
            id=hotel_id,
            exclude_unset=True,
            data=hotel_data
        )
        if result['status'] == 'OK':
            await session.commit()
        return result
