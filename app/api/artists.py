from quart import Blueprint, request, websocket

from .common import handle_generate_request, handle_stream_request
from ..validation import ArtistRequest

artists_blueprint = Blueprint("artists", __name__)


@artists_blueprint.route("/generate", methods=["POST"])
async def generate_artists():
    return await handle_generate_request(request, ArtistRequest)


@artists_blueprint.websocket("/stream")
async def stream_artists():
    while True:
        await handle_stream_request(websocket, ArtistRequest)
