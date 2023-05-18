import asyncio
from dataclasses import asdict
import json

from quart import Blueprint, request, websocket
from pydantic import ValidationError

from betty.generator import StoryGenerator
from betty.types import Idea
from ..validation import ItemRequest

ideas_blueprint = Blueprint("ideas", __name__)


@ideas_blueprint.route("/generate", methods=["POST"])
async def generate_ideas():
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
        item_request.examples = Idea.examples(item_request.num)

    return await story_generator.generate_story_ideas(**item_request.dict())


@ideas_blueprint.websocket("/stream")
async def stream_ideas():
    story_generator = None

    async def parse_and_emit_objects(**kwargs):
        async for idea in story_generator.stream_story_ideas(**kwargs):
            response = {"type": "item", "data": asdict(idea)}
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
