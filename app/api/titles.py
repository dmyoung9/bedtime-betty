from quart import Blueprint, request, websocket

from .common import handle_generate_request, handle_stream_request
from ..validation import TitleRequest

titles_blueprint = Blueprint("titles", __name__)


@titles_blueprint.route("/generate", methods=["POST"])
async def generate_titles():
    return await handle_generate_request(request, TitleRequest)


@titles_blueprint.websocket("/stream")
async def stream_titles():
    while True:
        await handle_stream_request(websocket, TitleRequest)
