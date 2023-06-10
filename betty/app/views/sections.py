from quart import Blueprint

from betty.types.data import Section

from .views import GenerateItemsView, StreamItemsView

sections_blueprint = Blueprint("sections", __name__)

sections_blueprint.add_url_rule(
    "/generate", view_func=GenerateItemsView.as_view("generate_stories", Section)
)
sections_blueprint.add_url_rule(
    "/stream",
    view_func=StreamItemsView.as_view("stream_stories", Section),
    is_websocket=True,
)
