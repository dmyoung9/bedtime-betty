from quart import Blueprint

from app.views.views import GenerateItemsView, StreamItemsView

from ..models.validation.requests import ImageRequestModel

images_blueprint = Blueprint("images", __name__)

images_blueprint.add_url_rule(
    "/generate",
    view_func=GenerateItemsView.as_view("generate_images", ImageRequestModel),
)
images_blueprint.add_url_rule(
    "/stream",
    view_func=StreamItemsView.as_view("stream_images", ImageRequestModel),
    is_websocket=True,
)
