from __future__ import annotations

from typing import Type

from pydantic import Field

from . import ItemModel, ItemRequestModel, ItemResponseModel
from .data import Idea


# class ArtistModel(ItemModel):
#     artist_name: str = Field(description="name of an artist")
#     artist_style: str = Field(description="styles the artist is known for")


# class AuthorModel(ItemModel):
#     author_name: str = Field(description="name of an author")
#     author_style: str = Field(description="styles the author is known for")


class IdeaModel(ItemModel[Idea]):
    idea: str = Field(description="an idea for a story")
    emoji: str = Field(description="emoji that represent the idea")

    @classmethod
    def get_dataclass(cls) -> Type[Idea]:
        return Idea

    @classmethod
    def get_completion_request_model(cls) -> Type[IdeaCompletionRequestModel]:
        return IdeaCompletionRequestModel

    @classmethod
    def get_response_model(cls) -> Type[ItemResponseModel[IdeaModel]]:
        return ItemResponseModel[IdeaModel]


class IdeaCompletionRequestModel(ItemRequestModel[IdeaModel]):
    num: int
    age: int


# class LessonModel(ItemModel):
#     lesson: str = Field(description="a lesson a story could teach")


# class SectionModel(ItemModel):
#     content: str = Field(description="the content of this section")


# class CoverModel(ItemModel):
#     author: str = Field(description="author of the story")
#     illustrator: str = Field(description="illustrator of the story")
#     title: str = Field(description="title of the story")
#     emoji: str = Field(description="emoji that convey the plot of the story")
#     outline: str = Field(description="short outline of the plot of the story")
#     lesson: str = Field(description="lesson the story subtly teaches")


# class StoryModel(CoverModel):
#     sections: list[SectionModel] = Field(description="sections of the story")
