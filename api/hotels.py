from fastapi import Query, APIRouter
from api.schemas.schemas import Hotel, HotelPATCH


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
    id: int | None = Query(
        default=None,
        description='индентификатор'
    ),
    name: str | None = Query(
        default=None,
        description='Оригинальное название отеля',
    ),
    title: str | None = Query(
        default=None,
        description='Название отеля'
    ),
    page: int = 1,
    per_page: int = 3
):
    end_point = page * per_page
    start_point = end_point - per_page
    if end_point > len(hotels):
        end_point = len(hotels)
    hotels_list_response = list()
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if name and hotel['name'] != name:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_list_response.append(hotel)
    return hotels_list_response[start_point: end_point]


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
    hotel: Hotel,
):
    if hotel.title is None:
        hotel.title = 'Не указан'
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'name': hotel.name,
        'title': hotel.title
    })
    return hotels[-1]


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
