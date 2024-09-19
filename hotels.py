from fastapi import Body, Query, APIRouter

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
    )
):
    hotels_list_response = list()
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if name and hotel['name'] != name:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_list_response.append(hotel)
    return hotels_list_response


@hotels_router.delete('/{hotel_id}')
async def delete_hotels(hotel_id: int):
    try:
        for hotel in hotels:
            if hotel['id'] == hotel_id:
                hotels.remove(hotel)
                return hotels
    except IndexError:
        return f'Отель с id {hotel_id} не найден.'


@hotels_router.post('/')
async def post_hotel(
    hotel_name: str = Body(embed=True),
    hotel_title: None | str = Body(default=None, embed=True)
):
    if not hotel_title:
        hotel_title = 'Не указан'
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'name': hotel_name,
        'city': hotel_title
    })
    return hotels


@hotels_router.put('/{hotel_id}')
async def update_hotel(
    hotel_id: int,
    hotel_name: str = Body(
        description='Оригинальное название отеля',
        embed=True
    ),
    hotel_title: str = Body(
        description='Название отеля',
        embed=True
    )
):
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['name'] = hotel_name
            hotel['title'] = hotel_title
    return {'status': 'OK'}


@hotels_router.patch('/{hotel_id}')
async def update_hote(
    hotel_id: int,
    hotel_name: str | None = Body(
        default=None,
        description='Оригинальное название отеля',
        embed=True
    ),
    hotel_title: str | None = Body(
        default=None,
        description='Название отеля',
        embed=True
    )
):
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if hotel_name:
                hotel['name'] = hotel_name
            if hotel_title:
                hotel['title'] = hotel_title
            return hotel
