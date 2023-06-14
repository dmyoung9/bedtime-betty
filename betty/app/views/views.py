from dataclasses import asdict
import json
from typing import Type

from quart import jsonify, request, views, websocket

from betty.chat.api import ChatAPI
from betty.types import Item

from ...database import db


class BaseModelView(views.MethodView):
    def __init__(self, item_type: Type[Item]):
        self.item_type = item_type

    @classmethod
    def as_view(cls, name, *class_args, **class_kwargs):
        view = super().as_view(name, *class_args, **class_kwargs)
        view.model = cls(*class_args, **class_kwargs)
        return view


class CreateItemsView(BaseModelView):
    async def handle_create_request(self):
        data = await request.get_json()
        item_request = self.item_type.get_item_model().parse_obj(data).dict()

        story = self.item_type.get_database_model()(**item_request)

        db.session.add(story)
        db.session.commit()

        return jsonify({"story": story.id}), 201

    async def post(self):
        return await self.handle_create_request()


class GenerateItemsView(BaseModelView):
    async def handle_generate_request(self):
        openai_api_key = request.headers.pop(
            "Authorization", "Invalid Authorization"
        ).split(" ")[1]

        story_generator = ChatAPI(ai_prefix="Betty", openai_api_key=openai_api_key)

        data = await request.get_json()
        item_request = (
            self.item_type.get_completion_request_model().parse_obj(data).dict()
        )

        items = await story_generator.generate(self.item_type, **item_request)

        return {"total": len(items), "data": items}

    async def post(self):
        return await self.handle_generate_request()


class RetrieveItemsView(BaseModelView):
    async def handle_retrieve_request(self, id: int):
        item = self.item_type.get_database_model().query.get_or_404(id)
        return jsonify(item.to_dict())

    async def get(self, id):
        return await self.handle_retrieve_request(id)


class StreamItemsView(views.View):
    methods = ["GET"]

    def __init__(self, item_type: Type[Item]):
        self.item_type = item_type

    @classmethod
    def as_view(cls, name, *class_args, **class_kwargs):
        view = super().as_view(name, *class_args, **class_kwargs)
        view.model = cls(*class_args, **class_kwargs)
        return view

    async def dispatch_request(self, **kwargs):
        return await self.websocket(**kwargs)

    async def handle_streamed_item(self, item: Item, **kwargs) -> None:
        response = {"type": "item", "data": asdict(item)}
        await websocket.send(json.dumps(response))
        print(json.dumps(response))

    async def handle_stream_request(self, **kwargs):
        message = await websocket.receive()
        data = json.loads(message)

        if data.get("type") == "request":
            data = data.get("data", {})
            item_request = (
                self.item_type.get_completion_request_model().parse_obj(data).dict()
            )

            story_generator = ChatAPI(
                ai_prefix="Betty", openai_api_key=data.pop("api_key", "")
            )

            start = json.dumps({"type": "start"})
            await websocket.send(start)
            print(start)

            await story_generator.stream(
                self.item_type,
                **item_request,
                callback_func=self.handle_streamed_item,
                callback_kwargs=kwargs
            )

            end = json.dumps({"type": "end"})
            await websocket.send(end)
            print(end)

    async def websocket(self, **kwargs):
        while True:
            await self.handle_stream_request(**kwargs)
