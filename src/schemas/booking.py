from datetime import date, datetime, timedelta

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_serializer
)

from src.constants import DATETIME_FORMAT


class BookingCreateRequest(BaseModel):
    date_from: date = Field(default=(date.today() + timedelta(days=1)))
    date_to: date = Field(default=(date.today() + timedelta(days=2)))
    room_id: int

    model_config = {
        "json_schema_extra": {
            "Создание новой брони": {
                "summary": "Создание новой брони",
                "value": {
                    "date_from": f"{date.today() + timedelta(days=1)}",
                    "date_to": f"{date.today() + timedelta(days=2)}",
                    "room_id": 1,
                },
            }
        }
    }


class BookingCreate(BaseModel):
    price: int
    user_id: int
    date_to: date
    date_from: date
    room_id: int


class BookingUpdateRequest(BaseModel):
    date_from: date = Field(default=(date.today() + timedelta(days=1)))
    date_to: date = Field(default=(date.today() + timedelta(days=2)))
    room_id: int | None = Field(1)

    model_config = ConfigDict(from_attributes=True)


class BookingUpdate(BaseModel):
    date_from: date | None = Field(default=date.today)
    date_to: date | None = Field(default=(date.today() + timedelta(days=1)))
    room_id: int | None = None
    price: int


class BookingResponse(BaseModel):
    id: int
    date_from: date
    date_to: date
    room_id: int
    user_id: int
    price: int
    total_cost: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("created_at")
    def serialize_created_at(self, created_at: datetime):
        return created_at.strftime(DATETIME_FORMAT)

    @field_serializer("updated_at")
    def serialize_updated_at(self, created_at: datetime):
        if created_at:
            return created_at.strftime(DATETIME_FORMAT)
        return None
