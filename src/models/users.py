from src.db import Base
from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy import String
import re


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
            raise ValueError(
                f'Пожалуйста, выберите одну из предложенных ролей: {role_list}'
            )
        return value.capitalize()

    @validates('email')
    def validate_email(self, key, value: str):
        email_pattern = r"^\S+@\S+\.\S+$"
        if not re.fullmatch(email_pattern, value):
            raise ValueError(
                'Пожалуйста, укажите валидный email. Например - test@test.test'
            )
        return value
