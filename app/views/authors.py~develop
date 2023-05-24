from quart import Blueprint

from app.views.views import GenerateItemsView, StreamItemsView

from ..models.validation.requests import AuthorRequestModel

authors_blueprint = Blueprint("authors", __name__)

authors_blueprint.add_url_rule(
    "/generate",
    view_func=GenerateItemsView.as_view("generate_authors", AuthorRequestModel),
)
authors_blueprint.add_url_rule(
    "/stream",
    view_func=StreamItemsView.as_view("stream_authors", AuthorRequestModel),
    is_websocket=True,
)
