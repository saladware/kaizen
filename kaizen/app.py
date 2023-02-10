from fastapi import FastAPI

from .proposals.router import proposals
from .users.router import users

app = FastAPI(
    title='Управление ППУ',
    description='web application for manage improvement proposals',
    version='0.1.2'
)

app.include_router(proposals)
app.include_router(users)
