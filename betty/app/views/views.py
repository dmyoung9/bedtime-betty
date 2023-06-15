from dataclasses import asdict
import json
from typing import Type

from quart import jsonify, request, views, websocket

from betty.chat.api import ChatAPI
from betty.types import Item

from ...database import db


class BaseModelView(views.MethodView):
    """
    Base class for all ModelView classes.

    Attributes:
        item_type (Type[Item]): The type of the item that this view handles.
    """

    def __init__(self, item_type: Type[Item]):
        self.item_type = item_type

    @classmethod
    def as_view(cls, name, *class_args, **class_kwargs):
        view = super().as_view(name, *class_args, **class_kwargs)
        view.model = cls(*class_args, **class_kwargs)
        return view


class CreateItemsView(BaseModelView):
    """
    A view for creating items.

    Inherits from:
        BaseModelView
    """

    async def handle_create_request(self):
        """
        Handles a create request.

        Returns:
            A tuple of a JSON response and a status code.
        """
        data = await request.get_json()
        item_request = self.item_type.get_item_model().parse_obj(data).dict()

        story = self.item_type.get_database_model()(**item_request)

        db.session.add(story)
        db.session.commit()

        return jsonify({"story": story.id}), 201

    async def post(self):
        """
        Handles a POST request.

        Returns:
            The result of handle_create_request.
        """
        return await self.handle_create_request()


class GenerateItemsView(BaseModelView):
    """
    A view for generating items.

    Inherits from:
        BaseModelView
    """

    async def handle_generate_request(self):
        """
        Handles a generate request.

        Returns:
            A dictionary containing the total number of items and the data for the
            items.
        """
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
        """
        Handles a POST request.

        Returns:
            The result of handle_generate_request.
        """
        return await self.handle_generate_request()


class RetrieveItemsView(BaseModelView):
    """
    A view for retrieving items.

    Inherits from:
        BaseModelView
    """

    async def handle_retrieve_request(self, id: int):
        """
        Handles a retrieve request.

        Args:
            id (int): The id of the item to retrieve.

        Returns:
            A JSON response containing the item data.
        """
        item = self.item_type.get_database_model().query.get_or_404(id)
        return jsonify(item.to_dict())

    async def get(self, id):
        """
        Handles a GET request.

        Args:
            id (int): The id of the item to retrieve.

        Returns:
            The result of handle_retrieve_request.
        """
        return await self.handle_retrieve_request(id)


class ListItemsView(BaseModelView):
    """
    A view for retrieving a list of existing items.

    Inherits from:
        BaseModelView
    """

    async def handle_list_request(self):
        """
        Handles a list request.

        Returns:
            A JSON response containing the item data.
        """
        items = self.item_type.get_database_model().query.all()
        return jsonify([item.to_dict() for item in items])

    async def get(self):
        """
        Handles a GET request.

        Returns:
            The result of handle_list_request.
        """
        return await self.handle_list_request()


class StreamItemsView(views.View):
    """
    A view for streaming items.

    Inherits from:
        views.View
    """

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
        """
        Handles a streamed item.

        Args:
            item (Item): The item to handle.
            **kwargs: Additional keyword arguments.
        """
        response = {"type": "item", "data": asdict(item)}
        await websocket.send(json.dumps(response))
        print(json.dumps(response))

    async def handle_stream_request(self, data, **kwargs):
        """
        Handles a stream request.

        Args:
            data (dict): The request data.
            **kwargs: Additional keyword arguments.
        """
        item_request = (
            self.item_type.get_completion_request_model().parse_obj(data).dict()
        )

        story_generator = ChatAPI(
            ai_prefix="Betty", openai_api_key=data.pop("api_key", "")
        )

        await story_generator.stream(
            self.item_type,
            **item_request,
            callback_func=self.handle_streamed_item,
            callback_kwargs=kwargs
        )

    async def websocket(self, **kwargs):
        """
        Handles a websocket connection.

        **kwargs: Additional keyword arguments.
        """
        while True:
            message = await websocket.receive()
            data = json.loads(message)
            if data.get("type") == "request":
                start = json.dumps({"type": "start"})
                await websocket.send(start)
                print(start)

                await self.handle_stream_request(data.get("data", {}), **kwargs)

                end = json.dumps({"type": "end"})
                await websocket.send(end)
                print(end)
