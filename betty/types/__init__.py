from __future__ import annotations

from abc import ABCMeta
from dataclasses import dataclass
from typing import Generic, Type, TypeVar

from pydantic import BaseModel


T = TypeVar("T")


@dataclass
class Item(metaclass=ABCMeta):
    @classmethod
    def model(cls) -> Type[ItemModel]:
        raise NotImplementedError()

    @classmethod
    def request_model(cls) -> Type[ItemRequestModel]:
        raise NotImplementedError()

    @classmethod
    def create_model(cls) -> Type[ItemCreateModel]:
        raise NotImplementedError()

    @classmethod
    def response_model(cls) -> Type[ItemResponseModel]:
        raise NotImplementedError()

    @classmethod
    def key(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def plural(cls) -> str:
        return f"{cls.key()}s"


class ItemModel(BaseModel):
    pass


class ItemCreateModel(BaseModel):
    obj: Type[ItemModel]


class ItemRequestModel(BaseModel):
    obj: Type[ItemModel]


class ItemResponseModel(BaseModel, Generic[T]):
    data: list[T]
