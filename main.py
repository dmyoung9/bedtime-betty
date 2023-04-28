import asyncio

from beddybai.generation.api import OpenAI
from beddybai.generation.generator import StoryGenerator

api = OpenAI()
story_generator = StoryGenerator()


async def main():
    authors = await story_generator.generate_author_styles(5)
    artists = await story_generator.generate_artist_styles(5)
    themes = await story_generator.generate_story_themes(5)

    theme_and_lesson = await story_generator.choose_lesson_for_theme(themes)
    author_and_artist = story_generator.choose_author_and_artist(authors, artists)

    story_info = {**theme_and_lesson, **author_and_artist}
    async for page in story_generator.generate_pages(story_info, size=256):
        print(page)


if __name__ == "__main__":
    asyncio.run(main())
