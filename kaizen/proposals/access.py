from uuid import UUID

from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..users.access import get_current_user
from ..users.models import User
from ..db import get_session
from . import service


async def get_author(proposal_id: UUID, user: User = Depends(get_current_user),
                     session: AsyncSession = Depends(get_session)) -> User:
    authors = await service.get_proposal_authors(session, proposal_id)
    if user not in authors:
        raise HTTPException(status.HTTP_403_FORBIDDEN, 'permission denied: you are not the author of this proposal')
    return user


