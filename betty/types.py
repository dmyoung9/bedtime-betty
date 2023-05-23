from __future__ import annotations
from abc import ABCMeta

from dataclasses import dataclass
from typing import Optional

import emoji as em

DEFAULT_NUM = 3


@dataclass
class Item(metaclass=ABCMeta):
    def __str__(self):
        return str(self.__dict__)

    @classmethod
    def prompt_type(cls):
        return f"{cls.__name__.lower()}s"

    @classmethod
    def _base_examples(cls, num: int = DEFAULT_NUM):
        return [
            {key: f"{{{key}}}" for key in cls.__dataclass_fields__.keys()}
            for _ in range(int((num / 2) + 1))
        ]

    @classmethod
    def examples(cls, num: int = DEFAULT_NUM):
        return cls._base_examples(num)


@dataclass
class Artist(Item):
    artist_name: str
    artist_style: str

    @classmethod
    def examples(cls, num: int = DEFAULT_NUM):
        examples = cls._base_examples(num)
        for example in examples:
            example["artist_style"] = ", ".join("{{artist_style}}" for _ in range(3))

        return examples


@dataclass
class Author(Item):
    author_name: str
    author_style: str

    @classmethod
    def examples(cls, num: int = DEFAULT_NUM):
        examples = cls._base_examples(num)
        for example in examples:
            example["author_style"] = ", ".join("{{author_style}}" for _ in range(3))

        return examples


@dataclass
class Idea(Item):
    idea: str
    emoji: str

    def __init__(self, idea: str, emoji: str = "", emojis: str = ""):
        self.idea = idea
        self.emoji = emoji or emojis

        if emoji_list := em.emoji_list(idea):
            self.idea, self.emoji = (
                self.idea[: emoji_list[0]["match_start"]],
                self.idea[emoji_list[0]["match_start"] :],
            )

    @classmethod
    def examples(cls, num: int = DEFAULT_NUM):
        examples = cls._base_examples(num)
        for example in examples:
            example["idea"] = "{{idea}}"
            example["emoji"] = "1️⃣2️⃣3️⃣4️⃣5️⃣"

        return examples


@dataclass
class Lesson(Item):
    lesson: str


@dataclass
class Title(Item):
    title: str


@dataclass
class Page(Item):
    number: int
    total: int
    content: str
    image: Optional[str] = None

    @classmethod
    def examples(cls, num: int = DEFAULT_NUM):
        examples = cls._base_examples(num)
        for idx, example in enumerate(examples):
            example["number"] = idx + 1
            example["total"] = num
            del example["image"]

        return examples


@dataclass
class Story:
    age: int
    story_idea: Idea
    story_lesson: Lesson
    story_author: Author
    story_artist: Artist
    story_title: Title
    pages: Optional[list[Page]] = None


@dataclass
class Image(Item):
    url: str


@dataclass
class Description(Item):
    content: str
