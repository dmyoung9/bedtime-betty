from __future__ import annotations

from dataclasses import dataclass
from typing import Type

from pydantic import Field

from sqlalchemy.orm import Mapped

from . import Item, ItemDatabaseModel, ItemModel, ItemRequestModel, ItemResponseModel
from ..database import db


@dataclass
class Section(Item):
    content: str

    @staticmethod
    def get_item_model() -> Type[SectionModel]:
        return SectionModel

    @staticmethod
    def get_completion_request_model() -> Type[SectionCompletionRequestModel]:
        return SectionCompletionRequestModel

    @staticmethod
    def get_response_model() -> Type[ItemResponseModel[SectionModel]]:
        return ItemResponseModel[SectionModel]

    @staticmethod
    def get_database_model() -> Type[ItemDatabaseModel]:
        raise NotImplementedError()


class SectionModel(ItemModel[Section]):
    content: str = Field(description="the content of this section")


class SectionCompletionRequestModel(ItemRequestModel[SectionModel]):
    age: int
    author: str = Field(description="author of the story")
    title: str = Field(description="title of the story")
    emoji: str = Field(description="emoji that convey the plot of the story")
    outline: str = Field(description="short outline of the plot of the story")
    lesson: str = Field(description="lesson the story subtly teaches")


class SectionDatabaseModel(ItemDatabaseModel):
    __tablename__ = "sections"

    content: Mapped[str] = db.Column(db.String, unique=True)
    story_id: Mapped[int] = db.Column(db.ForeignKey("stories.id"))
