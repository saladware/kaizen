from datetime import datetime
import uuid

from sqlalchemy import Column, String, Text, DateTime, text, Enum, Float, Boolean, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID

from ..db import Base
from .schemas import ProposalCategory, VerificationResult


class ProposalVerification(Base):
    __tablename__ = 'verifications'

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True)
    verified_at: datetime = Column(DateTime(timezone=True), nullable=False)
    controller_id = Column(UUID(as_uuid=True), nullable=False)
    result: VerificationResult = Column(Enum(VerificationResult), nullable=False)
    comment: str = String(Text)


class ProposalAuthor(Base):
    __tablename__ = 'authors'
    __table_args__ = (
        UniqueConstraint('proposal_id', 'user_id', name='_proposal_author_uc'),
    )

    proposal_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True)
    user_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True)
    weight: float = Column(Float(), server_default=text("1.0"))
    created_at: datetime = Column(DateTime(timezone=True), server_default=func.now())


class Proposal(Base):
    __tablename__ = 'proposals'

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    number: str | None = Column(String(12), unique=True)
    title: str = Column(String(200), unique=True, nullable=False)
    registered_at: datetime | None = Column(DateTime(timezone=True))
    created_at: datetime = Column(DateTime(timezone=True), server_default=func.now())
    problem_description: str = Column(Text, nullable=False)
    proposal_content: str = Column(Text, nullable=False)
    expected_result: str = Column(Text, nullable=False)
    category: ProposalCategory = Column(Enum(ProposalCategory), nullable=False)
    initiator_id: uuid.UUID = Column(UUID(as_uuid=True), nullable=False)
    is_verified: bool = Column(Boolean, server_default=text("false"))
