from quart import Blueprint

from app.views.views import GenerateItemsView, StreamItemsView

from ..models.validation import ArtistRequestModel

artists_blueprint = Blueprint("artists", __name__)

artists_blueprint.add_url_rule(
    "/generate",
    view_func=GenerateItemsView.as_view("generate_artists", ArtistRequestModel),
)
artists_blueprint.add_url_rule(
    "/stream",
    view_func=StreamItemsView.as_view("stream_artists", ArtistRequestModel),
    is_websocket=True,
)
