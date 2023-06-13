from __future__ import annotations

from dataclasses import dataclass
from typing import Type

from pydantic import Field

from . import Item, ItemModel, ItemRequestModel, ItemResponseModel
from .sections import SectionModel


@dataclass
class Story(Item):
    age: int
    author: str
    title: str
    emoji: str
    outline: str
    lesson: str

    @classmethod
    def get_item_model(cls) -> Type[StoryModel]:
        return StoryModel

    @classmethod
    def get_completion_request_model(cls) -> Type[ItemRequestModel[ItemModel]]:
        raise NotImplementedError()

    @classmethod
    def get_response_model(cls) -> Type[ItemResponseModel[StoryModel]]:
        return ItemResponseModel[StoryModel]


class StoryModel(ItemModel[Story]):
    age: int
    author: str = Field(description="author of the story")
    title: str = Field(description="title of the story")
    emoji: str = Field(description="emoji that convey the plot of the story")
    outline: str = Field(description="short outline of the plot of the story")
    lesson: str = Field(description="lesson the story subtly teaches")

    sections: list[SectionModel] = []
