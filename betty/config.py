import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI: str = os.environ.get("SQLALCHEMY_DATABASE_URI", "")
    BASE_API_URL: str = os.environ.get("BASE_API_URL", "")
    SSL_ENABLED: bool = os.environ.get("SSL_ENABLED", "false").lower() == "true"
