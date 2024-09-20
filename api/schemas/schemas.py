from pydantic import BaseModel, Field


class Hotel(BaseModel):
    name: str = Field(
        ...,
        description='Оригинальное название отеля',
    ),
    title: str = Field(
        ...,
        description='Название отеля'
    )


class HotelPATCH(BaseModel):
    name: str | None = Field(
        default=None,
        description='Оригинальное название отеля',
    ),
    title: str | None = Field(
        default=None,
        description='Название отеля'
    )
