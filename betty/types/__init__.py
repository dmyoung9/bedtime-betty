from __future__ import annotations

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel


ItemType = TypeVar("ItemType", bound="Item")
ModelType = TypeVar("ModelType", bound="ItemModel")


@dataclass
class Item(Generic[ItemType], metaclass=ABCMeta):
    @classmethod
    def key(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def plural(cls) -> str:
        return f"{cls.key()}s"

    @classmethod
    @abstractmethod
    def get_item_model(cls) -> Type[ItemModel[ItemType]]:
        ...

    @classmethod
    @abstractmethod
    def get_completion_request_model(cls) -> Type[ItemRequestModel[ModelType]]:
        ...

    @classmethod
    @abstractmethod
    def get_response_model(cls) -> Type[ItemResponseModel[ModelType]]:
        ...


class ItemModel(BaseModel, Generic[ItemType]):
    pass


class ItemRequestModel(GenericModel, Generic[ModelType]):
    pass


class ItemResponseModel(GenericModel, Generic[ModelType]):
    data: list[ModelType]
