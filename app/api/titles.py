from quart import Blueprint

from app.api.views import GenerateItemsView, StreamItemsView

from ..validation import TitleRequest

titles_blueprint = Blueprint("titles", __name__)

titles_blueprint.add_url_rule(
    "/generate", view_func=GenerateItemsView.as_view("generate_titles", TitleRequest)
)
titles_blueprint.add_url_rule(
    "/stream",
    view_func=StreamItemsView.as_view("stream_titles", TitleRequest),
    is_websocket=True,
)
