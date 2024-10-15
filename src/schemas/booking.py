from pydantic import BaseModel, Field
from datetime import date


class BookingCreate(BaseModel):
    date_from: date
    date_to: date
    room_id: int


class BookingResponse(BookingCreate):
    user_id: int
    price: int
    total_price: int
