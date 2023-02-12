import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel

from ..users.schemas import User


class VerificationResult(str, Enum):
    REJECTED = "REJECTED"
    ACCEPTED = "ACCEPTED"


class ProposalCategory(str, Enum):
    WITH_ECO = "WITH_ECO"
    WITHOUT_ECO = "WITHOUT_ECO"
    IMPORTANT = "IMPORTANT"


class ProposalAuthor(BaseModel):
    user_id: UUID
    weight: float
    created_at: datetime.datetime


class CreateProposal(BaseModel):
    title: str
    problem_description: str
    proposal_content: str
    expected_result: str
    category: ProposalCategory


class ProposalVerification(BaseModel):
    verified_at: datetime.datetime
    controller: User
    result: VerificationResult


class Proposal(BaseModel):
    id: UUID
    number: str | None
    title: str
    registered_at: datetime.datetime | None
    created_at: datetime.datetime
    problem_description: str
    proposal_content: str
    expected_result: str
    category: ProposalCategory
    initiator_id: UUID
    is_verified: bool

    class Config:
        orm_mode = True


class ProposalDetails(BaseModel):
    id: UUID
    number: str | None
    title: str
    registered_at: datetime.datetime | None
    created_at: datetime.datetime
    problem_description: str
    proposal_content: str
    expected_result: str
    category: ProposalCategory
    initiator: User
    verification: ProposalVerification | None
    authors: list[ProposalAuthor]


class ProposalList(BaseModel):
    proposals: list[Proposal]
