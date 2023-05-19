from quart import Blueprint

from app.api.views import GenerateItemsView, StreamItemsView

from ..validation import AuthorRequest

authors_blueprint = Blueprint("authors", __name__)

authors_blueprint.add_url_rule(
    "/generate",
    view_func=GenerateItemsView.as_view("generate_authors", AuthorRequest),
)
authors_blueprint.add_url_rule(
    "/stream",
    view_func=StreamItemsView.as_view("stream_authors", AuthorRequest),
    is_websocket=True,
)
