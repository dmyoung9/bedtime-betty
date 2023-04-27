import re
from typing import Tuple

from ..common.utils import TITLE_LINE_REGEX
from .api import OpenAI


class StoryGenerator:
    def __init__(
        self,
        author: dict[str, str],
        artist: dict[str, str],
        age_range: Tuple[int, int] = (
            2,
            8,
        ),
        total_paragraphs: int = 7,
    ):
        self.author_style = author
        self.artist_style = artist
        self.age_range = age_range
        self.total_paragraphs = total_paragraphs
        self.story_theme = None
        self.story_lesson = None
        self.api = OpenAI()

    async def generate_story_ideas(self, num: int = 3):
        pass

    async def generate_image(
        self, segment_data: dict[str, str], info: dict[str, str | int], prompts: dict
    ) -> str:
        """
        Generates a prompt with which to generate an image, and then
        generates an image with it. Updates the data given to the function.
        """
        art_messages = (
            OpenAI.user(
                prompts["illustration"]["prompt"].format(
                    story_passage=segment_data["section"], **info["artist_style"]
                )
            ),
        )
        prompt = await self.api.get_completion(art_messages)
        # print(prompt)
        segment_data["art"] = await self.api.get_image(prompt)
        return segment_data["art"]

    async def process_chunk(self, chunk, sections, buffer, title=""):
        segment_data = None

        if (content := chunk.get("content")) is not None:
            buffer += content
            segment = ""
            print(content, end="")

            while "\n\n" in buffer:
                segment_data = {"section": None, "art": None}

                segment, _, buffer = buffer.partition("\n\n")

                if title_match := re.match(TITLE_LINE_REGEX, segment.rstrip()):
                    match = title_match.groups()[0]
                    if not sections:
                        title = match
                    else:
                        segment_data["section"] = match
                else:
                    segment_data["section"] = segment.rstrip()
        elif (choices := chunk.get("choices")) and choices[0][
            "finish_reason"
        ] is not None:
            segment_data = {"art": None, "section": buffer.rstrip()}

        if segment_data is not None:
            sections.append(segment_data)
        # image_task = asyncio.create_task(generate_image(segment_data, info, prompts))
        # pending_image_tasks.append(image_task)

        return title, buffer

    async def generate_story(
        self, prompt: str, info: dict[str, str | int], prompts: dict
    ) -> Tuple[str, list[dict[str, str]]]:
        """Generates a story from a prompt, including illustrations."""

        title = ""
        sections: list[dict[str, str]] = []
        # pending_image_tasks = []
        buffer = ""

        async for chunk in self.api.get_streaming_completion(prompt):
            title, buffer = await self.process_chunk(chunk, sections, buffer, title)

        # await asyncio.gather(*pending_image_tasks)

        return title, sections
