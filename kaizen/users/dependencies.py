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
from ..exceptions import PermissionDenied

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
    if not user.is_active:
        raise PermissionDenied('user is inactive')
    return user


async def get_current_controller(user: User = Depends(get_current_user)) -> User:
    if user.role not in (Role.CONTROLLER, Role.ADMIN):
        raise PermissionDenied('you are not a controller')
    return user


async def get_current_member(user: User = Depends(get_current_user)) -> User:
    if user.role not in (Role.MEMBER, Role.DIRECTOR, Role.ADMIN):
        raise PermissionDenied('you are not a member')
    return user


async def get_current_director(user: User = Depends(get_current_user)) -> User:
    if user.role not in (Role.DIRECTOR, Role.ADMIN):
        raise PermissionDenied('you are not a director')
    return user


async def get_current_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != Role.ADMIN:
        raise PermissionDenied('you are not a admin')
    return user


async def get_user_from_path(user_id: UUID, current_user: User = Depends(get_current_user),
                             session: AsyncSession = Depends(get_session)) -> User:
    """returns the user from user_id in the path if the current user id is in the path or if the user is
    an administrator"""
    if current_user.id == user_id:
        return current_user
    if current_user.role == Role.ADMIN:
        return await get_user(session, user_id)
    raise PermissionDenied('you are not a admin')

