import os
from dotenv import load_dotenv

load_dotenv()  # 👈 loads .env

APP_NAME = os.getenv("APP_NAME", "FastAPI App")
DEBUG = os.getenv("DEBUG", "False") == "True"

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
)

DATABASE_URL = os.getenv("DATABASE_URL")

FRONTEND_URL = os.getenv("FRONTEND_URL")
