from dataclasses import dataclass
from typing import Type

from . import Item
from .response import (
    ArtistResponseModel,
    AuthorResponseModel,
    IdeaResponseModel,
    LessonResponseModel,
    StoryResponseModel,
)
from .validation import ArtistModel, AuthorModel, IdeaModel, LessonModel, StoryModel


@dataclass
class Artist(Item):
    artist_name: str
    artist_style: str

    @classmethod
    def model(cls) -> Type[ArtistModel]:
        return ArtistModel

    @classmethod
    def response_model(cls) -> Type[ArtistResponseModel]:
        return ArtistResponseModel


@dataclass
class Author(Item):
    author_name: str
    author_style: str

    @classmethod
    def response_model(cls) -> Type[AuthorResponseModel]:
        return AuthorResponseModel

    @classmethod
    def model(cls) -> Type[AuthorModel]:
        return AuthorModel


@dataclass
class Idea(Item):
    idea: str
    emoji: str

    @classmethod
    def response_model(cls) -> Type[IdeaResponseModel]:
        return IdeaResponseModel

    @classmethod
    def model(cls) -> Type[IdeaModel]:
        return IdeaModel


@dataclass
class Lesson(Item):
    lesson: str

    @classmethod
    def response_model(cls) -> Type[LessonResponseModel]:
        return LessonResponseModel

    @classmethod
    def model(cls) -> Type[LessonModel]:
        return LessonModel


@dataclass
class Story(Item):
    author: str
    illustrator: str
    title: str
    emoji: str
    outline: str
    lesson: str

    @classmethod
    def plural(cls) -> str:
        return "stories"

    @classmethod
    def response_model(cls) -> Type[StoryResponseModel]:
        return StoryResponseModel

    @classmethod
    def model(cls) -> Type[StoryModel]:
        return StoryModel

    def __str__(self) -> str:
        return (
            f"# {self.emoji} {self.title}\n"
            f"written in the style of {self.author}\n"
            f"with illustrations similar to {self.illustrator}\n"
            f"{self.outline}\n"
            f"about '{self.lesson}'"
        )
