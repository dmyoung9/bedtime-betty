from __future__ import annotations

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Type

from pydantic import BaseModel


@dataclass
class Item(metaclass=ABCMeta):
    @classmethod
    def key(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def plural(cls) -> str:
        return f"{cls.key()}s"

    @classmethod
    @abstractmethod
    def response_model(cls) -> Type[ItemModel]:
        ...

    @classmethod
    @abstractmethod
    def model(cls) -> Type[ItemModel]:
        ...


class ItemModel(BaseModel):
    pass


class ItemResponseModel(BaseModel):
    data: list[ItemModel]
