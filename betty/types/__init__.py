from __future__ import annotations

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Generic, Type, TypeVar

from pydantic import BaseModel


T = TypeVar("T")


@dataclass
class Item(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def model(cls) -> Type[ItemModel]:
        ...

    @classmethod
    @abstractmethod
    def request_model(cls) -> Type[ItemRequestModel]:
        ...

    @classmethod
    @abstractmethod
    def response_model(cls) -> Type[ItemResponseModel]:
        ...

    @classmethod
    def key(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def plural(cls) -> str:
        return f"{cls.key()}s"


class ItemModel(BaseModel):
    pass


class ItemRequestModel(BaseModel):
    obj: Type[ItemModel]


class ItemResponseModel(BaseModel, Generic[T]):
    data: list[T]
