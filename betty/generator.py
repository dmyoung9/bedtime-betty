from dataclasses import asdict
import json

from typing import AsyncGenerator, Optional
from . import BaseGenerator
from .types import Artist, Author, Idea, Item, Lesson, Paragraph, Scene, Title

DEFAULT_NUM = 3
DEFAULT_AGE = 7


def plural(num):
    return "s" if num > 1 else ""


class StoryGenerator(BaseGenerator[Item]):
    def _build_info(
        self,
        num: int = DEFAULT_NUM,
        age: int = DEFAULT_AGE,
        examples: Optional[list[Item]] = None,
        **kwargs,
    ):
        k_num = kwargs.pop("num", num)

        info = {
            "num": k_num,
            "age": kwargs.pop("age", age),
            "examples": json.dumps(examples or []),
            "plural": plural(k_num),
        }

        for k, v in kwargs.items():
            if isinstance(v, Item):
                info.update(**asdict(v))
            elif isinstance(v, dict):
                info.update(**v)
            else:
                info[k] = v

        return info

    def _build_filename(self, obj: Item) -> str:
        return f"{type(obj).__name__.lower()}s.md"

    async def stream_story_ideas(self, **kwargs) -> AsyncGenerator[Item, None]:
        examples = kwargs.get("examples") or Idea.examples(
            kwargs.get("num", DEFAULT_NUM)
        )

        async for idea in self.stream_items(Idea, examples=examples, **kwargs):
            yield idea

    async def stream_story_lessons(self, **kwargs) -> AsyncGenerator[Item, None]:
        examples = kwargs.get("examples") or Lesson.examples(
            kwargs.get("num", DEFAULT_NUM)
        )

        async for lesson in self.stream_items(Lesson, examples=examples, **kwargs):
            yield lesson

    async def stream_story_authors(self, **kwargs) -> AsyncGenerator[Item, None]:
        examples = kwargs.get("examples") or Author.examples(
            kwargs.get("num", DEFAULT_NUM)
        )

        async for author in self.stream_items(Author, examples=examples, **kwargs):
            yield author

    async def stream_story_artists(self, **kwargs) -> AsyncGenerator[Item, None]:
        examples = kwargs.get("examples") or Artist.examples(
            kwargs.get("num", DEFAULT_NUM)
        )

        async for artist in self.stream_items(Artist, examples=examples, **kwargs):
            yield artist

    async def stream_story_titles(self, **kwargs) -> AsyncGenerator[Item, None]:
        examples = kwargs.get("examples") or Title.examples(
            kwargs.get("num", DEFAULT_NUM)
        )

        async for title in self.stream_items(Title, examples=examples, **kwargs):
            yield title

    async def stream_story_paragraphs(self, **kwargs) -> AsyncGenerator[Item, None]:
        examples = kwargs.get("examples") or Paragraph.examples(
            kwargs.get("num", DEFAULT_NUM)
        )

        async for paragraph in self.stream_items(
            Paragraph, examples=examples, **kwargs
        ):
            yield paragraph

    async def stream_story_scenes(self, **kwargs) -> AsyncGenerator[Item, None]:
        examples = kwargs.get("examples") or Scene.examples(
            kwargs.get("num", DEFAULT_NUM)
        )

        async for scene in self.stream_items(Scene, examples=examples, **kwargs):
            yield scene
