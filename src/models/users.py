from src.db import Base
from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy import String, Enum, Column
import enum


class UserRoleEnum(enum.Enum):
    ADMIN = 'Админ'
    MODER = 'Модератор'
    USER = 'Пользователь'


class UsersModel(Base):

    username: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(100))
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str] = mapped_column(String(128))
    role: Mapped[str]

    @validates('role')
    def validate_role(self, key, value: str):
        role_list = ('Админ', 'Модератор', 'Пользователь')

        if value.lower() not in role_list:
            return f"Роли на выбор: {role_list}"
        return value.capitalize()
