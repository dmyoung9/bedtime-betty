from quart import Blueprint

from betty.types.data import Artist

from .views import GenerateItemsView, StreamItemsView

artists_blueprint = Blueprint("artists", __name__)

artists_blueprint.add_url_rule(
    "/generate",
    view_func=GenerateItemsView.as_view("generate_artists", Artist),
)
artists_blueprint.add_url_rule(
    "/stream",
    view_func=StreamItemsView.as_view("stream_artists", Artist),
    is_websocket=True,
)
