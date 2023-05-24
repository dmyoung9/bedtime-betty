from __future__ import annotations

from typing import Generic, Optional, Type

from pydantic import validator

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
    examples: Optional[list[T]] = None

    class Config:
        extra = "forbid"


class ArtistRequestModel(ItemRequestModel[Artist]):
    obj: Type[Artist] = Artist

    @validator("examples", always=True)
    def set_examples(cls, v, values, **kwargs):
        return Artist.examples(values["num"])


class AuthorRequestModel(ItemRequestModel[Author]):
    obj: Type[Author] = Author

    @validator("examples", always=True)
    def set_examples(cls, v, values, **kwargs):
        return Author.examples(values["num"])


class DescriptionRequestModel(ItemRequestModel[Description]):
    obj: Type[Description] = Description
    page: Page
    artist: Artist

    @validator("examples", always=True)
    def set_examples(cls, v, values, **kwargs):
        return Description.examples(values["num"])


class IdeaRequestModel(ItemRequestModel[Idea]):
    obj: Type[Idea] = Idea

    @validator("examples", always=True)
    def set_examples(cls, v, values, **kwargs):
        return Idea.examples(values["num"])


class ImageRequestModel(ItemRequestModel[Image]):
    obj: Type[Image] = Image
    size: int = 1024
    artist: Artist
    description: Description

    @validator("examples", always=True)
    def set_examples(cls, v, values, **kwargs):
        return Image.examples(values["num"])


class LessonRequestModel(ItemRequestModel[Lesson]):
    obj: Type[Lesson] = Lesson

    @validator("examples", always=True)
    def set_examples(cls, v, values, **kwargs):
        return Lesson.examples(values["num"])


class PageRequestModel(ItemRequestModel[Page]):
    obj: Type[Page] = Page
    idea: Idea
    lesson: Lesson
    author: Author
    title: Title
    examples: Optional[list[Page]] = None

    @validator("examples", always=True)
    def set_examples(cls, v, values, **kwargs):
        return Page.examples(values["num"])


class TitleRequestModel(ItemRequestModel[Title]):
    obj: Type[Title] = Title
    idea: Idea
    lesson: Lesson
    author: Author

    @validator("examples", always=True)
    def set_examples(cls, v, values, **kwargs):
        return Title.examples(values["num"])


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
