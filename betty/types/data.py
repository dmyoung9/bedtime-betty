from dataclasses import dataclass
from typing import Type

from . import Item, ItemResponseModel
from .request import (
    ArtistRequestModel,
    AuthorRequestModel,
    CoverRequestModel,
    IdeaRequestModel,
    LessonRequestModel,
    SectionRequestModel,
    StoryCreateModel,
    StoryRequestModel,
)
from .validation import (
    ArtistModel,
    AuthorModel,
    CoverModel,
    IdeaModel,
    LessonModel,
    SectionModel,
    StoryModel,
)


@dataclass
class Artist(Item):
    artist_name: str
    artist_style: str

    @classmethod
    def model(cls) -> Type[ArtistModel]:
        return ArtistModel

    @classmethod
    def request_model(cls) -> Type[ArtistRequestModel]:
        return ArtistRequestModel

    @classmethod
    def response_model(cls) -> Type[ItemResponseModel[ArtistModel]]:
        return ItemResponseModel[ArtistModel]


@dataclass
class Author(Item):
    author_name: str
    author_style: str

    @classmethod
    def model(cls) -> Type[AuthorModel]:
        return AuthorModel

    @classmethod
    def request_model(cls) -> Type[AuthorRequestModel]:
        return AuthorRequestModel

    @classmethod
    def response_model(cls) -> Type[ItemResponseModel[AuthorModel]]:
        return ItemResponseModel[AuthorModel]


@dataclass
class Idea(Item):
    idea: str
    emoji: str

    @classmethod
    def model(cls) -> Type[IdeaModel]:
        return IdeaModel

    @classmethod
    def request_model(cls) -> Type[IdeaRequestModel]:
        return IdeaRequestModel

    @classmethod
    def response_model(cls) -> Type[ItemResponseModel[IdeaModel]]:
        return ItemResponseModel[IdeaModel]


@dataclass
class Lesson(Item):
    lesson: str

    @classmethod
    def model(cls) -> Type[LessonModel]:
        return LessonModel

    @classmethod
    def request_model(cls) -> Type[LessonRequestModel]:
        return LessonRequestModel

    @classmethod
    def response_model(cls) -> Type[ItemResponseModel[LessonModel]]:
        return ItemResponseModel[LessonModel]


@dataclass
class Section(Item):
    content: str

    @classmethod
    def model(cls) -> Type[SectionModel]:
        return SectionModel

    @classmethod
    def request_model(cls) -> Type[SectionRequestModel]:
        return SectionRequestModel

    @classmethod
    def response_model(cls) -> Type[ItemResponseModel[SectionModel]]:
        return ItemResponseModel[SectionModel]


@dataclass
class Cover(Item):
    author: str
    illustrator: str
    title: str
    emoji: str
    outline: str
    lesson: str

    @classmethod
    def model(cls) -> Type[CoverModel]:
        return CoverModel

    @classmethod
    def request_model(cls) -> Type[CoverRequestModel]:
        return CoverRequestModel

    @classmethod
    def response_model(cls) -> Type[ItemResponseModel[CoverModel]]:
        return ItemResponseModel[CoverModel]

    def __str__(self) -> str:
        return (
            f"# {self.emoji} {self.title}\n"
            f"written in the style of {self.author}\n"
            f"with illustrations similar to {self.illustrator}\n"
            f"{self.outline}\n"
            f"about '{self.lesson}'"
        )


@dataclass
class Story(Cover):
    @classmethod
    def model(cls) -> Type[StoryModel]:
        return StoryModel

    @classmethod
    def request_model(cls) -> Type[StoryRequestModel]:
        return StoryRequestModel

    @classmethod
    def response_model(cls) -> Type[ItemResponseModel[StoryModel]]:
        return ItemResponseModel[StoryModel]

    @classmethod
    def create_model(cls) -> Type[StoryCreateModel]:
        return StoryCreateModel
