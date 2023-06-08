from quart import views

from betty.types import Item

from .common import handle_generate_request, handle_stream_request


class BaseModelView(views.MethodView):
    def __init__(self, item: Item):
        self.item = item

    @classmethod
    def as_view(cls, name, *class_args, **class_kwargs):
        view = super().as_view(name, *class_args, **class_kwargs)
        view.model = cls(*class_args, **class_kwargs)
        return view


class GenerateItemsView(BaseModelView):
    async def post(self):
        return await handle_generate_request(self.item)


class StreamItemsView(views.View):
    methods = ["GET"]

    def __init__(self, item: Item, *class_args, **class_kwargs):
        self.item = item

    async def dispatch_request(self, **kwargs):
        return await self.websocket()

    async def websocket(self):
        while True:
            await handle_stream_request(self.item)
