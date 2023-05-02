import os
from pathlib import Path
from typing import Callable, Iterable, Optional, Union

import yaml

from .api import OpenAI, assistant, system, user
from .prompt import Prompt
from .types import (
    Artist,
    Author,
    Item,
    Message,
    StoryInfo,
    Theme,
    Lesson,
    Title,
)


BASE_PATH = Path(os.getcwd())
PROMPTS_PATH = BASE_PATH / "prompts"

# Ages when it is most influential to share bedtime stories with your kids!
DEFAULT_AGE_MIN = 2
DEFAULT_AGE_MAX = 7


class StoryGenerator:
    """
    A class for generating stories, titles, themes, lessons, authors, artists,
    and images using OpenAI's API. Each story is tailored for a specific age
    range based on the user inputs.
    """

    def __init__(self, api_key: str):
        """Initialize a new instance of the StoryGenerator class."""
        self.api = OpenAI(api_key)
        self.age_min = DEFAULT_AGE_MIN
        self.age_max = DEFAULT_AGE_MAX

    async def generate_items(
        self,
        num: int,
        prompt_filename: str,
        extra: Optional[StoryInfo] = None,
        process_response: Optional[
            Callable[
                [str],
                Union[
                    list[Title], list[Theme], list[Lesson], list[Author], list[Artist]
                ],
            ]
        ] = None,
        age_min: int = DEFAULT_AGE_MIN,
        age_max: int = DEFAULT_AGE_MAX,
    ) -> list[Item]:
        """Generate a list of items based on the target age range, prompt file,
        and processing function."""

        info: StoryInfo = {
            "age_min": age_min,
            "age_max": age_max,
            "num": num,
            "plural": "s" if num > 1 else "",
        }

        if extra is not None:
            info.update(extra)

        prompt = Prompt.from_file(PROMPTS_PATH / prompt_filename).format_with(info)
        bedtime_betty = Prompt.from_file(PROMPTS_PATH / "bedtime_betty.md").format_with(
            {}
        )
        messages = (system(bedtime_betty), user(prompt))

        print(f"Generating {prompt_filename.split('.')[0]} for {info}...")
        response = await self.api.get_completion(messages)

        return process_response(response) if process_response is not None else response

    async def generate_items_streaming(
        self,
        num: int,
        prompt_filename: str,
        extra: Optional[StoryInfo] = None,
        age_min: int = DEFAULT_AGE_MIN,
        age_max: int = DEFAULT_AGE_MAX,
        separator: str = r"\n\n",
    ) -> list[Item]:
        """Generate a list of items based on the target age range, prompt file,
        and processing function."""

        info: StoryInfo = {
            "age_min": age_min,
            "age_max": age_max,
            "num": num,
            "plural": "s" if num > 1 else "",
        }

        if extra is not None:
            info.update(extra)

        prompt = Prompt.from_file(PROMPTS_PATH / prompt_filename).format_with(info)
        bedtime_betty = Prompt.from_file(PROMPTS_PATH / "bedtime_betty.md").format_with(
            {}
        )

        messages = (system(bedtime_betty), user(prompt))

        print(user(prompt))
        async for item in self.api.stream_yaml(messages, separator=separator):
            yield item

    async def generate_story_themes(
        self,
        num: int = 3,
        age_min: int = DEFAULT_AGE_MIN,
        age_max: int = DEFAULT_AGE_MAX,
    ) -> list[Theme]:
        """Generate a list of story themes based on the target age range."""

        return await self.generate_items(
            num,
            "story_themes.md",
            None,
            lambda response: [
                Theme(**obj) for obj in yaml.safe_load(response.strip("`"))
            ],
            age_min,
            age_max,
        )

    async def generate_story_themes_streaming(
        self,
        num: int = 3,
        age_min: int = DEFAULT_AGE_MIN,
        age_max: int = DEFAULT_AGE_MAX,
    ) -> list[Theme]:
        """Generate a list of story themes based on the target age range."""

        async for theme in self.generate_items_streaming(
            num,
            "story_themes.md",
            None,
            age_min,
            age_max,
            separator=r"\n\n",
        ):
            yield theme

    async def generate_story_lessons(
        self,
        num: int = 3,
        age_min: int = DEFAULT_AGE_MIN,
        age_max: int = DEFAULT_AGE_MAX,
    ) -> list[Lesson]:
        """Generate a list of lessons for a specific story theme based on the target
        age range."""

        return await self.generate_items(
            num,
            "story_lessons.md",
            None,
            lambda response: [
                lesson.lower().strip("-. ") for lesson in response.splitlines()
            ],
            age_min,
            age_max,
        )

    async def generate_story_lessons_streaming(
        self,
        num: int = 3,
        age_min: int = DEFAULT_AGE_MIN,
        age_max: int = DEFAULT_AGE_MAX,
    ) -> list[Lesson]:
        """Generate a list of story lessons based on the target age range."""

        async for lesson in self.generate_items_streaming(
            num, "story_lessons.md", None, age_min, age_max, separator=r"\n"
        ):
            yield Lesson(lesson)

    async def generate_author_styles(
        self,
        num: int = 10,
        age_min: int = DEFAULT_AGE_MIN,
        age_max: int = DEFAULT_AGE_MAX,
    ) -> list[Author]:
        """Generate a list of author styles based on the target age range."""

        return await self.generate_items(
            num,
            "author_styles.md",
            None,
            lambda response: [
                Author(
                    author_name=(author := i.strip('"-. ').split(":"))[0].rstrip(),
                    author_style=author[1].lower().lstrip(),
                )
                for i in response.splitlines()
            ],
            age_min,
            age_max,
        )

    async def generate_artist_styles(
        self,
        num: int = 10,
        age_min: int = DEFAULT_AGE_MIN,
        age_max: int = DEFAULT_AGE_MAX,
    ) -> list[Artist]:
        """Generate a list of artist styles based on the target age range."""

        return await self.generate_items(
            num,
            "artist_styles.md",
            None,
            lambda response: [
                Artist(
                    artist_name=(artist := i.strip('"-. ').split(":"))[0].rstrip(),
                    artist_style=artist[1].lower().lstrip(),
                )
                for i in response.splitlines()
            ],
            age_min,
            age_max,
        )

    async def generate_story_titles(
        self,
        story_theme: str,
        story_lesson: str,
        num: int = 1,
        age_min: int = DEFAULT_AGE_MIN,
        age_max: int = DEFAULT_AGE_MAX,
        **kwargs,
    ) -> list[Title]:
        """Generate a title for the given story based on its content."""

        return await self.generate_items(
            num,
            "story_titles.md",
            {"story_theme": story_theme, "story_lesson": story_lesson},
            lambda response: [title.strip('"-. ') for title in response.splitlines()],
            age_min,
            age_max,
        )

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
