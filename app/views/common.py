import asyncio
from dataclasses import asdict
import json

# from pydantic import ValidationError
from quart import request, websocket

from betty.generator.story import StoryGenerator
from betty.generator.test import TestGenerator

DEBUG = True


async def emit_items_to_websocket(story_generator, **kwargs):
    start = {"type": "start", "requested": kwargs.get("num", -1)}
    await websocket.send(json.dumps(start))
    print(json.dumps(start))
    emitted = 0

    async for item in story_generator.stream_story_items(**kwargs):
        response = {"type": "item", "data": asdict(item)}
        await websocket.send(json.dumps(response))
        emitted += 1
        print(json.dumps(response))

    end = {"type": "end", "total": emitted}
    await websocket.send(json.dumps(end))
    print(json.dumps(end))


async def handle_generate_request(request_type):
    openai_api_key = request.headers.pop(
        "Authorization", "Invalid Authorization"
    ).split(" ")[1]

    story_generator = TestGenerator() if DEBUG else StoryGenerator(openai_api_key)

    data = await request.get_json()
    # try:
    item_request = request_type.parse_obj(data)
    print(item_request)
    # except ValidationError as ve:
    #     return {"error": str(ve)}, 400

    items = await story_generator.generate_story_items(**item_request.dict())

    return {"total": len(items), "data": items}


async def handle_stream_request(request_type):
    message = await websocket.receive()
    data = json.loads(message)

    if data.get("type") == "request":
        # try:
        item_request = request_type.parse_obj(data.get("data", {}))
        # except ValidationError as ve:
        #     return {"error": str(ve)}, 400

        openai_api_key = data.pop("api_key", "")
        story_generator = TestGenerator() if DEBUG else StoryGenerator(openai_api_key)

        asyncio.create_task(
            emit_items_to_websocket(story_generator, **item_request.dict())
        )