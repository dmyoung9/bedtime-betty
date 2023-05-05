from dotenv import load_dotenv

from beddybai.generation.api import assistant, user

load_dotenv()

import asyncio
import os  # noqa: E402

from app import quart_app  # noqa: E402
from beddybai.generation.generator import StoryGenerator  # noqa: E402

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
story_generator = StoryGenerator(OPENAI_API_KEY)


async def main():
    pass
    # authors = await story_generator.generate_author_styles(num=5)
    # print(authors)
    # artists = await story_generator.generate_artist_styles(num=5)
    # print(artists)
    # async for theme in story_generator.generate_story_themes_streaming(num=3):
    #     print(theme.__dict__)
    # lessons = await story_generator.generate_story_lessons(num=5)
    # print(lessons)
    # async for lesson in story_generator.generate_story_lessons_streaming(num=3):
    #     print(lesson)

    story_info = {
        "age_min": 5,
        "age_max": 9,
        "author_name": "Dr. Seuss",
        "author_style": "whimsical and rhyming",
        "emoji": "🌳🐿️",
        "story_theme": "a squirrel learns to be brave in the forest",
        "story_lesson": "sharing is caring",
        "story_title": "Brave Little Squirrel",
    }

    previous_paragraphs = []
    total_paragraphs = 4
    for i in range(total_paragraphs):
        paragraph = await story_generator.generate_story_paragraph(
            story_info,
            previous_paragraphs=previous_paragraphs,
            total_paragraphs=total_paragraphs,
        )
        previous_paragraphs.append(paragraph)
        print(f"Paragraph {i+1}")
        print(paragraph)
        print()

    # theme_and_lesson = await story_generator.choose_lesson_for_theme(themes)
    # print(theme_and_lesson)
    # author_and_artist = story_generator.choose_author_and_artist(authors, artists)
    # print(author_and_artist)

    # story_info = {**theme_and_lesson, **author_and_artist}
    # async for page in story_generator.generate_pages(story_info, size=256):
    #     print(page)


if __name__ == "__main__":
    # asyncio.run(main())
    quart_app.run(host="0.0.0.0", port=5000, debug=True)
