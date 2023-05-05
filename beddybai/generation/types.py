from dataclasses import dataclass
from typing import Literal, TypeVar, TypedDict, Optional

Item = TypeVar("Item")
Lesson = str
Title = str
Role = Literal["system", "assistant", "user"]
StoryKey = Literal["age_min", "age_max", "num", "story_theme", "story_lesson", "plural"]


class StoryInfo(TypedDict, total=False):
    age_min: int
    age_max: int
    num: int
    emoji: str
    story_theme: str
    story_lesson: str
    plural: str


@dataclass
class Artist:
    artist_name: str
    artist_style: str

    def __str__(self):
        return f"{self.artist_name} ({self.artist_style})"


@dataclass
class Author:
    author_name: str
    author_style: str

    def __str__(self):
        return f"{self.author_name} ({self.author_style})"


@dataclass
class Theme:
    emoji: str
    story_theme: str
    color: str
    text_color: str

    def __str__(self):
        return f"{self.emoji} - {self.story_theme}"


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
