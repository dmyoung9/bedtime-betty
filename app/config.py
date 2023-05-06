from dotenv import load_dotenv

load_dotenv()

import os  # noqa: E402


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    BASE_API_URL = os.environ.get("BASE_API_URL")
    SSL_ENABLED = os.environ.get("SSL_ENABLED").lower() == "true"
