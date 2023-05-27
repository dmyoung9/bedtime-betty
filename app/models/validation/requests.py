from __future__ import annotations

from typing import Generic, Type
from app.models.validation.items import (
    ArtistModel,
    AuthorModel,
    DescriptionModel,
    IdeaModel,
    LessonModel,
    PageModel,
    TitleModel,
)

from betty.types import Item
from betty.types.items import (
    Artist,
    Author,
    Description,
    Idea,
    Image,
    Lesson,
    Page,
    Title,
)
from . import DEFAULT_NUM, RequestModel, T


class ItemRequestModel(RequestModel[Item], Generic[T]):
    obj: Type[Item] = Item
    num: int = DEFAULT_NUM
    age: int

    class Config:
        extra = "forbid"


class ArtistRequestModel(ItemRequestModel[Artist]):
    obj: Type[Artist] = Artist


class AuthorRequestModel(ItemRequestModel[Author]):
    obj: Type[Author] = Author


class DescriptionRequestModel(ItemRequestModel[Description]):
    obj: Type[Description] = Description
    page: PageModel
    artist: ArtistModel


class IdeaRequestModel(ItemRequestModel[Idea]):
    obj: Type[Idea] = Idea


class ImageRequestModel(ItemRequestModel[Image]):
    obj: Type[Image] = Image
    size: int = 1024
    artist: ArtistModel
    description: DescriptionModel


class LessonRequestModel(ItemRequestModel[Lesson]):
    obj: Type[Lesson] = Lesson


class PageRequestModel(ItemRequestModel[Page]):
    obj: Type[Page] = Page
    idea: IdeaModel
    lesson: LessonModel
    author: AuthorModel
    title: TitleModel


class TitleRequestModel(ItemRequestModel[Title]):
    obj: Type[Title] = Title
    idea: IdeaModel
    lesson: LessonModel
    author: AuthorModel


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
