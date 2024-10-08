import re

from pydantic import (BaseModel, ConfigDict, Field, field_validator,
                      model_validator, EmailStr)
from fastapi_users import schemas
from sqlalchemy import select, func
from src.models.users import User as UserModel
from fastapi import HTTPException
from src.db import async_session_maker


class UserRequestAdd(BaseModel):
    email: EmailStr = Field(max_length=100)
    username: str = Field(max_length=100)
    password: str = Field(max_length=64)
    first_name: str | None = Field(default=None, max_length=64)
    last_name: str | None = Field(default=None, max_length=128)
    role: str = Field(default='Пользователь')

    @field_validator('role')
    def validate_role(cls, value: str):
        role_list = ('Админ', 'Модератор', 'Пользователь')

        if value.capitalize() not in role_list:
            raise ValueError(
                f"Пожалуйста, выберите одну из предложенных ролей: {role_list}"
            )
        return value.capitalize()

    @model_validator(mode='after')
    def using_different_languages(cls, values):
        if values.first_name is not None and values.last_name is not None:
            full_name = f'{values.first_name} {values.last_name}'
            if (
                (re.search('[а-я]', full_name, re.IGNORECASE)) and
                (re.search('[a-z]', full_name, re.IGNORECASE))
            ):
                raise ValueError(
                    'Пожалуйста, не смешивайте русские и латинские буквы'
                )
            return values
        return values


class UserAdd(BaseModel):
    email: EmailStr = Field(max_length=100)
    username: str = Field(max_length=100)
    hashed_password: str = Field(max_length=64)
    first_name: str | None = Field(default=None, max_length=64)
    last_name: str | None = Field(default=None, max_length=128)
    role: str = Field(default='Пользователь')


class User(BaseModel):
    id: int
    email: EmailStr = Field(max_length=100)
    username: str = Field(max_length=100)
    first_name: str | None = Field(default=None, max_length=64)
    last_name: str | None = Field(default=None, max_length=128)
    role: str

    model_config = ConfigDict(from_attributes=True)


class UserJwt(BaseModel):
    email: EmailStr
    password: str


class UserJwtWithHashedPassword(User):
    hashed_password: str


class UserRead(schemas.BaseUser[int]):
    username: str = Field(max_length=64)
    first_name: str | None = Field(default=None, max_length=64)
    last_name: str | None = Field(default=None, max_length=128)


class UserCreate(schemas.BaseUserCreate):
    username: str = Field(max_length=64)
    first_name: str | None = Field(default=None, max_length=64)
    last_name: str | None = Field(default=None, max_length=128)


class UserUpdate(schemas.BaseUserUpdate):
    username: str = Field(max_length=64)
    first_name: str | None = Field(default=None, max_length=64)
    last_name: str | None = Field(default=None, max_length=128)
