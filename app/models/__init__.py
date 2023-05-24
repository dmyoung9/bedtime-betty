import quart.flask_patch  # noqa: F401

from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from quart_sqlalchemy import SQLAlchemy


T = TypeVar("T")
DEFAULT_NUM = 3

db = SQLAlchemy()


class RequestModel(BaseModel, Generic[T]):
    obj: Type[T]
