import asyncio
from dataclasses import asdict
import json

from quart import Blueprint, request, websocket
from pydantic import ValidationError

from betty.generator import StoryGenerator
from betty.types import Lesson
from ..validation import ItemRequest

lessons_blueprint = Blueprint("lessons", __name__)


@lessons_blueprint.route("/generate", methods=["POST"])
async def generate_lessons():
    openai_api_key = request.headers.pop(
        "Authorization", "Invalid Authorization"
    ).split(" ")[1]
    story_generator = StoryGenerator(openai_api_key)

    data = await request.get_json()
    try:
        item_request = ItemRequest.parse_obj(data)
    except ValidationError as ve:
        return {"error": str(ve)}, 400

    if not item_request.examples:
        item_request.examples = Lesson.examples(item_request.num)

    return await story_generator.generate_story_items(Lesson, **item_request.dict())


@lessons_blueprint.websocket("/stream")
async def stream_lessons():
    story_generator = None

    async def parse_and_emit_objects(**kwargs):
        async for lesson in story_generator.stream_story_items(Lesson, **kwargs):
            response = {"type": "item", "data": asdict(lesson)}
            await websocket.send(json.dumps(response))

        end = {"type": "end"}
        await websocket.send(json.dumps(end))

    while True:
        message = await websocket.receive()
        data = json.loads(message)

        try:
            item_request = ItemRequest.parse_obj(data.get("data", {}))
        except ValidationError as ve:
            return {"error": str(ve)}, 400

        if data.get("type") == "request":
            story_generator = StoryGenerator(data.pop("api_key", ""))
            asyncio.create_task(parse_and_emit_objects(**item_request.dict()))
