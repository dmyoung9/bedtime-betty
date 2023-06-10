from pydantic import Field

from . import ItemModel


class ArtistModel(ItemModel):
    artist_name: str = Field(description="name of an artist")
    artist_style: str = Field(description="styles the artist is known for")


class AuthorModel(ItemModel):
    author_name: str = Field(description="name of an author")
    author_style: str = Field(description="styles the author is known for")


class IdeaModel(ItemModel):
    idea: str = Field(description="an idea for a story")
    emoji: str = Field(description="emoji that represent the idea")


class LessonModel(ItemModel):
    lesson: str = Field(description="a lesson a story could teach")


class SectionModel(ItemModel):
    content: str = Field(description="the content of this section")


class CoverModel(ItemModel):
    author: str = Field(description="author of the story")
    illustrator: str = Field(description="illustrator of the story")
    title: str = Field(description="title of the story")
    emoji: str = Field(description="emoji that convey the plot of the story")
    outline: str = Field(description="short outline of the plot of the story")
    lesson: str = Field(description="lesson the story subtly teaches")
