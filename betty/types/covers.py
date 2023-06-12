from __future__ import annotations

from dataclasses import dataclass
from typing import Type

from pydantic import Field

from . import Item, ItemModel, ItemRequestModel, ItemResponseModel


@dataclass
class Cover(Item):
    author: str
    illustrator: str
    title: str
    emoji: str
    outline: str
    lesson: str


class CoverModel(ItemModel[Cover]):
    author: str = Field(description="author of the story")
    illustrator: str = Field(description="illustrator of the story")
    title: str = Field(description="title of the story")
    emoji: str = Field(description="emoji that convey the plot of the story")
    outline: str = Field(description="short outline of the plot of the story")
    lesson: str = Field(description="lesson the story subtly teaches")

    @classmethod
    def get_dataclass(cls) -> Type[Cover]:
        return Cover

    @classmethod
    def get_completion_request_model(cls) -> Type[CoverCompletionRequestModel]:
        return CoverCompletionRequestModel

    @classmethod
    def get_response_model(cls) -> Type[ItemResponseModel[CoverModel]]:
        return ItemResponseModel[CoverModel]


class CoverCompletionRequestModel(ItemRequestModel[CoverModel]):
    num: int
    age: int
