from typing import Optional, Union

import uvicorn
from fastapi import FastAPI, Query, Body
from fastapi.openapi.docs import (get_redoc_html, get_swagger_ui_html,
                                  get_swagger_ui_oauth2_redirect_html)

app = FastAPI(docs_url=None, redoc_url=None)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="https://unpkg.com/redoc@next/bundles/redoc.standalone.js",
    )

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


@app.get('/hotels')
async def get_hotels(
    id: Optional[Union[int, None]] = Query(
        default=None,
        description='индентификатор'
    ),
    name: Optional[Union[str, None]] = Query(
        default=None,
        description='Оригинальное название отеля',
    ),
    title: Optional[Union[str, None]] = Query(
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


@app.delete('/hotels/{hotel_id}/')
async def delete_hotels(hotel_id: int):
    del hotels[hotel_id]
    return hotels


@app.post('/hotels')
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


@app.put('/hotels/{hotel_id}')
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


@app.patch('/hotels/{hotel_id}')
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


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
