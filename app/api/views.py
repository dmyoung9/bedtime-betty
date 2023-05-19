from quart import request, websocket, views

from .common import handle_generate_request, handle_stream_request


class BaseModelView(views.MethodView):
    def __init__(self, request_model):
        self.request_model = request_model

    @classmethod
    def as_view(cls, name, *class_args, **class_kwargs):
        view = super().as_view(name, *class_args, **class_kwargs)
        view.model = cls(*class_args, **class_kwargs)
        return view


class GenerateItemsView(BaseModelView):
    async def post(self):
        return await handle_generate_request(request, self.request_model)


class StreamItemsView(views.View):
    methods = ["GET"]

    def __init__(self, request_model, *class_args, **class_kwargs):
        self.request_model = request_model

    async def dispatch_request(self, **kwargs):
        return await self.websocket(websocket)

    async def websocket(self, websocket):
        while True:
            await handle_stream_request(websocket, self.request_model)
