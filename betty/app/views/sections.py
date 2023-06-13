from quart import Blueprint

from betty.types.sections import Section

from .views import GenerateItemsView, StreamItemsView

sections_blueprint = Blueprint("sections", __name__)

sections_blueprint.add_url_rule(
    "/generate", view_func=GenerateItemsView.as_view("generate_sections", Section)
)
sections_blueprint.add_url_rule(
    "/stream",
    view_func=StreamItemsView.as_view("stream_sections", Section),
    is_websocket=True,
)
