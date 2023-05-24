from __future__ import annotations

from abc import ABCMeta
from dataclasses import asdict, dataclass, field
import json
from typing import Optional, Union

import emoji as em


@dataclass
class Item(metaclass=ABCMeta):
    def __str__(self):
        return str(self.__dict__)

    def __dict__(self):
        return asdict(self)

    def as_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def _base_examples(
        cls, num, previous: Optional[list[Item]] = None
    ) -> dict[str, Union[int, list[Item]]]:
        data = previous or []

        data.extend(
            [
                cls(
                    **{
                        key: f"{{{key}}} {num - idx}"
                        for key in cls.__dataclass_fields__.keys()
                    }
                )
                for idx in range(num - len(data), 0, -1)
            ]
        )

        return {"total": num, "data": data}

    @classmethod
    def examples(cls, num):
        return cls._base_examples(num)


@dataclass
class Artist(Item):
    artist_name: str
    artist_style: str


@dataclass
class Author(Item):
    author_name: str
    author_style: str


@dataclass
class Description(Item):
    description: str


@dataclass
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


@dataclass
class Image(Item):
    url: str


@dataclass
class Lesson(Item):
    lesson: str


@dataclass
class Page(Item):
    content: str
    image: Optional[Image] = None


@dataclass
class Story:
    age: int
    idea: Idea
    lesson: Lesson
    author: Author
    artist: Artist
    title: Title
    pages: list[Page] = field(default_factory=list)


@dataclass
class Title(Item):
    title: str
