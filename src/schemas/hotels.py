from pydantic import BaseModel, Field


class Hotel(BaseModel):
    title: str = Field(
        description='Название отеля'
    )
    location: str = Field(
        description='Место расположения'
    )

    class Config:
        title = 'Отели'
        schema_extra = {
            'examples': {
                'Izmailovo Moscow': {
                    'summary': 'Izmailovo Moscow',
                    'value': {
                        'title': 'Izmailovo Alpha Hotel',
                        'location': 'Izmailovskoye shosse, 71A, Moscow',
                    },
                },
                'Ararat Moscow': {
                    'summary': 'Ararat Moscow',
                    'value': {
                        'title': 'Ararat Park Hotel Moscow',
                        'location': 'Neglinnaya ul., 4, Moskva, Moscow'
                    },
                },
                'Stella di Mosca Moscow': {
                    'summary': 'Stella di Mosca Moscow',
                    'value': {
                        'title': 'Stella di Mosca By BVLGARI Hotels',
                        'location': (
                            'Moscow, Bolshaya Nikitskaya Street, 9, Moscow'
                        )
                    },
                }
            }
        }


class HotelPATCH(BaseModel):
    title: str | None = Field(
        default=None,
        description='Название отеля'
    )
    location: str | None = Field(
        default=None,
        description='Место расположения'
    )
