from typing import Optional, Type

from betty.types.data import Artist, Author, Idea, Lesson
from betty.types.items import Image, Description, Page, Title

from . import ItemModel


class ArtistModel(ItemModel[Artist]):
    obj: Type[Artist] = Artist
    artist_name: str
    artist_style: str


class AuthorModel(ItemModel[Author]):
    obj: Type[Author] = Author
    author_name: str
    author_style: str


class DescriptionModel(ItemModel[Description]):
    obj: Type[Description] = Description
    description: str


class IdeaModel(ItemModel[Idea]):
    obj: Type[Idea] = Idea
    idea: str


class ImageModel(ItemModel[Image]):
    obj: Type[Image] = Image
    url: str


class LessonModel(ItemModel[Lesson]):
    obj: Type[Lesson] = Lesson
    lesson: str


class PageModel(ItemModel[Page]):
    obj: Type[Page] = Page
    content: str
    image: Optional[ImageModel] = None


class TitleModel(ItemModel[Title]):
    obj: Type[Title] = Title
    title: str
