from dotenv import load_dotenv

load_dotenv()

import os  # noqa: E402


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
