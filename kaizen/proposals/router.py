from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from . import service, schemas
from ..users.models import User
from ..users.service import get_current_user
from ..exceptions import EntityAlreadyExists

proposals = APIRouter(
    prefix='/proposals',
    tags=['proposals']
)


@proposals.get('/my')
async def get_my_proposals(session: AsyncSession = Depends(get_session),
                           user: User = Depends(get_current_user)) -> schemas.ProposalList:
    result = await service.get_user_proposals(session, user.id)
    return schemas.ProposalList(proposals=result)


@proposals.get('/{id}')
async def get_proposal_by_id(proposal_id: UUID, session: AsyncSession = Depends(get_session)) -> schemas.Proposal:
    return await service.get_proposal_details(session, proposal_id)


@proposals.post('/')
async def create_proposal(data: schemas.CreateProposal, session: AsyncSession = Depends(get_session),
                          user: User = Depends(get_current_user)) -> schemas.Proposal:
    try:
        return await service.create_proposal(session, data, user)
    except EntityAlreadyExists:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "proposal with this title already exists")
