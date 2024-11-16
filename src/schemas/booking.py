from datetime import date, datetime, timedelta

from pydantic import (BaseModel, ConfigDict, Field, field_serializer,
                      field_validator, model_validator)

from src.constants import DATE_FORMAT, DATETIME_FORMAT


class BookingCreateRequest(BaseModel):
    date_from: date | str = Field(
        default=(date.today().strftime(DATE_FORMAT)))
    date_to: date | str = Field(
        default=(
            date.today() + timedelta(days=1)
            ).strftime(DATE_FORMAT)
        )
    room_id: int

    model_config = {
        'json_schema_extra': {
            'Создание новой брони': {
                'summary': 'Создание новой брони',
                'value': {
                    'date_from': date.today().strftime(DATE_FORMAT),
                    'date_to': (
                        date.today() + timedelta(days=1)
                        ).strftime(DATE_FORMAT),
                    'room_id': 1,
                }
            }
        }
    }

    @field_validator('date_from')
    def check_date_from_later_than_now(cls, value):
        if value < date.today():
            raise ValueError(
                'Дата бронирования не может быть раньше текущего времени'
            )
        return value

    @model_validator(mode='before')
    def check_date_to_later_than_date_from(cls, values):
        values['date_to'] = datetime.strptime(
                values['date_to'],
                DATE_FORMAT
            )
        values['date_from'] = datetime.strptime(
                values['date_from'],
                DATE_FORMAT
            )
        if values['date_to'] <= values['date_from']:
            raise ValueError(
                'Время начала бронирвоания не может быть '
                'раньше времени конца бронирования'
            )
        return values


class BookingCreate(BaseModel):

    price: int
    user_id: int
    date_to: date
    date_from: date
    room_id: int


class BookingUpdateRequest(BaseModel):
    date_from: date | str | None = Field(
        default=(date.today().strftime(DATE_FORMAT)))
    date_to: date | str | None = Field(
        default=(
            date.today() + timedelta(days=1)
            ).strftime(DATE_FORMAT)
        )
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
        values['date_to'] = datetime.strptime(values['date_to'], DATE_FORMAT)
        values['date_from'] = datetime.strptime(
            values['date_from'], DATE_FORMAT)
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

    @field_serializer('date_to')
    def serialize_date_to(self, date_to: date):
        return date_to.strftime(DATE_FORMAT)

    @field_serializer('date_from')
    def serialize_date_from(self, date_from: date):
        return date_from.strftime(DATE_FORMAT)

    @field_serializer('created_at')
    def serialize_created_at(self, created_at: datetime):
        return created_at.strftime(DATETIME_FORMAT)

    @field_serializer('updated_at')
    def serialize_updated_at(self, created_at: datetime):
        if created_at:
            return created_at.strftime(DATETIME_FORMAT)
        return None
