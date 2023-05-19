import asyncio
from dataclasses import asdict
import json
from pydantic import ValidationError
from quart import websocket

from betty.generator.story import StoryGenerator


async def emit_items_to_websocket(story_generator, **kwargs):
    start = {"type": "start"}
    await websocket.send(json.dumps(start))
    print(json.dumps(start))

    async for item in story_generator.stream_story_items(**kwargs):
        response = {"type": "item", "data": asdict(item)}
        await websocket.send(json.dumps(response))
        print(json.dumps(response))

    end = {"type": "end"}
    await websocket.send(json.dumps(end))
    print(json.dumps(end))


async def handle_generate_request(request, request_type):
    openai_api_key = request.headers.pop(
        "Authorization", "Invalid Authorization"
    ).split(" ")[1]
    story_generator = StoryGenerator(openai_api_key)

    data = await request.get_json()
    try:
        item_request = request_type.parse_obj(data)
    except ValidationError as ve:
        return {"error": str(ve)}, 400

    return await story_generator.generate_story_items(**item_request.dict())


async def handle_stream_request(websocket, request_type):
    message = await websocket.receive()
    data = json.loads(message)

    if data.get("type") == "request":
        try:
            item_request = request_type.parse_obj(data.get("data", {}))
        except ValidationError as ve:
            return {"error": str(ve)}, 400

        story_generator = StoryGenerator(data.pop("api_key", ""))
        asyncio.create_task(
            emit_items_to_websocket(story_generator, **item_request.dict())
        )
