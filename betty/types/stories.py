from __future__ import annotations

from dataclasses import dataclass
from typing import Type

from pydantic import Field

from sqlalchemy.orm import Mapped

from . import Item, ItemDatabaseModel, ItemModel, ItemRequestModel, ItemResponseModel
from .sections import SectionDatabaseModel, SectionModel
from ..database import db


@dataclass
class Story(Item):
    """
    Represents a Story item.

    Parameters:
    - age: The age of the story.
    - author: The author of the story.
    - title: The title of the story.
    - emoji: The emoji that conveys the plot of the story.
    - outline: A short outline of the plot of the story.
    - lesson: The lesson the story subtly teaches.
    """

    age: int
    author: str
    title: str
    emoji: str
    outline: str
    lesson: str

    @staticmethod
    def get_item_model() -> Type[StoryModel]:
        """
        Returns the model for the Story item.
        """
        return StoryModel

    @staticmethod
    def get_completion_request_model() -> Type[ItemRequestModel[ItemModel]]:
        """
        Returns the model for requesting a completion of the Story item.
        """
        raise NotImplementedError()

    @staticmethod
    def get_response_model() -> Type[ItemResponseModel[StoryModel]]:
        """
        Returns the model for the response from a completion of the Story item.
        """
        return ItemResponseModel[StoryModel]

    @staticmethod
    def get_database_model() -> Type[ItemDatabaseModel]:
        """
        Returns the database model for the Story item.
        """
        return StoryDatabaseModel


class StoryModel(ItemModel[Story]):
    """
    Represents the model for the Story item.
    """

    age: int
    author: str = Field(description="author of the story")
    title: str = Field(description="title of the story")
    emoji: str = Field(description="emoji that conveys the plot of the story")
    outline: str = Field(description="short outline of the plot of the story")
    lesson: str = Field(description="lesson the story subtly teaches")

    sections: list[SectionModel] = []


class StoryDatabaseModel(ItemDatabaseModel):
    """
    Represents the database model for the Story item.
    """

    __tablename__ = "stories"

    age: Mapped[int] = db.Column(db.Integer)
    author: Mapped[str] = db.Column(db.String)
    title: Mapped[str] = db.Column(db.String, unique=True)
    emoji: Mapped[str] = db.Column(db.String, unique=True)
    outline: Mapped[str] = db.Column(db.String, unique=True)
    lesson: Mapped[str] = db.Column(db.String)

    sections: Mapped[list[SectionDatabaseModel]] = db.relationship()
