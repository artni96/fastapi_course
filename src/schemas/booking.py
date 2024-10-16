from pydantic import BaseModel, field_validator, model_validator, Field
from datetime import date, timedelta


class BookingCreate(BaseModel):
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


class BookingResponse(BaseModel):
    date_from: date
    date_to: date
    room_id: int
    user_id: int
    price: int
    total_cost: int
