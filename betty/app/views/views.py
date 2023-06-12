from quart import views

from betty.types import ItemModel

from .common import (
    # handle_create_request,
    handle_generate_request,
    handle_stream_request,
)


class BaseModelView(views.MethodView):
    def __init__(self, item_model: ItemModel):
        self.item_model = item_model

    @classmethod
    def as_view(cls, name, *class_args, **class_kwargs):
        view = super().as_view(name, *class_args, **class_kwargs)
        view.model = cls(*class_args, **class_kwargs)
        return view


# class CreateItemsView(BaseModelView):
#     async def post(self):
#         return await handle_create_request(self.item)


class GenerateItemsView(BaseModelView):
    async def post(self):
        return await handle_generate_request(self.item_model)


class StreamItemsView(views.View):
    methods = ["GET"]

    def __init__(self, item_model: ItemModel, *class_args, **class_kwargs):
        self.item_model = item_model

    async def dispatch_request(self, **kwargs):
        return await self.websocket()

    async def websocket(self):
        while True:
            await handle_stream_request(self.item_model)
