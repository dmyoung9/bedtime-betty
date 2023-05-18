from dataclasses import asdict
import json

from typing import AsyncGenerator, Optional, Type, Union

from betty.api import OpenAI
from . import BaseGenerator
from .types import Artist, Author, Idea, Item, Lesson, Paragraph, Scene, Title

SYSTEM_PROMPT = "bedtime_betty"
DEFAULT_NUM = 3
DEFAULT_AGE = 7


def plural(num):
    return "s" if num > 1 else ""


class StoryGenerator(BaseGenerator[Item]):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(
            api=OpenAI(api_key), system_prompt=SYSTEM_PROMPT, *args, **kwargs
        )

    def _build_info(
        self,
        examples: Optional[list[Item]] = None,
        **kwargs,
    ):
        num = kwargs.pop("num")

        info = {
            "num": num,
            "age": kwargs.pop("age"),
            "examples": json.dumps(examples or []),
            "plural": plural(num),
        }

        for k, v in kwargs.items():
            if isinstance(v, Item):
                info.update(**asdict(v))
            elif isinstance(v, dict):
                info.update(**v)
            else:
                info[k] = v

        return info

    def _build_filename(self, obj: Union[Type[Item], str]) -> str:
        return f"{obj}.md" if isinstance(obj, str) else f"{obj.__name__.lower()}s.md"

    async def generate_story_items(self, obj: Type[Item], **kwargs) -> list[Item]:
        return await self.generate_items(obj, **kwargs)

    async def stream_story_items(
        self, obj: Type[Item], **kwargs
    ) -> AsyncGenerator[Item, None]:
        async for item in self.stream_items(obj, **kwargs):
            yield item

    async def generate_story_ideas(self, **kwargs) -> list[Item]:
        return await self.generate_items(Idea, **kwargs)

    async def stream_story_ideas(self, **kwargs) -> AsyncGenerator[Item, None]:
        async for idea in self.stream_items(Idea, **kwargs):
            yield idea

    async def generate_story_lessons(self, **kwargs) -> list[Item]:
        return await self.generate_items(Lesson, **kwargs)

    async def stream_story_lessons(self, **kwargs) -> AsyncGenerator[Item, None]:
        async for lesson in self.stream_items(Lesson, **kwargs):
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
