from typing import Type
from . import ItemRequestModel
from .validation import (
    ArtistModel,
    AuthorModel,
    IdeaModel,
    LessonModel,
    SectionModel,
    CoverModel,
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


# class StoryCreateRequest(BaseModel):
#     age: int
#     story_idea: Idea
#     story_lesson: Lesson
#     story_author: Author
#     story_artist: Artist
#     story_title: Title
#     story_pages: list[Page] = []

#     class Config:
#         extra = "forbid"
