from dotenv import load_dotenv

from backend import quart_app
from betty.api.openai.gpt import CompletionAPI
from betty.types import Author, Idea, Lesson, Page, Title

load_dotenv()

# import asyncio  # noqa: E402
import random  # noqa: E402
import os  # noqa: E402

# from app import quart_app  # noqa: E402
from betty.generator.story import StoryGenerator  # noqa: E402

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
CLIENT = CompletionAPI(OPENAI_API_KEY)
story_generator = StoryGenerator(OPENAI_API_KEY)


async def main():
    ideas = []
    lessons = []
    authors = []
    # artists = []
    # scenes = []

    async for idea in story_generator.stream_story_items(Idea, num=1):
        ideas.append(idea)
        print(idea, end=",\n")
    print()

    async for lesson in story_generator.stream_story_items(Lesson, num=1):
        lessons.append(lesson)
        print(lesson, end=",\n")
    print()

    async for author in story_generator.stream_story_items(Author, num=1):
        authors.append(author)
        print(author, end=",\n")
    print()

    # async for artist in story_generator.stream_items(Artist, age=9, num=12):
    #     artists.append(artist)
    #     print(artist, end=",\n")
    # print()

    # async for scene in story_generator.stream_items(
    #     Scene,
    #     story_paragraph={
    #         "content": ""
    #     },
    #     num=3,
    # ):
    #     scenes.append(scene)
    #     print(scene, end=",\n")
    # print()

    titles = []
    async for title in story_generator.stream_story_items(
        Title,
        num=1,
        story_idea=(story_idea := random.choice(ideas)),
        story_lesson=(story_lesson := random.choice(lessons)),
        story_author=(story_author := random.choice(authors)),
    ):
        titles.append(title)
        print(title, end=",\n")

    print()
    async for paragraph in story_generator.stream_story_items(
        Page,
        num=5,
        story_idea=story_idea,
        story_lesson=story_lesson,
        story_author=story_author,
        story_title=(story_title := random.choice(titles)),
    ):
        print(paragraph, end=",\n")
    print()


if __name__ == "__main__":
    # asyncio.run(main())
    quart_app.run(host="0.0.0.0", port=5000, debug=True)
