import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
DEEZER_BASE_URL = os.getenv("DEEZER_BASE_URL")

if not DEEZER_BASE_URL:
    raise RuntimeError("DEEZER_BASE_URL is not set in environment variables")
