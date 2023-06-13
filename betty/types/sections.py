from __future__ import annotations

from dataclasses import dataclass
from typing import Type

from pydantic import Field

from . import Item, ItemModel, ItemRequestModel, ItemResponseModel
from .covers import CoverModel


@dataclass
class Section(Item):
    content: str


class SectionModel(ItemModel[Section]):
    content: str = Field(description="the content of this section")

    @classmethod
    def get_dataclass(cls) -> Type[Section]:
        return Section

    @classmethod
    def get_completion_request_model(cls) -> Type[SectionCompletionRequestModel]:
        return SectionCompletionRequestModel

    @classmethod
    def get_response_model(cls) -> Type[ItemResponseModel[SectionModel]]:
        return ItemResponseModel[SectionModel]


class SectionCompletionRequestModel(ItemRequestModel[SectionModel]):
    age: int
    cover: CoverModel
