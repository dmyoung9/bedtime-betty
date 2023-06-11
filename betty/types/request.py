from typing import Type
from . import ItemCreateModel, ItemRequestModel
from .validation import (
    ArtistModel,
    AuthorModel,
    CoverModel,
    IdeaModel,
    LessonModel,
    SectionModel,
    StoryModel,
)


class ArtistRequestModel(ItemRequestModel):
    num: int
    age: int
    obj: Type[ArtistModel] = ArtistModel


class AuthorRequestModel(ItemRequestModel):
    num: int
    age: int
    obj: Type[AuthorModel] = AuthorModel


class IdeaRequestModel(ItemRequestModel):
    num: int
    age: int
    obj: Type[IdeaModel] = IdeaModel


class LessonRequestModel(ItemRequestModel):
    num: int
    age: int
    obj: Type[LessonModel] = LessonModel


class SectionRequestModel(ItemRequestModel):
    age: int
    cover: CoverModel
    obj: Type[SectionModel] = SectionModel


class CoverRequestModel(ItemRequestModel):
    num: int
    age: int
    obj: Type[CoverModel] = CoverModel


class StoryRequestModel(ItemRequestModel):
    id: int
    obj: Type[StoryModel] = StoryModel


class StoryCreateModel(ItemCreateModel):
    age: int
    author: str
    illustrator: str
    title: str
    emoji: str
    outline: str
    lesson: str
    sections: list[SectionModel] = []
    obj: Type[StoryModel] = StoryModel
