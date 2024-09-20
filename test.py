from pprint import pprint

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


def test_func(hotels, page: int = 1, per_page: int = 3):
    end_point = page * per_page
    start_point = end_point - per_page
    if end_point > len(hotels):
        end_point = len(hotels)
    return hotels[start_point: end_point]


pprint(test_func(hotels=hotels, page=3, per_page=5))
