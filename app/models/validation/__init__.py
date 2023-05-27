from typing import Generic, Type, TypeVar

from pydantic import BaseModel

DEFAULT_NUM = 3
T = TypeVar("T")


class ItemModel(BaseModel, Generic[T]):
    obj: Type[T]

    class Config:
        extra = "forbid"


class RequestModel(BaseModel, Generic[T]):
    obj: Type[T]

    class Config:
        extra = "forbid"
