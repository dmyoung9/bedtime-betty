from dataclasses import dataclass
from typing import Literal, TypeVar, TypedDict, Optional
import json

Title = str
Role = Literal["system", "assistant", "user"]
StoryKey = Literal["age", "num", "idea", "story_lesson", "plural"]


class API:
    pass


class StoryInfo(TypedDict, total=False):
    age: int
    num: int
    emoji: str
    idea: str
    story_lesson: str
    plural: str


@dataclass
class Item:
    def __str__(self):
        return json.dumps(self.__dict__)


@dataclass
class Artist:
    artist_name: str
    artist_style: str


@dataclass
class Author:
    author_name: str
    author_style: str


@dataclass
class Idea(Item):
    idea: str
    emoji: str


@dataclass
class Lesson(Item):
    lesson: str


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
