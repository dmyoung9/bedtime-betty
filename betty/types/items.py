from __future__ import annotations

from dataclasses import field
from typing import Optional

import emoji as em

from . import Item


class Artist(Item):
    artist_name: str
    artist_style: str


class Author(Item):
    author_name: str
    author_style: str


class Description(Item):
    description: str


class Idea(Item):
    idea: str
    emoji: str

    def __init__(self, *args, **kwargs):
        self.idea, self.emoji = Idea.parse_emoji(*args, **kwargs)

    @staticmethod
    def parse_emoji(*args, **kwargs):
        idea = kwargs["idea"]
        emoji = kwargs.get("emoji", kwargs.get("emojis"))

        return (
            (
                idea[: emoji_list[0]["match_start"]],
                idea[emoji_list[0]["match_start"] :],
            )
            if (emoji_list := em.emoji_list(idea))
            else (idea, emoji)
        )


class Image(Item):
    url: str


class Lesson(Item):
    lesson: str


class Page(Item):
    content: str
    image: Optional[Image] = None


class Story:
    age: int
    idea: Idea
    lesson: Lesson
    author: Author
    artist: Artist
    title: Title
    pages: list[Page] = field(default_factory=list)


class Title(Item):
    title: str
