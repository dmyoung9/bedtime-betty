from quart import Blueprint

from backend.api.views import GenerateItemsView, StreamItemsView

from ..validation import DescriptionRequest

descriptions_blueprint = Blueprint("descriptions", __name__)

descriptions_blueprint.add_url_rule(
    "/generate",
    view_func=GenerateItemsView.as_view("generate_descriptions", DescriptionRequest),
)
descriptions_blueprint.add_url_rule(
    "/stream",
    view_func=StreamItemsView.as_view("stream_descriptions", DescriptionRequest),
    is_websocket=True,
)
