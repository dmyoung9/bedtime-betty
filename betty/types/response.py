from . import ItemResponseModel

from .validation import (
    ArtistModel,
    AuthorModel,
    IdeaModel,
    LessonModel,
    SectionModel,
    StoryModel,
)


class ArtistResponseModel(ItemResponseModel):
    data: list[ArtistModel]


class AuthorResponseModel(ItemResponseModel):
    data: list[AuthorModel]


class IdeaResponseModel(ItemResponseModel):
    data: list[IdeaModel]


class LessonResponseModel(ItemResponseModel):
    data: list[LessonModel]


class SectionResponseModel(ItemResponseModel):
    data: list[SectionModel]


class StoryResponseModel(ItemResponseModel):
    data: list[StoryModel]
