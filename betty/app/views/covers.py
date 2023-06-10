from quart import Blueprint

from betty.types.data import Cover

from .views import GenerateItemsView, StreamItemsView

covers_blueprint = Blueprint("covers", __name__)

covers_blueprint.add_url_rule(
    "/generate", view_func=GenerateItemsView.as_view("generate_covers", Cover)
)
covers_blueprint.add_url_rule(
    "/stream",
    view_func=StreamItemsView.as_view("stream_covers", Cover),
    is_websocket=True,
)
