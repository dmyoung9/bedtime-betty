from email.generator import Generator
import os
from pathlib import Path
from typing import AsyncGenerator, Callable, Iterable, Optional, Union

import json

from .api import OpenAI, assistant, extract_json, system, user
from .prompt import Prompt
from .types import (
    API,
    Item,
    StoryInfo,
    Idea,
    Lesson,
)


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
        self.age = DEFAULT_AGE

    @staticmethod
    def _build_messages(prompt_filename, info):
        bedtime_betty = Prompt.from_file(PROMPTS_PATH / "bedtime_betty.md").format()
        prompt = Prompt.from_file(PROMPTS_PATH / prompt_filename).format(info)

        return (
            system(bedtime_betty),
            user(prompt),
        )

    async def generate_items(
        self,
        prompt_filename: str,
        examples: list[Item],
        num: int = DEFAULT_NUM,
        age: int = DEFAULT_AGE,
    ) -> list[Item]:
        info: StoryInfo = {"age": age, "num": num, "examples": json.dumps(examples)}

        print(f"Generating {prompt_filename.split('.')[0]} for {info}...")
        info["plural"] = plural(num)

        messages = StoryGenerator._build_messages(prompt_filename, info)
        response = await self.api.get_completion(messages)
        return extract_json(response)

    async def stream_items(
        self,
        prompt_filename: str,
        examples: list[Item],
        num: int = DEFAULT_NUM,
        age: int = DEFAULT_AGE,
    ) -> AsyncGenerator[Item, None]:
        info: StoryInfo = {"age": age, "num": num, "examples": json.dumps(examples)}

        print(f"Streaming {prompt_filename.split('.')[0]} for {info}...")
        info["plural"] = plural(num)

        messages = StoryGenerator._build_messages(prompt_filename, info)
        async for item in self.api.stream_json(messages):
            yield item

    async def generate_story_ideas(
        self, examples: list[Idea], num: int = 7, age: int = DEFAULT_AGE
    ) -> list[Idea]:
        ideas = await self.generate_items("story_ideas.md", examples, num, age)
        return [Idea(**idea) for idea in ideas]

    async def stream_story_ideas(
        self, examples: list[Idea], num: int = 7, age: int = DEFAULT_AGE
    ) -> AsyncGenerator[Idea, None]:
        async for idea in self.stream_items("story_ideas.md", examples, num, age):
            yield Idea(**idea)

    async def generate_story_lessons(
        self, examples: list[Lesson], num: int = 7, age: int = DEFAULT_AGE
    ) -> list[Lesson]:
        lessons = await self.generate_items("story_lessons.md", examples, num, age)
        return [Lesson(**lesson) for lesson in lessons]

    async def stream_story_lessons(
        self, examples: list[Lesson], num: int = 7, age: int = DEFAULT_AGE
    ) -> AsyncGenerator[Lesson, None]:
        async for lesson in self.stream_items("story_lessons.md", examples, num, age):
            yield Lesson(**lesson)

    # async def generate_story_lessons(
    #     self,
    #     num: int = 3,
    #     age_min: int = DEFAULT_AGE_MIN,
    #     age_max: int = DEFAULT_AGE_MAX,
    # ) -> list[Lesson]:
    #     """Generate a list of lessons for a specific story theme based on the target
    #     age range."""

    #     return await self.generate_items(
    #         num,
    #         "story_lessons.md",
    #         None,
    #         lambda response: [
    #             lesson.lower().strip("-. ") for lesson in response.splitlines()
    #         ],
    #         age_min,
    #         age_max,
    #     )

    # async def generate_story_lessons_streaming(
    #     self,
    #     num: int = 3,
    #     age_min: int = DEFAULT_AGE_MIN,
    #     age_max: int = DEFAULT_AGE_MAX,
    # ) -> list[Lesson]:
    #     """Generate a list of story lessons based on the target age range."""

    #     async for lesson in self.generate_items_streaming(
    #         num, "story_lessons.md", None, age_min, age_max, separator=r"\n"
    #     ):
    #         yield Lesson(lesson)

    # async def generate_author_styles(
    #     self,
    #     num: int = 10,
    #     age_min: int = DEFAULT_AGE_MIN,
    #     age_max: int = DEFAULT_AGE_MAX,
    # ) -> list[Author]:
    #     """Generate a list of author styles based on the target age range."""

    #     return await self.generate_items(
    #         num,
    #         "author_styles.md",
    #         None,
    #         lambda response: [
    #             Author(
    #                 author_name=(author := i.strip('"-. ').split(":"))[0].rstrip(),
    #                 author_style=author[1].lower().lstrip(),
    #             )
    #             for i in response.splitlines()
    #         ],
    #         age_min,
    #         age_max,
    #     )

    # async def generate_artist_styles(
    #     self,
    #     num: int = 10,
    #     age_min: int = DEFAULT_AGE_MIN,
    #     age_max: int = DEFAULT_AGE_MAX,
    # ) -> list[Artist]:
    #     """Generate a list of artist styles based on the target age range."""

    #     return await self.generate_items(
    #         num,
    #         "artist_styles.md",
    #         None,
    #         lambda response: [
    #             Artist(
    #                 artist_name=(artist := i.strip('"-. ').split(":"))[0].rstrip(),
    #                 artist_style=artist[1].lower().lstrip(),
    #             )
    #             for i in response.splitlines()
    #         ],
    #         age_min,
    #         age_max,
    #     )

    # async def generate_story_titles(
    #     self,
    #     story_theme: str,
    #     story_lesson: str,
    #     num: int = 1,
    #     age_min: int = DEFAULT_AGE_MIN,
    #     age_max: int = DEFAULT_AGE_MAX,
    #     **kwargs,
    # ) -> list[Title]:
    #     """Generate a title for the given story based on its content."""

    #     return await self.generate_items(
    #         num,
    #         "story_titles.md",
    #         {"story_theme": story_theme, "story_lesson": story_lesson},
    #         lambda response: [title.strip('"-. ') for title in response.splitlines()],
    #         age_min,
    #         age_max,
    #     )

    async def generate_image(
        self, story_paragraph: str, story_info: StoryInfo, **kwargs
    ) -> str:
        """Generate an image based on the story paragraph and story information."""

        info: StoryInfo = {
            **story_info,  # type: ignore
            "story_paragraph": story_paragraph,
        }

        prompt = Prompt.from_file(PROMPTS_PATH / "dall_e_prompt.md").format_with(info)
        bedtime_betty = str(Prompt.from_file(PROMPTS_PATH / "bedtime_betty.md"))

        context = [
            system(bedtime_betty),
            user(prompt),
        ]
        print("Generating image prompt...")
        prompt_response = await self.api.get_completion(context)

        print(f"Generating image for {prompt_response}...")
        art = await self.api.get_image(prompt_response, **kwargs)
        return art

    async def generate_story_paragraph(
        self,
        info: StoryInfo,
        previous_paragraphs: Optional[list[str]] = None,
        total_paragraphs: int = 7,
    ):
        previous_paragraphs = previous_paragraphs or []

        info["total_paragraphs"] = total_paragraphs
        story_prompt = Prompt.from_file(PROMPTS_PATH / "story.md").format_with(info)
        paragraph_prompt = Prompt.from_file(PROMPTS_PATH / "paragraph.md")
        bedtime_betty = str(Prompt.from_file(PROMPTS_PATH / "bedtime_betty.md"))

        context = [system(bedtime_betty), user(story_prompt)]

        if len(previous_paragraphs) >= total_paragraphs:
            paragraph_info = {
                "paragraph_number": len(previous_paragraphs) + 1,
                "total_paragraphs": total_paragraphs,
            }
            apology_prompt = Prompt.from_file(
                PROMPTS_PATH / "too_many_pages.md"
            ).format_with(paragraph_info)

            context.append(user(apology_prompt))
            return paragraph_info["paragraph_number"], await self.api.get_completion(
                context
            )

        paragraph_info = {
            "paragraph_number": 1,
            "total_paragraphs": total_paragraphs,
        }

        for i in range(len(previous_paragraphs)):
            context.append(user(paragraph_prompt.format_with(paragraph_info)))
            context.append(assistant(previous_paragraphs[i]))

            paragraph_info["paragraph_number"] += 1

        context.append(user(paragraph_prompt.format_with(paragraph_info)))

        return (await self.api.get_completion(context)).strip()

    async def generate_story_paragraphs_streaming(
        self,
        info: StoryInfo,
        total_paragraphs: int = 7,
    ):
        previous_paragraphs = []
        for _ in range(total_paragraphs):
            paragraph = await self.generate_story_paragraph(
                info, previous_paragraphs, total_paragraphs
            )
            previous_paragraphs.append(paragraph)
            yield paragraph
