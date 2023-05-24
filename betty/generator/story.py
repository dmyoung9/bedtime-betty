from dataclasses import asdict

import json
from typing import AsyncGenerator, Type, Union

from betty.api.openai.dalle import ImageAPI
from betty.api.openai.gpt import CompletionAPI
from . import BaseGenerator
from ..types.items import Image, Item, Page
from ..prompt import Prompt

SYSTEM_PROMPT = "bedtime_betty"
DEFAULT_NUM = 3
DEFAULT_AGE = 7


def plural(num):
    return "s" if num > 1 else ""


class StoryGenerator(BaseGenerator[Item]):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(system_prompt=SYSTEM_PROMPT, *args, **kwargs)
        self.completion_api = CompletionAPI(api_key)
        self.image_api = ImageAPI(api_key)

    def _build_info(
        self,
        *args,
        **kwargs,
    ):
        print(kwargs)
        obj = kwargs.pop("obj", Item)
        num = kwargs.get("num", DEFAULT_NUM)

        if examples := kwargs.pop("examples", []):
            write_or_continue = (
                "continue this"  # "write an" if kwargs.get(examples) else
            )
            placeholder_or_previous = "Previous items"
            if obj == Page:
                examples = [
                    e if isinstance(e, dict) else asdict(e) for e in examples["pages"]
                ]
                print(examples)
            else:
                examples = [e if isinstance(e, dict) else asdict(e) for e in examples]
        else:
            write_or_continue = "write an"
            placeholder_or_previous = "Example with placeholders"
            examples = obj.examples(num)

        info = {
            "num": num,
            "age": kwargs.get("age", DEFAULT_AGE),
            "examples": json.dumps(examples),
            "plural": plural(num),
            "write_or_continue": write_or_continue,
            "placeholder_or_previous": placeholder_or_previous,
        }

        for k, v in kwargs.items():
            if isinstance(v, Item):
                info.update(**asdict(v))
            else:
                info[k] = v

        return info

    def _build_filename(self, obj: Union[Type[Item], str]) -> str:
        return f"{obj}.md" if isinstance(obj, str) else f"{obj.__name__.lower()}s.md"

    async def _generate(self, obj, filename, system_prompt_filename, **kwargs):
        if obj == Image:
            prompt = Prompt.from_file(filename).format(kwargs)
            return await self.image_api.get_json(prompt, **kwargs)

        messages = self.completion_api.build_messages(
            filename, system_prompt_filename, **kwargs
        )
        return await self.completion_api.get_json(messages)

    async def _stream(self, obj, filename, system_prompt_filename, **kwargs):
        messages = self.completion_api.build_messages(
            filename, system_prompt_filename, **kwargs
        )
        async for item in self.completion_api.stream_json(messages):
            yield item

    async def generate_story_items(self, obj: Type[Item], **kwargs) -> list[Item]:
        return await self.generate_items(obj, **kwargs)

    async def stream_story_items(
        self, obj: Type[Item], **kwargs
    ) -> AsyncGenerator[Item, None]:
        async for item in self.stream_items(obj, **kwargs):
            yield item
