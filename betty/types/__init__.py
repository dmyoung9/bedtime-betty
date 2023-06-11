from __future__ import annotations

from abc import ABCMeta
from dataclasses import asdict, dataclass
from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel


ItemType = TypeVar("ItemType", bound="Item")
ModelType = TypeVar("ModelType", bound="ItemModel")


@dataclass
class Item(metaclass=ABCMeta):
    @classmethod
    def model(cls) -> Type[ItemModel]:
        raise NotImplementedError()

    @classmethod
    def request_model(cls) -> Type[ItemRequestModel[ItemModel]]:
        raise NotImplementedError()

    @classmethod
    def create_model(cls) -> Type[ItemCreateModel[ItemModel]]:
        raise NotImplementedError()

    @classmethod
    def response_model(cls) -> Type[ItemResponseModel[ItemModel]]:
        raise NotImplementedError()

    @classmethod
    def key(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def plural(cls) -> str:
        return f"{cls.key()}s"


class ItemModel(BaseModel, Generic[ItemType, ModelType]):
    @classmethod
    def from_item(cls, item: ItemType):
        return cls(**asdict(item))

    def to_item(self) -> ItemType:
        return self.obj(**self.dict())


class ItemCreateModel(GenericModel, Generic[ModelType]):
    _obj: Type[ModelType]


class ItemRequestModel(GenericModel, Generic[ModelType]):
    pass


class ItemResponseModel(GenericModel, Generic[ModelType]):
    data: list[ModelType]
