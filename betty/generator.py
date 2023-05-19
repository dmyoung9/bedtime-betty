from dataclasses import asdict

import json
from typing import AsyncGenerator, Type, Union

from betty.api.openai.gpt import CompletionAPI
from . import BaseGenerator
from .types import Item

SYSTEM_PROMPT = "bedtime_betty"
DEFAULT_NUM = 3
DEFAULT_AGE = 7


def plural(num):
    return "s" if num > 1 else ""


class StoryGenerator(BaseGenerator[Item]):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(
            api=CompletionAPI(api_key), system_prompt=SYSTEM_PROMPT, *args, **kwargs
        )

    def _build_info(
        self,
        **kwargs,
    ):
        obj = kwargs.pop("obj", Item)
        info = {
            "num": (num := kwargs.get("num", DEFAULT_NUM)),
            "age": kwargs.get("age", DEFAULT_AGE),
            "examples": json.dumps(kwargs.get("examples", obj.examples(num))),
            "plural": plural(num),
        }

        for k, v in kwargs.items():
            if isinstance(v, Item):
                info.update(**asdict(v))
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
