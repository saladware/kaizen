import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr


class Role(str, Enum):
    ADMIN = "ADMIN"
    DIRECTOR = "DIRECTOR"
    MEMBER = "MEMBER"
    CONTROLLER = "CONTROLLER"
    EMPLOYEE = "EMPLOYEE"


class RegisterUser(BaseModel):
    fullname: str
    email: EmailStr
    password: str
    department: str
    post: str


class User(BaseModel):
    id: UUID
    fullname: str
    email: EmailStr
    department: str
    post: str
    registered_at: datetime.datetime

    class Config:
        orm_mode = True


class EditUser(BaseModel):
    fullname: str | None
    email: EmailStr | None
    department: str | None
    post: str | None


class ChangeUserPassword(BaseModel):
    new_password: str
    old_password: str


class Token(BaseModel):
    access_token: str
    token_type: str
