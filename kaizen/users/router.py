from datetime import timedelta
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from .service import authenticate_user, create_access_token, get_current_user
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES
from ..db import get_session
from ..exceptions import EntityAlreadyExists, EntityNotExists, PermissionDenied
from . import service, schemas

users = APIRouter(prefix="/users", tags=["users"])


@users.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 session: AsyncSession = Depends(get_session)) -> schemas.Token:
    user = await authenticate_user(
        session=session,
        email=form_data.username,
        password=form_data.password
    )
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


@users.get('/me')
async def get_my_details(user=Depends(get_current_user)) -> schemas.User:
    return user


@users.post("/")
async def register_user(user_data: schemas.RegisterUser, session: AsyncSession = Depends(get_session)) -> schemas.User:
    try:
        return await service.create_user(session, user_data)
    except EntityAlreadyExists:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "user with this email already exists")


@users.get("/{user_id}")
async def get_user_details(user_id: UUID, session: AsyncSession = Depends(get_session)) -> schemas.User:
    try:
        return await service.get_user(session, user_id)
    except EntityNotExists:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user is not found")


@users.put("/{user_id}")
async def edit_user_details(user_id: UUID, user_data: schemas.EditUser,
                            session: AsyncSession = Depends(get_session)) -> schemas.User:
    try:
        return await service.update_user_details(session, user_id, user_data)
    except EntityAlreadyExists:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "user with this email already exists")


@users.put("/{user_id}/password")
async def change_passowrd(
        user_id: UUID,
        data: schemas.ChangeUserPassword,
        session: AsyncSession = Depends(get_session)
):
    try:
        await service.change_user_password(
            session=session,
            user_id=user_id,
            old_password=data.old_password,
            new_password=data.new_password
        )
    except PermissionDenied:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "incorrect password")


