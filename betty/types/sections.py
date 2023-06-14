from __future__ import annotations

from dataclasses import dataclass
from typing import Type

from pydantic import Field

from sqlalchemy.orm import Mapped

from ..database import db
from . import Item, ItemDatabaseModel, ItemModel, ItemRequestModel, ItemResponseModel


@dataclass
class Section(Item):
    """
    Represents a section of a story.

    Attributes:
        content (str): The content of the section.
    """

    content: str

    @staticmethod
    def get_item_model() -> Type[SectionModel]:
        """
        Get the Pydantic model for a Section item.

        Returns:
            Type[SectionModel]: The Pydantic model for a Section item.
        """
        return SectionModel

    @staticmethod
    def get_completion_request_model() -> Type[SectionCompletionRequestModel]:
        """
        Get the Pydantic model for a completion request of a Section item.

        Returns:
            Type[SectionCompletionRequestModel]: The Pydantic model for a completion request of a Section item.
        """
        return SectionCompletionRequestModel

    @staticmethod
    def get_response_model() -> Type[ItemResponseModel[SectionModel]]:
        """
        Get the Pydantic model for the response from a completion of a Section item.

        Returns:
            Type[ItemResponseModel[SectionModel]]: The Pydantic model for the response from a completion of a Section item.
        """
        return ItemResponseModel[SectionModel]

    @staticmethod
    def get_database_model() -> Type[ItemDatabaseModel]:
        """
        Get the SQLAlchemy database model for a Section item.

        Returns:
            Type[ItemDatabaseModel]: The SQLAlchemy database model for a Section item.
        """
        return SectionDatabaseModel


class SectionModel(ItemModel[Section]):
    """
    Pydantic model for a Section item.

    Attributes:
        content (str): The content of the section.
    """

    content: str = Field(description="the content of this section")


class SectionCompletionRequestModel(ItemRequestModel[SectionModel]):
    """
    Pydantic model for a completion request of a Section item.

    Attributes:
        age (int): The age of the user.
        author (str): The author of the story.
        title (str): The title of the story.
        emoji (str): The emoji that conveys the plot of the story.
        outline (str): The short outline of the plot of the story.
        lesson (str): The lesson the story subtly teaches.
    """

    age: int
    author: str = Field(description="author of the story")
    title: str = Field(description="title of the story")
    emoji: str = Field(description="emoji that convey the plot of the story")
    outline: str = Field(description="short outline of the plot of the story")
    lesson: str = Field(description="lesson the story subtly teaches")


class SectionDatabaseModel(ItemDatabaseModel):
    """
    SQLAlchemy database model for a Section item.

    Attributes:
        __tablename__ (str): The name of the database table.
        serialize_only (tuple): The columns to be serialized.
        content (Mapped[str]): The content of the section.
        story_id (Mapped[int]): The foreign key to the parent story.
    """

    __tablename__ = "sections"
    serialize_only = ("content",)

    content: Mapped[str] = db.Column(db.String, unique=True)
    story_id: Mapped[int] = db.Column(db.ForeignKey("stories.id"))
