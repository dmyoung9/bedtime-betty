from quart import Blueprint

from backend.api.views import GenerateItemsView, StreamItemsView

from ..validation import IdeaRequest

ideas_blueprint = Blueprint("ideas", __name__)

ideas_blueprint.add_url_rule(
    "/generate", view_func=GenerateItemsView.as_view("generate_ideas", IdeaRequest)
)
ideas_blueprint.add_url_rule(
    "/stream",
    view_func=StreamItemsView.as_view("stream_ideas", IdeaRequest),
    is_websocket=True,
)
