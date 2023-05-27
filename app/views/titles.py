from quart import Blueprint

from app.views.views import GenerateItemsView, StreamItemsView

from ..models.validation.requests import TitleRequestModel

titles_blueprint = Blueprint("titles", __name__)

titles_blueprint.add_url_rule(
    "/generate",
    view_func=GenerateItemsView.as_view("generate_titles", TitleRequestModel),
)
titles_blueprint.add_url_rule(
    "/stream",
    view_func=StreamItemsView.as_view("stream_titles", TitleRequestModel),
    is_websocket=True,
)
