from dotenv import load_dotenv

load_dotenv()

import os  # noqa: E402
from typing import Literal, NotRequired, TypedDict  # noqa: E402

Lesson = str
Role = Literal["system", "assistant", "user"]


class Artist(TypedDict):
    artist: str
    artist_style: str


class Author(TypedDict):
    author: str
    author_style: str


class Config:
    def __init__(self):
        self.OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY")


class Theme(TypedDict):
    emoji: str
    story_theme: str


class Message(TypedDict):
    role: Role
    content: str


class Page(TypedDict):
    content: str
    image: NotRequired[None | str]


class Story(TypedDict):
    title: str
    pages: list[Page]


class StoryInfo(TypedDict):
    emoji: NotRequired[None | str]
    story_theme: NotRequired[None | str]
    story_lesson: NotRequired[None | str]
    author: NotRequired[None | str]
    author_style: NotRequired[None | str]
    artist: NotRequired[None | str]
    artist_style: NotRequired[None | str]
    age_min: NotRequired[None | int]
    age_max: NotRequired[None | int]
    num: NotRequired[None | int]
    story: NotRequired[None | str]


config = Config()
