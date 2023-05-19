from quart import Blueprint

from app.api.views import GenerateItemsView, StreamItemsView

from ..validation import ImageRequest

images_blueprint = Blueprint("images", __name__)

images_blueprint.add_url_rule(
    "/generate", view_func=GenerateItemsView.as_view("generate_images", ImageRequest)
)
images_blueprint.add_url_rule(
    "/stream",
    view_func=StreamItemsView.as_view("stream_images", ImageRequest),
    is_websocket=True,
)
