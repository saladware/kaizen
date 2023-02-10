import datetime
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from .models import Proposal, ProposalAuthor
from .schemas import CreateProposal
from ..users.models import User
from ..exceptions import EntityAlreadyExists


async def proposal_add_author(session: AsyncSession, proposal: Proposal, author: User):
    author = ProposalAuthor(proposal_id=proposal.id, user_id=author.id)
    session.add(author)
    await session.commit()  # TODO: hadnle unique constraint exception


async def generate_proposal_number(session: AsyncSession, proposal: Proposal) -> str:
    if proposal.number is not None:
        raise EntityAlreadyExists
    group = {"WITH_ECO": 1, "WITHOUT_ECO": 2, "IMPORTANT": 3}[proposal.category]
    proposal_rows = await session.execute(func.count(Proposal.id))
    serial = proposal_rows.scalar()
    year = datetime.date.today().year
    return f"{group}-{serial:05}-{year}"


async def create_proposal(session: AsyncSession, data: CreateProposal, initiator: User) -> Proposal:
    proposal = Proposal(
        title=data.title,
        problem_description=data.problem_description,
        proposal_content=data.proposal_content,
        expected_result=data.expected_result,
        category=data.category,
        initiator_id=initiator.id
    )
    session.add(proposal)
    try:
        await session.commit()
    except IntegrityError as e:
        raise EntityAlreadyExists("proposal with this title already exists")
    await session.refresh(proposal)
    await proposal_add_author(session, proposal, initiator)
    return proposal


async def get_proposal_details(session: AsyncSession, proposal_id: UUID):
    result = await session.execute(
        statement=select(Proposal).where(Proposal.id == proposal_id)
    )
    return result.scalar_one()


async def get_user_proposals(session: AsyncSession, user_id: UUID) -> list[Proposal]:
    result = await session.execute(
        select(Proposal)
        .join(ProposalAuthor, Proposal.id == ProposalAuthor.proposal_id)
        .filter(ProposalAuthor.user_id == user_id)
    )
    return list(result.scalars())


async def edit_proposal(session: AsyncSession, proposal_id: UUID, data):
    ...
