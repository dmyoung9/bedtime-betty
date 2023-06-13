from __future__ import annotations

from dataclasses import asdict
import json
from typing import Type

from quart import jsonify, request, websocket

from ...types.database import Stories
from ...chat.api import ChatAPI
from ...types import Item

from ...database import db

DEBUG = False


async def handle_create_request(item_type: Type[Item]):
    data = await request.get_json()
    item_request = item_type.get_item_model().parse_obj(data).dict()

    story = Stories(**item_request)

    db.session.add(story)
    db.session.commit()

    # items = await story_generator.generate(obj, **request_dict)

    return jsonify({"story": story.id}), 201


async def handle_generate_request(item_type: Type[Item]):
    openai_api_key = request.headers.pop(
        "Authorization", "Invalid Authorization"
    ).split(" ")[1]

    story_generator = ChatAPI(ai_prefix="Betty", openai_api_key=openai_api_key)

    data = await request.get_json()
    item_request = item_type.get_completion_request_model().parse_obj(data).dict()

    items = await story_generator.generate(item_type, **item_request)

    return {"total": len(items), "data": items}


async def handle_stream_request(item_type: Type[Item]):
    message = await websocket.receive()
    data = json.loads(message)
    emitted = []

    async def emit_item_to_websocket(item: Item) -> None:
        response = {"type": "item", "data": asdict(item)}
        await websocket.send(json.dumps(response))
        emitted.append(item)
        print(json.dumps(response))

    if data.get("type") == "request":
        data = data.get("data", {})
        item_request = item_type.get_completion_request_model().parse_obj(data).dict()

        story_generator = ChatAPI(
            ai_prefix="Betty", openai_api_key=data.pop("api_key", "")
        )

        start = {"type": "start", "requested": item_request.get("num", -1)}
        await websocket.send(json.dumps(start))
        print(json.dumps(start))

        await story_generator.stream(
            item_type, **item_request, callback_func=emit_item_to_websocket
        )

        end = {"type": "end", "total": len(emitted)}
        await websocket.send(json.dumps(end))
        print(json.dumps(end))
