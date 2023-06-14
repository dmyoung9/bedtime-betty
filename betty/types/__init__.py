from __future__ import annotations

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

from sqlalchemy.orm import Mapped
from sqlalchemy_serializer import SerializerMixin

from ..database import db


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

    @staticmethod
    @abstractmethod
    def get_item_model() -> Type[ItemModel[ItemType]]:
        ...

    @staticmethod
    @abstractmethod
    def get_completion_request_model() -> Type[ItemRequestModel[ModelType]]:
        ...

    @staticmethod
    @abstractmethod
    def get_response_model() -> Type[ItemResponseModel[ModelType]]:
        ...

    @staticmethod
    @abstractmethod
    def get_database_model() -> Type[ItemDatabaseModel]:
        ...


class ItemModel(BaseModel, Generic[ItemType]):
    pass


class ItemRequestModel(GenericModel, Generic[ModelType]):
    pass


class ItemRetrieveModel(ItemRequestModel[ModelType]):
    id: int


class ItemResponseModel(GenericModel, Generic[ModelType]):
    data: list[ModelType]


class ItemDatabaseModel(db.Model, SerializerMixin):
    __abstract__ = True

    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
