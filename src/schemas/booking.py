from pydantic import BaseModel, ConfigDict, field_validator, model_validator, Field
from datetime import date, timedelta


class BookingCreateRequest(BaseModel):
    date_from: date = Field(default=date.today)
    date_to: date = Field(default=(date.today() + timedelta(days=1)))
    room_id: int

    @field_validator('date_from')
    def check_date_from_later_than_now(cls, value):
        if value < date.today():
            raise ValueError(
                'Дата бронирования не может быть раньше текущего времени'
            )
        return value

    @model_validator(mode='before')
    def check_date_to_later_than_date_from(cls, values):
        if values['date_to'] <= values['date_from']:
            raise ValueError(
                'Время начала бронирвоания не может быть '
                'раньше времени конца бронирования'
            )
        return values


class BookingUpdateRequest(BaseModel):
    date_from: date | None = Field(default=date.today)
    date_to: date | None = Field(default=(date.today() + timedelta(days=1)))
    room_id: int | None = Field(None)

    @field_validator('date_from')
    def check_date_from_later_than_now(cls, value):
        if value < date.today():
            raise ValueError(
                'Дата бронирования не может быть раньше текущего времени'
            )
        return value

    @model_validator(mode='before')
    def check_date_to_later_than_date_from(cls, values):
        if values['date_to'] <= values['date_from']:
            raise ValueError(
                'Время начала бронирвоания не может быть '
                'раньше времени конца бронирования'
            )
        return values

    model_config = ConfigDict(from_attributes=True)


class BookingUpdate(BaseModel):
    date_from: date | None = Field(default=date.today)
    date_to: date | None = Field(default=(date.today() + timedelta(days=1)))
    room_id: int | None = Field(None)


class BookingCreate(BookingCreateRequest):
    price: int
    user_id: int


class BookingResponse(BaseModel):
    id: int
    date_from: date
    date_to: date
    room_id: int
    user_id: int
    price: int
    total_cost: int

    model_config = ConfigDict(from_attributes=True)
