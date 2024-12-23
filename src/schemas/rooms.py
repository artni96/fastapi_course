from pydantic import BaseModel, ConfigDict, Field, field_validator
from src.schemas.facilities import FacilityResponse


class RoomCreateRequest(BaseModel):
    title: str = Field(description="Название")
    description: str | None = Field(default=None, description="Описание номера")
    price: int = Field(description="цена за сутки")
    quantity: int = Field(description="Количество")
    facility_ids: list[int] = []

    @field_validator("price")
    def validate_price(cls, value: int):
        if value < 0:
            raise ValueError("Значение поля 'price' должно быть положительным!")
        return value

    @field_validator("quantity")
    def validate_quantity(cls, value: int):
        if value < 0:
            raise ValueError("Значение поля 'quantity' должно быть положительным!")
        return value

    model_config = {
        "json_schema_extra": {
            "Одноместный номер": {
                "summary": "Одноместный номер",
                "value": {
                    "title": "Одноместный номер",
                    "description": (
                        "Одноместный - cтандартный с широкой кроватью или "
                        "с двумя раздельными кроватями"
                    ),
                    "price": 3000,
                    "quantity": 10,
                    "facility_ids": [1, 2],
                },
            },
            "Двуместный номер": {
                "summary": "Двуместный номер",
                "value": {
                    "title": "Двуместный номер",
                    "description": ("Двухместный - cтандартный с двумя кроватями"),
                    "price": 4500,
                    "quantity": 7,
                    "facility_ids": [
                        2,
                    ],
                },
            },
            "Двуместный номер повышенной комфортности": {
                "summary": "Двуместный номер повышенной комфортности",
                "value": {
                    "title": "Двуместный номер повышенной комфортности",
                    "description": (
                        "Двухместный - повышенной комфортности c широкой "
                        "кроватью или с двумя раздельными кроватями"
                    ),
                    "price": 6000,
                    "quantity": 6,
                },
            },
            "Невалидный запрос": {
                "summary": "Невалидный запрос",
                "value": {
                    "title": "Одноместный номер",
                    "description": (
                        "Одноместный - cтандартный с широкой кроватью или "
                        "с двумя раздельными кроватями"
                    ),
                    "price": -10,
                    "quantity": -10,
                },
            },
        }
    }


class RoomCreate(BaseModel):
    hotel_id: int = Field(description="id отеля")
    title: str = Field(description="Название")
    description: str | None = Field(default=None, description="Описание номера")
    price: int = Field(description="цена за сутки")
    quantity: int = Field(description="Количество")

    model_config = ConfigDict(from_attributes=True)


class RoomInfo(RoomCreate):
    id: int


class RoomWithFacilitiesResponse(RoomInfo):
    facilities: list[FacilityResponse] = []


class RoomPutRequest(RoomCreateRequest):
    model_config = {
        "json_schema_extra": {
            "Изменение всех полей": {
                "summary": "Изменение всех полей",
                "value": {
                    "title": "Новое название номера",
                    "description": "Новое описание номера",
                    "price": 2000,
                    "quantity": 7,
                    "facility_ids": [1, 2],
                },
            }
        }
    }


class RoomPut(RoomCreate):
    pass


class RoomPatchRequest(BaseModel):
    title: str | None = Field(default=None, description="Название")
    description: str | None = Field(default=None, description="Описание номера")
    price: int | None = Field(default=None, description="цена за сутки")
    quantity: int | None = Field(default=None, description="Количество")
    facility_ids: list[int] | None = Field(
        default=None, description="Список id удобств номера"
    )

    model_config = {
        "json_schema_extra": {
            "Изменение одного поля title": {
                "summary": "Изменение одного поля title",
                "value": {
                    "title": "Новое название номера",
                },
            },
            "Изменение полей price и quantity": {
                "summary": "Изменение полей price и quantity",
                "value": {"price": 1000, "quantity": 5},
            },
            "Изменение полей title, description, price, quantity и " "facility_ids": {
                "summary": (
                    "Изменение полей title, description, "
                    "price, quantity и facility_ids"
                ),
                "value": {
                    "title": "Новое название номера",
                    "description": "Новое описание номера",
                    "price": 2000,
                    "quantity": 7,
                    "facility_ids": [1, 2],
                },
            },
        }
    }


class RoomPatch(RoomPatchRequest):
    hotel_id: int


class RoomExtendedResponse(RoomWithFacilitiesResponse):
    booked_rooms: int | None = None
    avaliable_rooms: int | None = None

    model_config = ConfigDict(from_attributes=True)
    facilities: list[FacilityResponse] = []
