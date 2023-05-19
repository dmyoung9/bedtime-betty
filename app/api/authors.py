from quart import Blueprint, request, websocket

from .common import handle_generate_request, handle_stream_request
from ..validation import AuthorRequest

authors_blueprint = Blueprint("authors", __name__)


@authors_blueprint.route("/generate", methods=["POST"])
async def generate_authors():
    return await handle_generate_request(request, AuthorRequest)


@authors_blueprint.websocket("/stream")
async def stream_authors():
    while True:
        await handle_stream_request(websocket, AuthorRequest)
