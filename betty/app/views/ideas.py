from quart import Blueprint

from betty.types.validation import IdeaModel

from .views import GenerateItemsView, StreamItemsView

ideas_blueprint = Blueprint("ideas", __name__)

ideas_blueprint.add_url_rule(
    "/generate", view_func=GenerateItemsView.as_view("generate_ideas", IdeaModel)
)
ideas_blueprint.add_url_rule(
    "/stream",
    view_func=StreamItemsView.as_view("stream_ideas", IdeaModel),
    is_websocket=True,
)
