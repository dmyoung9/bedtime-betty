import quart.flask_patch  # noqa: F401

from typing import TypeAlias

from quart_sqlalchemy import SQLAlchemy
from quart_sqlalchemy.model import DefaultMeta

db = SQLAlchemy()

BaseModel: TypeAlias = DefaultMeta
