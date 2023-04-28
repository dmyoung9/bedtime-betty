import os
from pathlib import Path
import random
from typing import AsyncGenerator

from .api import OpenAI, user
from .prompt import Prompt
from .types import Artist, Author, Page, Story, StoryInfo, Theme, Lesson


BASE_PATH = Path(os.getcwd())
PROMPTS_PATH = BASE_PATH / "prompts"


class StoryGenerator:
    """
    A class for generating stories, titles, themes, lessons, authors, artists,
    and images using OpenAI's API. Each story is tailored for a specific age
    range based on the user inputs.
    """

    def __init__(self, age_min: int = 5, age_max: int = 9):
        """Initialize a new instance of the StoryGenerator class."""

        self.age_min = age_min
        self.age_max = age_max
        self.api = OpenAI()

    @staticmethod
    def choose_author_and_artist(
        authors: list[Author], artists: list[Artist]
    ) -> StoryInfo:
        """Choose an author and artist for the story, ensuring that the author and
        artist are the same if they appear in both lists, otherwise selecting a
        random artist."""

        author = random.choice(authors)
        artist = next(
            (artist for artist in artists if artist["artist"] == author["author"]),
            random.choice(artists),
        )

        return {**author, **artist}  # type: ignore

    async def choose_lesson_for_theme(self, themes: list[Theme], **kwargs) -> StoryInfo:
        """Choose a lesson based on the provided theme or a random theme from the
        list."""

        theme = kwargs.get("story_theme") or random.choice(themes)
        lessons = await self.generate_story_lessons(theme["story_theme"], **kwargs)
        lesson = random.choice(lessons)

        return {**theme, "story_lesson": lesson}  # type: ignore

    async def generate_story_themes(self, num: int = 3) -> list[Theme]:
        """Generate a list of story themes based on the target age range."""

        info: StoryInfo = {"age_min": self.age_min, "age_max": self.age_max, "num": num}
        prompt = Prompt.from_file(PROMPTS_PATH / "story_themes.md").format_with(info)
        messages = (user(prompt),)
        print(f"Generating themes for {info}...")
        theme_response = await self.api.get_completion(messages)

        return [
            {
                "emoji": (theme := i.lstrip("- ").rstrip(".").split(": "))[0],
                "story_theme": theme[1].lower(),
            }
            for i in theme_response.splitlines()
        ]

    async def generate_story_lessons(
        self, story_theme: str, num: int = 10
    ) -> list[Lesson]:
        """Generate a list of lessons for a specific story theme based on the target
        age range."""

        info: StoryInfo = {
            "age_min": self.age_min,
            "age_max": self.age_max,
            "num": num,
            "story_theme": story_theme,
        }
        prompt = Prompt.from_file(PROMPTS_PATH / "story_lessons.md").format_with(info)
        messages = (user(prompt),)
        print(f"Generating lessons for {info}...")
        lesson_response = await self.api.get_completion(messages)

        return [
            lesson.lstrip("- ").strip().rstrip(".").lower()
            for lesson in lesson_response.splitlines()
        ]

    async def generate_author_styles(self, num: int = 10) -> list[Author]:
        """Generate a list of author styles based on the target age range."""

        info: StoryInfo = {"age_min": self.age_min, "age_max": self.age_max, "num": num}
        prompt = Prompt.from_file(PROMPTS_PATH / "author_styles.md").format_with(info)
        messages = (user(prompt),)
        print(f"Generating authors for {info}...")
        author_response = await self.api.get_completion(messages)

        return [
            {
                "author": (author := i.lstrip("- ").rstrip(".").split(": "))[0],
                "author_style": author[1].lower(),
            }
            for i in author_response.splitlines()
        ]

    async def generate_artist_styles(self, num: int = 10) -> list[Artist]:
        """Generate a list of artist styles based on the target age range."""

        info: StoryInfo = {"age_min": self.age_min, "age_max": self.age_max, "num": num}
        prompt = Prompt.from_file(PROMPTS_PATH / "artist_styles.md").format_with(info)
        messages = (user(prompt),)
        print(f"Generating artists for {info}...")
        artist_response = await self.api.get_completion(messages)

        return [
            {
                "artist": (artist := i.lstrip("- ").rstrip(".").split(": "))[0],
                "artist_style": artist[1].lower(),
            }
            for i in artist_response.splitlines()
        ]

    async def generate_title(self, story: list[Page]) -> str:
        """Generate a title for the given story based on its content."""

        story_paragraphs: str = "\n\n".join(page["content"] for page in story)
        prompt = Prompt.from_file(PROMPTS_PATH / "title.md").format_with(
            {"story": story_paragraphs}
        )
        messages = (user(prompt),)
        print("Generating title for story...")
        title_response = await self.api.get_completion(messages)

        return title_response.strip()

    async def generate_image(
        self, story_paragraph: str, story_info: StoryInfo, **kwargs
    ) -> str:
        """Generate an image based on the story paragraph and story information."""

        info: StoryInfo = {
            **story_info,  # type: ignore
            "story_paragraph": story_paragraph,
        }

        prompt = Prompt.from_file(PROMPTS_PATH / "dall_e_prompt.md").format_with(info)
        messages = (user(prompt),)
        print("Generating image prompt...")
        prompt_response = await self.api.get_completion(messages)

        print(f"Generating image for {prompt_response}...")
        art = await self.api.get_image(prompt_response, **kwargs)
        return art

    async def generate_story(self, story_info: StoryInfo) -> Story:
        """Generate a complete story based on the provided story information."""

        story_info.update({"age_min": self.age_min, "age_max": self.age_max})
        prompt = Prompt.from_file(PROMPTS_PATH / "story.md").format_with(story_info)
        messages = (user(prompt),)
        print(f"Generating story for {story_info}...")
        story_response = await self.api.get_completion(messages)
        story_paragraphs: list[Page] = [
            {"content": paragraph.strip()} for paragraph in story_response.split("\n\n")
        ]
        story_title = await self.generate_title(story_paragraphs)

        return {"title": story_title, "pages": story_paragraphs}

    async def generate_pages(
        self, story_info: StoryInfo, **kwargs
    ) -> AsyncGenerator[str | Page, None]:
        """Generate pages for a story, including images, based on the provided story
        information."""

        story = await self.generate_story(story_info)
        yield story["title"]

        for page in story["pages"]:
            page["image"] = await self.generate_image(
                page["content"], story_info, **kwargs
            )
            yield page
