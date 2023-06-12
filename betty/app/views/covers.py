from quart import Blueprint

from betty.types.covers import CoverModel

from .views import GenerateItemsView, StreamItemsView

covers_blueprint = Blueprint("covers", __name__)

covers_blueprint.add_url_rule(
    "/generate", view_func=GenerateItemsView.as_view("generate_covers", CoverModel)
)
covers_blueprint.add_url_rule(
    "/stream",
    view_func=StreamItemsView.as_view("stream_covers", CoverModel),
    is_websocket=True,
)
