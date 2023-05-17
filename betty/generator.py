from dataclasses import asdict

import json
import os
from pathlib import Path
from typing import AsyncGenerator, Optional, Union

from .api import assistant, system, user
from .prompt import Prompt
from .types import (
    API,
    Artist,
    Author,
    Idea,
    Item,
    ItemInfo,
    Lesson,
    StoryInfo,
    StoryKeys,
    Title,
    TitleInfo,
)


BASE_PATH = Path(os.getcwd())
PROMPTS_PATH = BASE_PATH / "prompts"

DEFAULT_NUM = 3
DEFAULT_AGE = 7

PROMPT_TYPES = {
    "ideas": Idea,
    "lessons": Lesson,
    "artists": Artist,
    "authors": Author,
    "titles": Title,
}


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
    def _build_item_info(
        num: int = DEFAULT_NUM,
        age: int = DEFAULT_AGE,
        examples: list[Item] = None,
        **kwargs,
    ) -> Union[ItemInfo, TitleInfo]:
        # security feature: `info` will be logged to the server console
        # **only** pass api keys via http headers
        if "api_key" in kwargs:
            print("Removing API key...")
            del kwargs["api_key"]

        k_num = kwargs.pop("num", num)
        plural = "s" if k_num > 1 else ""

        info = {
            "num": k_num,
            "age": kwargs.pop("age", age),
            "examples": json.dumps(examples or []),
            "plural": plural,
        }

        for k, v in [(k, v) for k, v in kwargs.items() if k in StoryKeys]:
            if isinstance(v, Item):
                info.update(**asdict(v))
            elif isinstance(v, dict):
                info.update(**v)
            else:
                info[k] = v

        return info

    # @staticmethod
    # def _build_story_info(
    #     story_author,
    #     story_idea,
    #     story_lesson,
    #     story_title,
    #     age: int = DEFAULT_AGE,
    #     **kwargs,
    # ) -> StoryInfo:
    #     return {
    #         **asdict(story_author),
    #         **asdict(story_idea),
    #         **asdict(story_lesson),
    #         **asdict(story_title),
    #         "age": age,
    #         **kwargs,
    #     }

    @staticmethod
    def _build_messages(prompt_filename, info):
        bedtime_betty = Prompt.from_file(PROMPTS_PATH / "bedtime_betty.md").format()
        prompt = Prompt.from_file(PROMPTS_PATH / prompt_filename).format(info)

        return [
            system(bedtime_betty),
            user(prompt),
        ]

    # @staticmethod
    # def _build_paragraphs(
    #     previous_paragraphs, info, total_paragraphs: int = DEFAULT_NUM
    # ):
    #     info["paragraph_number"] = len(previous_paragraphs) + 1
    #     info["total_paragraphs"] = total_paragraphs

    #     context = StoryGenerator._build_messages("story.md", info)

    #     paragraph_info = {
    #         "paragraph_number": 1,
    #         "total_paragraphs": total_paragraphs,
    #     }

    #     paragraph_prompt = Prompt.from_file(PROMPTS_PATH / "paragraph.md")
    #     for i in range(len(previous_paragraphs)):
    #         context.append(user(paragraph_prompt.format(paragraph_info)))
    #         context.append(assistant(json.dumps(previous_paragraphs[i])))

    #         paragraph_info["paragraph_number"] += 1

    #     context.append(user(paragraph_prompt.format(paragraph_info)))
    #     return context

    async def generate_items(
        self,
        obj: Item,
        examples: Optional[list[Item]] = None,
        **kwargs,
    ) -> list[Item]:
        info = StoryGenerator._build_item_info(
            examples=examples or obj.examples(kwargs.get("num", DEFAULT_NUM)), **kwargs
        )
        print(f"Generating {obj.prompt_type()} for {info}...")

        messages = StoryGenerator._build_messages(f"{obj.prompt_type()}.md", info)
        items = await self.api.get_json(messages)

        return [obj(**item) for item in items]

    async def stream_items(
        self,
        obj: Item,
        examples: Optional[list[Item]] = None,
        **kwargs,
    ) -> AsyncGenerator[Item, None]:
        info = StoryGenerator._build_item_info(
            examples=examples or obj.examples(kwargs.get("num", DEFAULT_NUM)), **kwargs
        )
        print(f"Streaming {obj.prompt_type()} for {info}...")

        messages = StoryGenerator._build_messages(f"{obj.prompt_type()}.md", info)
        async for item in self.api.stream_json(messages):
            yield obj(**item)

    # async def generate_image(
    #     self, story_paragraph: str, story_info: StoryInfo, **kwargs
    # ) -> str:
    #     """Generate an image based on the story paragraph and story information."""

    #     info: StoryInfo = {
    #         **story_info,  # type: ignore
    #         "story_paragraph": story_paragraph,
    #     }

    #     prompt = Prompt.from_file(PROMPTS_PATH / "dall_e_prompt.md").format_with(info)
    #     bedtime_betty = str(Prompt.from_file(PROMPTS_PATH / "bedtime_betty.md"))

    #     context = [
    #         system(bedtime_betty),
    #         user(prompt),
    #     ]
    #     print("Generating image prompt...")
    #     prompt_response = await self.api.get_completion(context)

    #     print(f"Generating image for {prompt_response}...")
    #     art = await self.api.get_image(prompt_response, **kwargs)
    #     return art

    # async def generate_story_paragraph(
    #     self,
    #     story_author,
    #     story_idea,
    #     story_lesson,
    #     story_title,
    #     age: int = DEFAULT_AGE,
    #     previous_paragraphs: Optional[list[str]] = None,
    #     total_paragraphs: int = 7,
    #     **kwargs,
    # ):
    #     print(
    #         f"Generating paragraph {len(previous_paragraphs) + 1}/{total_paragraphs}"
    #         f" of '{story_title.title}' by {story_author.author_name}..."
    #     )

    #     previous_paragraphs = previous_paragraphs or []
    #     info = StoryGenerator._build_story_info(
    #         story_author, story_idea, story_lesson, story_title, age=age, **kwargs
    #     )

    #     context = StoryGenerator._build_paragraphs(
    #         previous_paragraphs, info, total_paragraphs
    #     )

    #     return await self.api.get_json(context)
