from dotenv import load_dotenv

from beddybai.generation.api import assistant, user

load_dotenv()

import asyncio
import os  # noqa: E402

# from app import quart_app  # noqa: E402
from betty.generator.story import StoryGenerator  # noqa: E402

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
CLIENT = CompletionAPI(OPENAI_API_KEY)
story_generator = StoryGenerator(OPENAI_API_KEY)


async def main():
    pass
    # authors = await story_generator.generate_author_styles(num=5)
    # print(authors)
    # artists = await story_generator.generate_artist_styles(num=5)
    # print(artists)
    async for theme in story_generator.generate_story_themes_streaming(num=3):
        print(theme.__dict__)
    # lessons = await story_generator.generate_story_lessons(num=5)
    # print(lessons)

    # story_info = {
    #     "age_min": 5,
    #     "age_max": 9,
    #     "author_name": "Dr. Seuss",
    #     "author_style": "whimsical and rhyming",
    #     "emoji": "🌳🐿️",
    #     "story_theme": "a squirrel learns to be brave in the forest",
    #     "story_lesson": "sharing is caring",
    #     "story_title": "Brave Little Squirrel",
    # }

    # previous_paragraphs = []
    # total_paragraphs = 4
    # for i in range(total_paragraphs):
    #     paragraph = await story_generator.generate_story_paragraph(
    #         story_info,
    #         previous_paragraphs=previous_paragraphs,
    #         total_paragraphs=total_paragraphs,
    #     )
    #     previous_paragraphs.append(paragraph)
    #     print(f"Paragraph {i+1}")
    #     print(paragraph)
    #     print()

    # theme_and_lesson = await story_generator.choose_lesson_for_theme(themes)
    # print(theme_and_lesson)
    # author_and_artist = story_generator.choose_author_and_artist(authors, artists)
    # print(author_and_artist)

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
