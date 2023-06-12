from __future__ import annotations

import json
from typing import Type

from quart import request, websocket

# from betty.types.database import Stories
from betty.chat.api import ChatAPI
from betty.types import ItemModel

# from ...database import db

DEBUG = False


# async def handle_create_request(obj: Type[Item]):
#     data = await request.get_json()
#     data["obj"] = obj.model()
#     item_request = obj.create_model().parse_obj(data)
#     request_dict = item_request.dict()
#     request_dict.pop("obj", None)

#     story = Stories(**request_dict)

#     db.session.add(story)
#     db.session.commit()

#     # items = await story_generator.generate(obj, **request_dict)

#     return jsonify({"story": story.id}), 201


async def handle_generate_request(obj: Type[ItemModel]):
    openai_api_key = request.headers.pop(
        "Authorization", "Invalid Authorization"
    ).split(" ")[1]

    story_generator = ChatAPI(ai_prefix="Betty", openai_api_key=openai_api_key)

    data = await request.get_json()
    item_request = obj.get_completion_request_model().parse_obj(data).dict()

    items = await story_generator.generate(obj, **item_request)

    return {"total": len(items), "data": items}


async def handle_stream_request(obj: Type[ItemModel]):
    message = await websocket.receive()
    data = json.loads(message)
    emitted = []

    async def emit_item_to_websocket(item: ItemModel) -> None:
        response = {"type": "item", "data": item.dict()}
        await websocket.send(json.dumps(response))
        emitted.append(item)
        print(json.dumps(response))

    if data.get("type") == "request":
        data = data.get("data", {})
        item_request = obj.get_completion_request_model().parse_obj(data).dict()

        story_generator = ChatAPI(
            ai_prefix="Betty", openai_api_key=data.pop("api_key", "")
        )

        start = {"type": "start", "requested": item_request.get("num", -1)}
        await websocket.send(json.dumps(start))
        print(json.dumps(start))

        await story_generator.stream(
            obj, **item_request, callback_func=emit_item_to_websocket
        )

        end = {"type": "end", "total": len(emitted)}
        await websocket.send(json.dumps(end))
        print(json.dumps(end))
