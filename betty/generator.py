from dataclasses import asdict

import json
import os
from pathlib import Path
from typing import AsyncGenerator, Iterable, Optional

from .api import system, user
from .prompt import Prompt
from .types import API, Item, ItemInfo, Message


BASE_PATH = Path(os.getcwd())
PROMPTS_PATH = BASE_PATH / "prompts"

DEFAULT_NUM = 3
DEFAULT_AGE = 7


def plural(num):
    return "s" if num > 1 else ""


class StoryGenerator:
    """
    A class for generating stories, titles, themes, lessons, authors, artists,
    and images using OpenAI's API. Each story is tailored for a specific age
    range based on the user inputs.
    """

    def __init__(self, api: API):
        """Initialize a new instance of the StoryGenerator class."""
        self.api = api

    @staticmethod
    def _build_info(
        num: int = DEFAULT_NUM,
        age: int = DEFAULT_AGE,
        examples: list[Item] = None,
        **kwargs,
    ) -> ItemInfo:
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

    @staticmethod
    def _build_messages(prompt_filename: str, **kwargs) -> Iterable[Message]:
        bedtime_betty = Prompt.from_file(PROMPTS_PATH / "bedtime_betty.md").format()
        prompt = Prompt.from_file(PROMPTS_PATH / prompt_filename).format(kwargs)

        return [
            system(bedtime_betty),
            user(prompt),
        ]

    async def generate_items(
        self,
        obj: Item,
        examples: Optional[list[Item]] = None,
        **kwargs,
    ) -> list[Item]:
        info = StoryGenerator._build_info(
            examples=examples or obj.examples(kwargs.get("num", DEFAULT_NUM)), **kwargs
        )
        print(f"Generating {obj.prompt_type()} for {info}...")

        messages = StoryGenerator._build_messages(f"{obj.prompt_type()}.md", **info)
        items = await self.api.get_json(messages)

        return [obj(**item) for item in items]

    async def stream_items(
        self,
        obj: Item,
        examples: Optional[list[Item]] = None,
        **kwargs,
    ) -> AsyncGenerator[Item, None]:
        info = StoryGenerator._build_info(
            examples=examples or obj.examples(kwargs.get("num", DEFAULT_NUM)), **kwargs
        )
        print(f"Streaming {obj.prompt_type()} for {info}...")

        messages = StoryGenerator._build_messages(f"{obj.prompt_type()}.md", **info)
        async for item in self.api.stream_json(messages):
            yield obj(**item)
