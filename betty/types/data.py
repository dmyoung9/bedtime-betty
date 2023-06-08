from dataclasses import dataclass
from typing import Type

from . import Item
from .request import (
    ArtistRequestModel,
    AuthorRequestModel,
    IdeaRequestModel,
    LessonRequestModel,
    SectionRequestModel,
    StoryRequestModel,
)
from .response import (
    ArtistResponseModel,
    AuthorResponseModel,
    IdeaResponseModel,
    LessonResponseModel,
    SectionResponseModel,
    StoryResponseModel,
)
from .validation import (
    ArtistModel,
    AuthorModel,
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
    def response_model(cls) -> Type[ArtistResponseModel]:
        return ArtistResponseModel


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
    def response_model(cls) -> Type[AuthorResponseModel]:
        return AuthorResponseModel


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
    def response_model(cls) -> Type[IdeaResponseModel]:
        return IdeaResponseModel


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
    def response_model(cls) -> Type[LessonResponseModel]:
        return LessonResponseModel


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
    def response_model(cls) -> Type[SectionResponseModel]:
        return SectionResponseModel


@dataclass
class Story(Item):
    author: str
    illustrator: str
    title: str
    emoji: str
    outline: str
    lesson: str

    @classmethod
    def model(cls) -> Type[StoryModel]:
        return StoryModel

    @classmethod
    def request_model(cls) -> Type[StoryRequestModel]:
        return StoryRequestModel

    @classmethod
    def response_model(cls) -> Type[StoryResponseModel]:
        return StoryResponseModel

    @classmethod
    def plural(cls) -> str:
        return "stories"

    def __str__(self) -> str:
        return (
            f"# {self.emoji} {self.title}\n"
            f"written in the style of {self.author}\n"
            f"with illustrations similar to {self.illustrator}\n"
            f"{self.outline}\n"
            f"about '{self.lesson}'"
        )
