from dotenv import load_dotenv

from betty.api import OpenAI, assistant, user
from betty.types import Artist, Author, Idea, Lesson, Paragraph, Scene, Title

load_dotenv()

import asyncio
import random
import os  # noqa: E402

# from app import quart_app  # noqa: E402
from betty.generator import StoryGenerator  # noqa: E402

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
CLIENT = OpenAI(OPENAI_API_KEY)
story_generator = StoryGenerator(CLIENT)


async def main():
    ideas = []
    lessons = []
    authors = []
    # artists = []
    # scenes = []

    async for idea in story_generator.stream_items(Idea, num=10):
        ideas.append(idea)
        print(idea, end=",\n")
    print()

    async for lesson in story_generator.stream_items(Lesson, num=10):
        lessons.append(lesson)
        print(lesson, end=",\n")
    print()

    async for author in story_generator.stream_items(Author, num=5):
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
    #         "content": 'She approached the Honesty Tree with a feeling of shame, \nAnd whispered softly, "I\'m the one to blame." \nThe tree rustled gently and whispered back, \n"Honesty is best, it\'s a fact you can\'t hack."'
    #     },
    #     num=3,
    # ):
    #     scenes.append(scene)
    #     print(scene, end=",\n")
    # print()

    titles = []
    async for title in story_generator.stream_items(
        Title,
        examples=[],
        num=1,
        story_idea=(story_idea := random.choice(ideas)),
        story_lesson=(story_lesson := random.choice(lessons)),
        story_author=(story_author := random.choice(authors)),
    ):
        story_title = title
        titles.append(title)
        print(title, end=",\n")

    print()
    async for paragraph in story_generator.stream_items(
        Paragraph,
        examples=[],
        num=5,
        story_idea=story_idea,
        story_lesson=story_lesson,
        story_author=story_author,
        story_title=story_title,
    ):
        print(paragraph, end=",\n")
    print()


if __name__ == "__main__":
    asyncio.run(main())
    # quart_app.run(host="0.0.0.0", port=5000, debug=True)
