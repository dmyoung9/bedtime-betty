from __future__ import annotations

from dataclasses import dataclass
from typing import Type

from pydantic import Field

from . import Item, ItemModel, ItemRequestModel, ItemResponseModel


@dataclass
class Section(Item):
    content: str

    @classmethod
    def get_item_model(cls) -> Type[SectionModel]:
        return SectionModel

    @classmethod
    def get_completion_request_model(cls) -> Type[SectionCompletionRequestModel]:
        return SectionCompletionRequestModel

    @classmethod
    def get_response_model(cls) -> Type[ItemResponseModel[SectionModel]]:
        return ItemResponseModel[SectionModel]


class SectionModel(ItemModel[Section]):
    content: str = Field(description="the content of this section")


class SectionCompletionRequestModel(ItemRequestModel[SectionModel]):
    age: int
    author: str = Field(description="author of the story")
    title: str = Field(description="title of the story")
    emoji: str = Field(description="emoji that convey the plot of the story")
    outline: str = Field(description="short outline of the plot of the story")
    lesson: str = Field(description="lesson the story subtly teaches")
