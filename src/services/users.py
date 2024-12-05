# from typing import Optional, Union
#
# from fastapi import Depends, Request
# from fastapi_users import (
#     BaseUserManager,
#     FastAPIUsers,
#     IntegerIDMixin,
#     InvalidPasswordException,
# )
# from fastapi_users.authentication import (
#     AuthenticationBackend,
#     BearerTransport,
#     JWTStrategy,
# )
# from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from src.config import settings
# from src.db import get_async_session
# from src.models.users import User
# from src.schemas.users import UserCreate
# import re
#
# async def get_user_db(session: AsyncSession = Depends(get_async_session)):
#     yield SQLAlchemyUserDatabase(session, User)
#
#
# bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
#
#
# def get_jwt_strategy() -> JWTStrategy:
#     return JWTStrategy(secret=settings.SECRET_KEY, lifetime_seconds=3600)
#
#
# auth_backend = AuthenticationBackend(
#     name="jwt",
#     transport=bearer_transport,
#     get_strategy=get_jwt_strategy,
# )
#
#
# class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
#     async def validate_password(
#         self,
#         password: str,
#         user: Union[UserCreate, User],
#     ) -> None:
#         if len(password) < 6:
#             raise InvalidPasswordException(
#                 reason="Password should be at least 3 characters"
#             )
#         if not (
#             (re.search("[а-я]", password, re.IGNORECASE))
#             or (re.search("[a-z]", password, re.IGNORECASE))
#         ):
#             raise InvalidPasswordException(
#                 reason=(
#                     "Password should contain at least " '1 "a-z" or "а-я" character'
#                 )
#             )
#         if user.email in password:
#             raise InvalidPasswordException(reason="Password should not contain e-mail")
#
#     async def on_after_register(self, user: User, request: Optional[Request] = None):
#         print(f"Пользователь {user.email} зарегистрирован.")
#
#
# async def get_user_manager(user_db=Depends(get_user_db)):
#     yield UserManager(user_db)
#
#
# fastapi_users = FastAPIUsers[User, int](
#     get_user_manager,
#     [auth_backend],
# )
#
# current_user = fastapi_users.current_user(active=True)
# current_superuser = fastapi_users.current_user(active=True, superuser=True)
from datetime import timezone, datetime, timedelta

import jwt
from passlib.context import CryptContext

from src.config import settings
from src.exceptions import IncorrectTokenException, ObjectAlreadyExistsException, UserAlreadyExistsException, \
    EmailNotRegisteredException, IncorrectPasswordException
from src.schemas.users import UserAdd, UserRequestAdd, UserLoginRequest
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        user_info = await self.get_one_with_role(data['user_id'])
        to_encode = user_info.model_dump()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise IncorrectTokenException

    async def register_user(self, data: UserRequestAdd):
        hashed_password = self.hash_password(data.password)
        new_user_data = UserAdd(hashed_password=hashed_password, **data.model_dump())
        try:
            await self.db.users.add(new_user_data)
            await self.db.commit()
        except ObjectAlreadyExistsException as ex:
            raise UserAlreadyExistsException from ex

    async def login_user(self, data: UserLoginRequest) -> str:
        user = await self.db.users.get_user_with_hashed_password(email=data.email)
        if not user:
            raise EmailNotRegisteredException
        if not self.verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordException
        access_token = await self.create_access_token({"user_id": user.id})
        return access_token

    async def get_one_or_none_user(self, user):
        return await self.db.users.get_one_or_none(id=user.id)

    async def get_one_with_role(self, user_id: int):
        return await self.db.users.get_user_info_for_jwt_token(user_id)
