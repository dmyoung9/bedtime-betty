from quart import Blueprint

from betty.types.data import Author

from .views import GenerateItemsView, StreamItemsView

authors_blueprint = Blueprint("authors", __name__)

authors_blueprint.add_url_rule(
    "/generate",
    view_func=GenerateItemsView.as_view("generate_authors", Author),
)
authors_blueprint.add_url_rule(
    "/stream",
    view_func=StreamItemsView.as_view("stream_authors", Author),
    is_websocket=True,
)
