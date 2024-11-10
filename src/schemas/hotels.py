from pydantic import BaseModel, ConfigDict, Field


class HotelBase(BaseModel):
    title: str = Field(
        description='Название отеля'
    )
    location: str = Field(
        description='Место расположения'
    )

    class Config:
        orm_mode = True
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


class HotelAddRequest(HotelBase):
    image: str = None


class HotelPutRequest(HotelBase):
    image: str


class HotelAddPut(BaseModel):
    title: str = Field(
        description='Название отеля'
    )
    location: str = Field(
        description='Место расположения'
    )
    image: str = None


class HotelResponse(HotelBase):
    id: int
    image: int | None = None


class HotelPatch(BaseModel):
    title: str | None = Field(
        default=None,
        description='Название отеля'
    )
    location: str | None = Field(
        default=None,
        description='Место расположения'
    )
    image: str | None = None
