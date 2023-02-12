from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..users.dependencies import get_current_user
from ..users.models import User
from ..exceptions import PermissionDenied
from ..db import get_session
from . import service


async def get_author(proposal_id: UUID, user: User = Depends(get_current_user),
                     session: AsyncSession = Depends(get_session)) -> User:
    authors = await service.get_proposal_authors(session, proposal_id)
    if user not in authors:
        raise PermissionDenied('you are not the author of this proposal')
    return user


