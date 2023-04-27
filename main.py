import random
import json

from beddybai.generation.api import OpenAI
from beddybai.generation.generator import StoryGenerator
from beddybai.common.utils import clean_numbered_content

api = OpenAI()
story_generator = StoryGenerator({}, {})


async def main():
    prompts = None
    with open("./prompts.json", "r") as f:
        prompts = json.load(f)

    info = {
        "age_min": 5,
        "age_max": 9,
        "author_style": random.choice(prompts["story"]["styles"])["style"],
        "artist_style": random.choice(prompts["illustration"]["styles"]),
    }

    idea_messages = (OpenAI.user(prompts["ideas"]["prompt"].format(**info)),)
    moral_messages = (OpenAI.user(prompts["morals"]["prompt"].format(**info)),)

    ideas = await api.get_completion(idea_messages)
    morals = await api.get_completion(moral_messages)

    info.update(
        {
            "story_theme": random.choice(clean_numbered_content(ideas)),
            "moral_lesson": random.choice(clean_numbered_content(morals)),
        }
    )

    print(info)

    story_messages = (OpenAI.user(prompts["story"]["prompt"].format(**info)),)

    title, sections = await story_generator.generate_story(
        story_messages, info, prompts
    )
    print(title)
    print()
    for section in sections:
        print(section["section"])
        # print(section["art"])
        print()
