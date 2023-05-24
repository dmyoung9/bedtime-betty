from quart import Blueprint

from app.views.views import GenerateItemsView, StreamItemsView

from ..models.validation.requests import DescriptionRequestModel

descriptions_blueprint = Blueprint("descriptions", __name__)

descriptions_blueprint.add_url_rule(
    "/generate",
    view_func=GenerateItemsView.as_view(
        "generate_descriptions", DescriptionRequestModel
    ),
)
descriptions_blueprint.add_url_rule(
    "/stream",
    view_func=StreamItemsView.as_view("stream_descriptions", DescriptionRequestModel),
    is_websocket=True,
)
