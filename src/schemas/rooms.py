from pydantic import BaseModel, Field, field_validator


class RoomCreateRequest(BaseModel):
    title: str = Field(
        description='Название'
    )
    description: str = Field(
        description='Описание номера'
    )
    price: int = Field(
        description='цена за сутки'
    )
    quantity: int = Field(
        description='Количество'
    )

    @field_validator('price')
    def validate_price(cls, value: int):
        if value < 0:
            raise ValueError(
                "Значение поля 'price' должно быть положительным!"
            )
        return value

    @field_validator('quantity')
    def validate_quantity(cls, value: int):
        if value < 0:
            raise ValueError(
                "Значение поля 'quantity' должно быть положительным!"
            )
        return value

    class Config:
        schema_extra = {
            'examples': {
                'Одноместный номер': {
                    'summary': 'Одноместный номер',
                    'value': {
                        'title': 'Одноместный номер',
                        'description': (
                            'Одноместный - cтандартный с широкой кроватью или '
                            'с двумя раздельными кроватями'
                        ),
                        'price': 3000,
                        'quantity': 10
                    }
                },
                'Двуместный номер': {
                    'summary': 'Двуместный номер',
                    'value': {
                        'title': 'Двуместный номер',
                        'description': (
                            'Двухместный - cтандартный с двумя кроватями'
                        ),
                        'price': 4500,
                        'quantity': 7
                    }
                },
                'Двуместный номер повышенной комфортности': {
                    'summary': 'Двуместный номер повышенной комфортности',
                    'value': {
                        'title': 'Двуместный номер повышенной комфортности',
                        'description': (
                            'Двухместный - повышенной комфортности c широкой '
                            'кроватью или с двумя раздельными кроватями'
                        ),
                        'price': 6000,
                        'quantity': 6
                    }
                },
                'Невалидный запрос': {
                    'summary': 'Невалидный запрос',
                    'value': {
                        'title': 'Одноместный номер',
                        'description': (
                            'Одноместный - cтандартный с широкой кроватью или '
                            'с двумя раздельными кроватями'
                        ),
                        'price': -10,
                        'quantity': -10
                    }
                },
            }
        }


class RoomCreate(RoomCreateRequest):
    hotel_id: int


class RoomInfo(RoomCreate):
    id: int
    hotel_id: int


class RoomPutRequest(RoomCreateRequest):

    class Config:
        schema_extra = {
            'examples': {
                'Изменение всех полей': {
                    'summary': 'Изменение всех полей',
                    'value': {
                        'title': 'Новое название номера',
                        'description': 'Новое описание номера',
                        'price': 2000,
                        'quantity': 7
                    }
                }
            }
        }


class RoomPut(RoomPutRequest):
    hotel_id: int


class RoomPatchRequest(BaseModel):
    title: str | None = Field(
        default=None,
        description='Название'
    )
    description: str | None = Field(
        default=None,
        description='Описание номера'
    )
    price: int | None = Field(
        default=None,
        description='цена за сутки'
    )
    quantity: int | None = Field(
        default=None,
        description='Количество'
    )

    class Config:
        schema_extra = {
            'examples': {
                'Изменение одного поля title': {
                    'summary': 'Изменение одного поля title',
                    'value': {
                        'title': 'Новое название номера'
                    }
                },
                'Изменение полей price и quantity': {
                    'summary': 'Изменение полей price и quantity',
                    'value': {
                        'price': 1000,
                        'quantity': 5
                    }
                },
                'Изменение полей title, description, price и quantity': {
                    'summary': ('Изменение полей title, description, '
                                'price и quantity'),
                    'value': {
                        'title': 'Новое название номера',
                        'description': 'Новое описание номера',
                        'price': 2000,
                        'quantity': 7
                    }
                }
            }
        }


class RoomPatch(RoomPatchRequest):
    hotel_id: int


class RoomTestResponse(BaseModel):
    hotel_id: int
    id: int
    title: str = Field(
        description='Название'
    )
    description: str = Field(
        description='Описание номера'
    )
    quantity: int
    booked_rooms: int
    avaliable_rooms: int = Field(
        description='Количество'
    )
    price: int = Field(
        description='цена за сутки'
    )
