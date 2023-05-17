from __future__ import annotations
from abc import ABCMeta

from dataclasses import dataclass
from typing import Literal, TypedDict, Optional

import emoji as em

Role = Literal["system", "assistant", "user"]
StoryKeys = [
    "age",
    "num",
    "plural",
    "examples",
    "story_idea",
    "story_lesson",
    "story_author",
    "story_artist",
    "story_title",
    "story_paragraph",
]


class API:
    pass


class StoryInfo(TypedDict, total=False):
    age: int
    num: int
    emoji: str
    idea: str
    lesson: str
    plural: str


class ItemInfo(TypedDict):
    num: int
    age: int
    plural: str
    examples: str  # examples is an array of `Item` objects, as a JSON


class TitleInfo(ItemInfo):
    idea: str
    lesson: str


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
            dict.fromkeys(cls.__dataclass_fields__.keys(), "...")
            for _ in range(int((num / 2) + 1))
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
            example["artist_style"] = "..., ..., ..."

        return examples


@dataclass
class Author(Item):
    author_name: str
    author_style: str

    @classmethod
    def examples(cls, num):
        examples = cls._base_examples(num)
        for example in examples:
            example["author_style"] = "..., ..., ..."

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
    def examples(cls, num):
        examples = cls._base_examples(num)
        for example in examples:
            example["idea"] = "story idea"
            example["emoji"] = "1️⃣2️⃣3️⃣"

        return examples


@dataclass
class Lesson(Item):
    lesson: str


@dataclass
class Title(Item):
    title: str


@dataclass
class Paragraph(Item):
    content: str


@dataclass
class Scene(Item):
    description: str


class Message(TypedDict):
    role: Role
    content: str


@dataclass
class Page:
    content: str
    image: Optional[None | str]


@dataclass
class Story:
    title: str
    pages: list[Page]
