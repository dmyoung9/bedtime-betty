from quart import Blueprint

from app.api.views import GenerateItemsView, StreamItemsView

from ..validation import ArtistRequest

artists_blueprint = Blueprint("artists", __name__)

artists_blueprint.add_url_rule(
    "/generate", view_func=GenerateItemsView.as_view("generate_artists", ArtistRequest)
)
artists_blueprint.add_url_rule(
    "/stream",
    view_func=StreamItemsView.as_view("stream_artists", ArtistRequest),
    is_websocket=True,
)
