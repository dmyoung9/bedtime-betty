from __future__ import annotations

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel


ItemType = TypeVar("ItemType", bound="Item")
ModelType = TypeVar("ModelType", bound="ItemModel")


@dataclass
class Item(metaclass=ABCMeta):
    @classmethod
    def key(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def plural(cls) -> str:
        return f"{cls.key()}s"


class ItemModel(BaseModel, Generic[ItemType]):
    @classmethod
    @abstractmethod
    def get_dataclass(cls) -> Type[ItemType]:
        ...

    @classmethod
    @abstractmethod
    def get_completion_request_model(cls) -> Type[ItemRequestModel[ModelType]]:
        ...

    @classmethod
    @abstractmethod
    def get_response_model(cls) -> Type[ItemResponseModel[ModelType]]:
        ...


class ItemCreateModel(GenericModel, Generic[ModelType]):
    _obj: Type[ModelType]


class ItemRequestModel(GenericModel, Generic[ModelType]):
    pass


class ItemResponseModel(GenericModel, Generic[ModelType]):
    data: list[ModelType]
