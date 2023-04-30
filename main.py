from dotenv import load_dotenv

load_dotenv()

import os  # noqa: E402

from app import quart_app  # noqa: E402
from beddybai.generation.generator import StoryGenerator  # noqa: E402

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
story_generator = StoryGenerator(OPENAI_API_KEY)


async def main():
    authors = await story_generator.generate_author_styles(num=5)
    print(authors)
    artists = await story_generator.generate_artist_styles(num=5)
    print(artists)
    themes = await story_generator.generate_story_themes(num=5)
    print(themes)
    lessons = await story_generator.generate_story_lessons(num=5)
    print(lessons)

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
