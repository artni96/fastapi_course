from pydantic import BaseModel, Field


class RoomBase(BaseModel):
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
                }
            }
        }


class RoomInfo(RoomBase):
    id: int
    hotel_id: int


class RoomPatch(BaseModel):
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
