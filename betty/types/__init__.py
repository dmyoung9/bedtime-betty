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
    """Base class for all Items."""

    @classmethod
    def key(cls) -> str:
        """Returns the key for this Item."""
        return cls.__name__.lower()

    @classmethod
    def plural(cls) -> str:
        """Returns the plural form of this Item."""
        return f"{cls.key()}s"

    @staticmethod
    @abstractmethod
    def get_item_model() -> Type[ItemModel[ItemType]]:
        """Returns the model for this type of Item."""
        ...

    @staticmethod
    @abstractmethod
    def get_completion_request_model() -> Type[ItemRequestModel[ModelType]]:
        """Returns the model for requesting a completion of this type of Item."""
        ...

    @staticmethod
    @abstractmethod
    def get_response_model() -> Type[ItemResponseModel[ModelType]]:
        """Returns the model for the response from a completion of this type of Item."""
        ...

    @staticmethod
    @abstractmethod
    def get_database_model() -> Type[ItemDatabaseModel]:
        """Returns the database model for this type of Item."""
        ...


class ItemModel(BaseModel, Generic[ItemType]):
    """Base class for all Item models."""

    pass


class ItemRequestModel(GenericModel, Generic[ModelType]):
    """Base class for all request models."""

    pass


class ItemRetrieveModel(ItemRequestModel[ModelType]):
    """Base class for all "retrieve" request models."""

    id: int


class ItemResponseModel(GenericModel, Generic[ModelType]):
    """Base class for all response models."""

    data: list[ModelType]


class ItemDatabaseModel(db.Model, SerializerMixin):
    """Base class for all database models."""

    __abstract__ = True

    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
