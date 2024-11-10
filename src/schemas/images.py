from pydantic import BaseModel


class ImageCreate(BaseModel):
    name: str


class ImageRead(ImageCreate):
    id: int
