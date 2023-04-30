import os
from pathlib import Path
from typing import Callable, Optional, Union

from .api import OpenAI, user
from .prompt import Prompt
from .types import (
    Artist,
    Author,
    Item,
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
            "plural": "(s)" if num > 1 else "",
        }

        if extra is not None:
            info.update(extra)

        prompt = Prompt.from_file(PROMPTS_PATH / prompt_filename).format_with(info)
        messages = (user(prompt),)

        print(f"Generating {prompt_filename.split('.')[0]} for {info}...")
        response = await self.api.get_completion(messages)

        return process_response(response) if process_response is not None else response

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
                Theme(
                    emoji=(theme := i.strip('"-. ').split(":"))[0].rstrip(),
                    story_theme=theme[1].lower().lstrip(),
                )
                for i in response.splitlines()
            ],
            age_min,
            age_max,
        )

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
    ) -> list[Title]:
        """Generate a title for the given story based on its content."""

        return await self.generate_items(
            num,
            "title.md",
            {"story_theme": story_theme, "story_lesson": story_lesson},
            lambda response: [title.strip('"-. ') for title in response.splitlines()],
            age_min,
            age_max,
        )
