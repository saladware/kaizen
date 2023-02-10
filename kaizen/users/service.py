from datetime import timedelta, datetime
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from PIL import ImageDraw, Image
import numpy as np
import hashlib

from .models import User
from .schemas import RegisterUser, EditUser
from ..config import ALGORITHM, SECRET_KEY
from ..db import get_session
from ..exceptions import EntityAlreadyExists, EntityNotExists, PermissionDenied

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


def _hash_password(password: str) -> str:
    return pwd_context.hash(password)


def _verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


async def create_user(session: AsyncSession, data: RegisterUser) -> User:
    user = User(
        email=data.email,
        hashed_password=_hash_password(data.password),
        fullname=data.fullname,
        post=data.post,
        department=data.department
    )
    session.add(user)
    try:
        await session.commit()
    except IntegrityError as e:
        raise EntityAlreadyExists("user with this email already exists")
    await session.refresh(user)
    return user


async def get_user(session: AsyncSession, user_id: UUID) -> User:
    cursor = await session.execute(
        statement=select(User).where(User.id == user_id)
    )
    if result := cursor.first():
        return result[0]
    raise EntityNotExists


async def get_user_by_email_or_none(session: AsyncSession, email: str) -> User | None:
    cursor = await session.execute(
        statement=select(User).where(User.email == email)
    )
    return cursor.scalar_one_or_none()


async def update_user_details(session: AsyncSession, user_id: UUID, data: EditUser) -> User:
    user = await get_user(session, user_id)
    for key, value in data.dict(exclude_none=True).items():
        setattr(user, key, value)
    try:
        await session.commit()
    except IntegrityError as e:
        raise EntityAlreadyExists("user with this email already exists")
    return user


async def change_user_password(session: AsyncSession, user_id: UUID, old_password: str, new_password: str):
    user = await get_user(session, user_id)
    if not _verify_password(old_password, user.hashed_password):
        raise PermissionDenied
    user.hashed_password = _hash_password(new_password)


async def authenticate_user(session: AsyncSession, email: str, password: str) -> User | None:
    user = await get_user_by_email_or_none(session, email)
    if user is not None and _verify_password(password, user.hashed_password):
        return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user(session, UUID(username))
    if user is None:
        raise credentials_exception
    return user


def generate_user_avatar(avatar_size: int, username: str):
    bytes_ = hashlib.md5(username.encode('utf-8')).digest()
    main_color = tuple(channel // 2 + 128 for channel in bytes_[:3])

    need_color = np.array([bit == '1' for byte in bytes_[3:3 + 9] for bit in bin(byte)[2:].zfill(8)]).reshape(6, 12)
    need_color = np.concatenate((need_color, need_color[::-1]), axis=0)

    for i in range(12):
        need_color[0, i] = 0
        need_color[11, i] = 0
        need_color[i, 0] = 0
        need_color[i, 11] = 0

    img_size = (avatar_size, avatar_size)
    block_size = avatar_size // 12
    img = Image.new('RGBA', img_size, 0)
    draw = ImageDraw.Draw(img)

    for x in range(avatar_size):
        for y in range(avatar_size):
            if need_color[x // block_size, y // block_size]:
                draw.point((x, y), main_color)

    img.save(f'{username}.png', format='png')
