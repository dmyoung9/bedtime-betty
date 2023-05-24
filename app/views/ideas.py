from quart import Blueprint

from app.views.views import GenerateItemsView, StreamItemsView

from ..models.validation import IdeaRequestModel

ideas_blueprint = Blueprint("ideas", __name__)

ideas_blueprint.add_url_rule(
    "/generate", view_func=GenerateItemsView.as_view("generate_ideas", IdeaRequestModel)
)
ideas_blueprint.add_url_rule(
    "/stream",
    view_func=StreamItemsView.as_view("stream_ideas", IdeaRequestModel),
    is_websocket=True,
)
