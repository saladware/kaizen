import uuid

from sqlalchemy import Column, String, Text, Enum, text

from ..db import Base
from sqlalchemy.dialects.postgresql import UUID

from .schemas import Role


class User(Base):
    __tablename__ = 'users'

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    email: str = Column(String(264), unique=True, nullable=False)
    fullname: str = Column(String(264), nullable=False)
    department: str = Column(String(264), nullable=False)
    post: str = Column(String(264), nullable=False)
    role: Role = Column(Enum(Role), server_default="EMPLOYEE")
    hashed_password: str = Column(Text, nullable=False)
