from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .proposals.router import proposals
from .users.router import users
from . import exceptions


app = FastAPI(
    title='Управление ППУ',
    description='web application for manage improvement proposals',
    version='0.0.1'
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(proposals)
app.include_router(users)


@app.exception_handler(exceptions.PermissionDenied)
async def on_permission_denied(_: Request, e: exceptions.PermissionDenied):
    message = 'Permission denied'
    if len(e.args) > 0:
        message += f': {e.args[0]}'
    return JSONResponse(
        content={'error': message},
        status_code=status.HTTP_403_FORBIDDEN
    )


@app.exception_handler(exceptions.EntityAlreadyExists)
async def on_already_exists(_: Request, e: exceptions.EntityAlreadyExists):
    message = 'Entity already exists'
    if len(e.args) > 0:
        message = e.args[0]
    return JSONResponse(
        content={'error': message},
        status_code=status.HTTP_400_BAD_REQUEST
    )


@app.exception_handler(exceptions.EntityNotExists)
async def on_not_exists(_: Request, e: exceptions.EntityNotExists):
    message = 'Not found'
    if len(e.args) > 0:
        message = e.args[0]
    return JSONResponse(
        content={'error': message},
        status_code=status.HTTP_400_BAD_REQUEST
    )
