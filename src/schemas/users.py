from pydantic import BaseModel, Field, ConfigDict, field_validator
import re


class UserRequestAdd(BaseModel):
    email: str = Field(max_length=100)
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

    @field_validator('email')
    def validate_email(cls, value: str):
        email_pattern = r"^\S+@\S+\.\S+$"
        if not re.fullmatch(email_pattern, value):
            raise ValueError(
                'Пожалуйста, укажите валидный email. Например - test@test.test'
            )
        return value


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
