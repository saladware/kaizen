from uuid import UUID

from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from ..db import get_session
from .schemas import Role
from .models import User
from .service import get_user
from ..config import ALGORITHM, SECRET_KEY


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


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


async def get_controller(user: User = Depends(get_current_user)) -> User:
    if user.role not in (Role.CONTROLLER, Role.ADMIN):
        raise HTTPException(status.HTTP_403_FORBIDDEN, 'permission denied: you are not a controller')
    return user


async def get_member(user: User = Depends(get_current_user)) -> User:
    if user.role not in (Role.MEMBER, Role.DIRECTOR, Role.ADMIN):
        raise HTTPException(status.HTTP_403_FORBIDDEN, 'permission denied: you are not a member')
    return user


async def get_director(user: User = Depends(get_current_user)) -> User:
    if user.role not in (Role.DIRECTOR, Role.ADMIN):
        raise HTTPException(status.HTTP_403_FORBIDDEN, 'permission denied: you are not a director')
    return user


async def get_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != Role.ADMIN:
        raise HTTPException(status.HTTP_403_FORBIDDEN, 'permission denied: you are not an administrator')
    return user


async def get_user_from_path(user_id: UUID, user: User = Depends(get_current_user)):
    if user.role != Role.ADMIN and user.id != user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, 'permission denied: you are not an administrator')
    return user
