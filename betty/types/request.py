from typing import Type
from . import ItemRequestModel
from .validation import (
    ArtistModel,
    AuthorModel,
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
    obj: Type[SectionModel] = SectionModel


class StoryRequestModel(ItemRequestModel):
    obj: Type[StoryModel] = StoryModel


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
