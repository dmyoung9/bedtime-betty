from __future__ import annotations

from abc import ABCMeta
from dataclasses import dataclass, field
from typing import Optional

import emoji as em


@dataclass
class Item(metaclass=ABCMeta):
    def __str__(self):
        return str(self.__dict__)

    @classmethod
    def prompt_type(cls):
        return f"{cls.__name__.lower()}s"

    @classmethod
    def _base_examples(cls, num):
        return [
            {key: f"{{{key}}}" for key in cls.__dataclass_fields__.keys()}
            for _ in range(num)
        ]

    @classmethod
    def examples(cls, num):
        return cls._base_examples(num)


@dataclass
class Artist(Item):
    artist_name: str
    artist_style: str

    @classmethod
    def examples(cls, num):
        examples = cls._base_examples(num)
        for example in examples:
            example["artist_style"] = ", ".join("{artist_style}" for _ in range(3))

        return examples


@dataclass
class Author(Item):
    author_name: str
    author_style: str

    @classmethod
    def examples(cls, num):
        examples = cls._base_examples(num)
        for example in examples:
            example["author_style"] = ", ".join("{author_style}" for _ in range(3))

        return examples


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

    @classmethod
    def examples(cls, num):
        examples = cls._base_examples(num)

        # give "concrete" emoji example
        for example in examples:
            example["emoji"] = "1️⃣2️⃣3️⃣4️⃣5️⃣"

        return examples


@dataclass
class Image(Item):
    url: str


@dataclass
class Lesson(Item):
    lesson: str


@dataclass
class Page(Item):
    number: int
    content: str
    image: Optional[Image] = None

    @classmethod
    def examples(cls, num):
        examples = cls._base_examples(num)

        # remove image from response, will be filled later
        for idx, example in enumerate(examples):
            example["number"] = idx + 1
            del example["image"]

        return {"total": num, "pages": examples}


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
