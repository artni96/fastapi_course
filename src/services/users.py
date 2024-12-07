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
            new_user = await self.db.users.add(new_user_data)
            await self.db.commit()
            return new_user
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
