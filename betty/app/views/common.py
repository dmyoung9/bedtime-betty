from __future__ import annotations

from dataclasses import asdict
import json
from typing import Type

from quart import jsonify, request, websocket

from betty.types.database import Stories
from betty.chat.api import ChatAPI
from betty.types import Item

from ...database import db

DEBUG = False


async def handle_create_request(obj: Type[Item]):
    data = await request.get_json()
    data["obj"] = obj.model()
    item_request = obj.create_model().parse_obj(data)
    request_dict = item_request.dict()
    request_dict.pop("obj", None)

    story = Stories(**request_dict)

    db.session.add(story)
    db.session.commit()

    # items = await story_generator.generate(obj, **request_dict)

    return jsonify({"story": story.id}), 201


async def handle_generate_request(obj: Type[Item]):
    openai_api_key = request.headers.pop(
        "Authorization", "Invalid Authorization"
    ).split(" ")[1]

    story_generator = ChatAPI(ai_prefix="Betty", openai_api_key=openai_api_key)

    data = await request.get_json()
    data["obj"] = obj.model()
    item_request = obj.request_model().parse_obj(data)
    request_dict = item_request.dict()
    request_dict.pop("obj", None)

    items = await story_generator.generate(obj, **request_dict)

    return {"total": len(items), "data": items}


async def handle_stream_request(obj: Type[Item]):
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
        data["obj"] = obj.model()
        item_request = obj.request_model().parse_obj(data)
        request_dict = item_request.dict()
        request_dict.pop("obj", None)

        story_generator = ChatAPI(
            ai_prefix="Betty", openai_api_key=data.pop("api_key", "")
        )

        start = {"type": "start", "requested": request_dict.get("num", -1)}
        await websocket.send(json.dumps(start))
        print(json.dumps(start))

        await story_generator.stream(
            obj, **request_dict, callback_func=emit_item_to_websocket
        )

        end = {"type": "end", "total": len(emitted)}
        await websocket.send(json.dumps(end))
        print(json.dumps(end))
