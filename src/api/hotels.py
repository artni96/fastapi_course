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


# @hotels_router.put('/{hotel_id}')
# async def update_hotel(
#     hotel_id: int,
#     hotel_data: Hotel
# ):
#     for hotel in hotels:
#         if hotel['id'] == hotel_id:
#             hotel['name'] = hotel_data.name
#             hotel['title'] = hotel_data.title
#             return hotel
#     return {'status': 'NOT FOUND'}


# @hotels_router.patch('/{hotel_id}')
# async def update_hote(
#     hotel_id: int,
#     hotel_data: HotelPATCH
# ):
#     for hotel in hotels:
#         if hotel['id'] == hotel_id:
#             if hotel_data.name is not None:
#                 hotel['name'] = hotel_data.name
#             if hotel_data.title is not None:
#                 hotel['title'] = hotel_data.title
#             return hotel
#     return {'status': 'NOT FOUND'}
