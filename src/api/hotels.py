from fastapi import Body, Query, APIRouter
from models.hotels import HotelsModel
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.db import async_session_maker
from sqlalchemy import insert, select
from src.db import engine


hotels_router = APIRouter(prefix='/hotels')


hotels = [
    {
        'id': 1,
        'name': 'The Carlton Moscow',
        'title': 'Ритц-Карлтон Москва',

    },
    {
        'id': 2,
        'name': 'Four Seasons Hotel Moscow',
        'title': 'Четыре Сезона Москва',
    },
    {
        'id': 3,
        'name': 'Hotel National',
        'title': 'Отель "Националь"',
    },
    {
        'id': 4,
        'name': 'Lotte Hotel Moscow',
        'title': 'ЛОТТЕ Отель Москва',
    },
    {
        'id': 5,
        'name': 'Radisson Royal Hotel',
        'title': 'Рэдиссон Ройал Hotel Москва',
    },
    {
        'id': 6,
        'name': 'Helvetia Hotel',
        'title': 'Отель "Гельвеция" Санкт-Петербург',
    },
    {
        'id': 7,
        'name': 'Pushka Inn Hotel',
        'title': 'Пушка ИНН Отель',
    },
    {
        'id': 8,
        'name': 'Kino Hostel on Vyborgskaya',
        'title': 'Кино Хостел на Выборгской',
    },
]


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
    per_page = pagination.per_page or 5
    limit = per_page
    offset = (pagination.page - 1) * limit
    async with async_session_maker() as session:
        query = select(HotelsModel)
        if title:
            query = query.filter(HotelsModel.title.icontains(title))
        if location:
            query = query.filter(HotelsModel.location.icontains(location))
        query = (
            query
            .offset(offset)
            .limit(limit)
        )
        result = await session.execute(query)
        return result.scalars().all()


@hotels_router.delete('/{hotel_id}')
async def delete_hotels(hotel_id: int):
    try:
        for hotel in hotels:
            if hotel['id'] == hotel_id:
                hotels.remove(hotel)
                return f'Отель с id {hotel_id} успешно удален.'
    except IndexError:
        return f'Отель с id {hotel_id} не найден.'


@hotels_router.post('/')
async def post_hotel(
    hotel: Hotel = Body(
        openapi_examples=Hotel.Config.schema_extra['examples']
    ),
):
    async with async_session_maker() as session:
        new_hotel_stmt = insert(HotelsModel).values(**hotel.model_dump())
        print(new_hotel_stmt.compile(
            engine,
            compile_kwargs={"literal_binds": True})
        )
        await session.execute(new_hotel_stmt)
        await session.commit()
    return f'{hotel.title} успешно добавлен.'


@hotels_router.put('/{hotel_id}')
async def update_hotel(
    hotel_id: int,
    hotel_data: Hotel
):
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['name'] = hotel_data.name
            hotel['title'] = hotel_data.title
            return hotel
    return {'status': 'NOT FOUND'}


@hotels_router.patch('/{hotel_id}')
async def update_hote(
    hotel_id: int,
    hotel_data: HotelPATCH
):
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if hotel_data.name is not None:
                hotel['name'] = hotel_data.name
            if hotel_data.title is not None:
                hotel['title'] = hotel_data.title
            return hotel
    return {'status': 'NOT FOUND'}
