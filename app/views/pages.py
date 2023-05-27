from quart import Blueprint

from app.views.views import GenerateItemsView, StreamItemsView

from ..models.validation.requests import PageRequestModel

pages_blueprint = Blueprint("pages", __name__)

pages_blueprint.add_url_rule(
    "/generate", view_func=GenerateItemsView.as_view("generate_pages", PageRequestModel)
)
pages_blueprint.add_url_rule(
    "/stream",
    view_func=StreamItemsView.as_view("stream_pages", PageRequestModel),
    is_websocket=True,
)
