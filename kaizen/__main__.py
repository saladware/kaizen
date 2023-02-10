import uvicorn
from . import app, config

if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host=config.APP_HOST,
        port=config.APP_PORT,
        server_header=False
    )
