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
