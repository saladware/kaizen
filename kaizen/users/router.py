from datetime import timedelta
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from .service import authenticate_user, create_access_token
from .dependencies import get_current_user, get_current_admin, get_user_from_path
from .models import User
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES
from ..db import get_session
from . import service, schemas

users = APIRouter(prefix="/users", tags=["users"])


@users.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 session: AsyncSession = Depends(get_session)) -> schemas.Token:
    user = await authenticate_user(session, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@users.get('/me', tags=['me'])
async def get_my_details(user: User = Depends(get_current_user)) -> schemas.User:
    return user


@users.put('/me', tags=['me'])
async def change_my_details(
        user_data: schemas.EditUser,
        session: AsyncSession = Depends(get_session),
        user: User = Depends(get_current_user)
) -> schemas.User:
    await service.change_user_details(session, user, **user_data.dict())
    return user


@users.put('/me/password', tags=['me'])
async def change_my_password(
    data: schemas.ChangeUserPassword,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    await service.change_user_password(session, user, data.old_password, data.new_password)


@users.post("/", tags=['admin'])
async def register_user(
        user_data: schemas.RegisterUser,
        session: AsyncSession = Depends(get_session),
        _: User = Depends(get_current_admin)
) -> schemas.User:
    user = await service.create_user(session, **user_data.dict())
    return user


@users.get("/{user_id}", tags=['admin'])
async def get_user_details(user: User = Depends(get_user_from_path)) -> schemas.User:
    return user


@users.put("/{user_id}", tags=['admin'])
async def edit_user_details(
        user_data: schemas.EditUser,
        user: User = Depends(get_user_from_path),
        session: AsyncSession = Depends(get_session)
) -> schemas.User:
    await service.change_user_details(session, user, **user_data.dict())
    return user


@users.put("/{user_id}/password", tags=['admin'])
async def change_password(
        data: schemas.ChangeUserPassword,
        user: User = Depends(get_user_from_path),
        session: AsyncSession = Depends(get_session)
):
    await service.change_user_password(session, user, data.old_password, data.new_password)


@users.delete('/{user_id}', tags=['admin'], dependencies=[Depends(get_current_admin)])
async def deactivate_user(user_id: UUID, session: AsyncSession = Depends(get_session)):
    await service.deactivate_user(session, user_id)
