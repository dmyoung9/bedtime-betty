from quart import Blueprint

from app.api.views import GenerateItemsView, StreamItemsView

from ..validation import PageRequest

pages_blueprint = Blueprint("pages", __name__)

pages_blueprint.add_url_rule(
    "/generate", view_func=GenerateItemsView.as_view("generate_pages", PageRequest)
)
pages_blueprint.add_url_rule(
    "/stream",
    view_func=StreamItemsView.as_view("stream_pages", PageRequest),
    is_websocket=True,
)
