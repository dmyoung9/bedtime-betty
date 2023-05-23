from typing import Optional, Type
from pydantic import BaseModel

from betty.types import (
    Artist,
    Author,
    Description,
    Idea,
    Image,
    Item,
    Lesson,
    Page,
    Title,
)

DEFAULT_NUM = 3
DEFAULT_AGE = 7


class ItemRequest(BaseModel):
    num: Optional[int] = DEFAULT_NUM
    age: Optional[int] = DEFAULT_AGE
    examples: Optional[list[Item]] = None

    class Config:
        extra = "forbid"


class IdeaRequest(ItemRequest):
    obj: Type[Item] = Idea
    examples: Optional[list[Item]] = Idea.examples(DEFAULT_NUM)


class LessonRequest(ItemRequest):
    obj: Type[Item] = Lesson
    examples: Optional[list[Item]] = Lesson.examples(DEFAULT_NUM)


class AuthorRequest(ItemRequest):
    obj: Type[Item] = Author
    examples: Optional[list[Item]] = Author.examples(DEFAULT_NUM)


class ArtistRequest(ItemRequest):
    obj: Type[Item] = Artist
    examples: Optional[list[Item]] = Artist.examples(DEFAULT_NUM)


class TitleRequest(ItemRequest):
    obj: Type[Item] = Title
    examples: Optional[list[Item]] = Title.examples(DEFAULT_NUM)
    story_idea: Idea
    story_lesson: Lesson
    story_author: Author


class PageRequest(ItemRequest):
    obj: Type[Item] = Page
    examples: list[Page] = Page.examples(DEFAULT_NUM)
    story_idea: Idea
    story_lesson: Lesson
    story_author: Author
    story_title: Title


class ImageRequest(ItemRequest):
    obj: Type[Item] = Image
    size: Optional[int] = 1024
    examples: Optional[list[Item]] = Image.examples(DEFAULT_NUM)
    story_artist: Artist
    story_description: Description


class DescriptionRequest(ItemRequest):
    obj: Type[Item] = Description
    examples: Optional[list[Item]] = Description.examples(DEFAULT_NUM)
    story_page: Page
    story_artist: Artist


class StoryCreateRequest(BaseModel):
    age: int
    story_idea: Idea
    story_lesson: Lesson
    story_author: Author
    story_artist: Artist
    story_title: Title
    story_pages: list[Page] = []

    class Config:
        extra = "forbid"


class ItemIdRequest(BaseModel):
    id: int
