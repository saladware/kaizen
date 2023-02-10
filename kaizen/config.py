from os import environ


# application
APP_HOST = environ.get("APP_HOST", "localhost")
APP_PORT = int(environ.get("APP_PORT", 8080))

# database
DB_USER = environ["DB_USER"]
DB_PASSWORD = environ["DB_PASSWORD"]
DB_NAME = environ["DB_NAME"]
DB_HOST = environ.get("DB_HOST", "localhost")
DB_PORT = int(environ.get("DB_PORT", 5432))

# authorization
SECRET_KEY = environ["APP_SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
