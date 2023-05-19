from quart import Blueprint, request, websocket

from .common import handle_generate_request, handle_stream_request
from ..validation import IdeaRequest

ideas_blueprint = Blueprint("ideas", __name__)


@ideas_blueprint.route("/generate", methods=["POST"])
async def generate_ideas():
    return await handle_generate_request(request, IdeaRequest)


@ideas_blueprint.websocket("/stream")
async def stream_ideas():
    while True:
        await handle_stream_request(websocket, IdeaRequest)
