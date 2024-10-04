from pydantic import BaseModel, Field, ConfigDict


class UserRequestAdd(BaseModel):
    email: str = Field(max_length=100)
    username: str = Field(max_length=100)
    password: str = Field(max_length=64)
    first_name: str | None = Field(default=None, max_length=64)
    last_name: str | None = Field(default=None, max_length=128)
    role: str = Field(default='Пользователь')


class UserAdd(BaseModel):
    email: str = Field(max_length=100)
    username: str = Field(max_length=100)
    hashed_password: str = Field(max_length=64)
    first_name: str | None = Field(default=None, max_length=64)
    last_name: str | None = Field(default=None, max_length=128)
    role: str = Field(default='Пользователь')


class User(BaseModel):
    id: int
    email: str = Field(max_length=100)
    username: str = Field(max_length=100)
    first_name: str | None = Field(default=None, max_length=64)
    last_name: str | None = Field(default=None, max_length=128)
    role: str

    model_config = ConfigDict(from_attributes=True)
