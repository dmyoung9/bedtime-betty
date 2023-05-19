from quart import Blueprint, request, websocket

from .common import handle_generate_request, handle_stream_request
from ..validation import LessonRequest

lessons_blueprint = Blueprint("lessons", __name__)


@lessons_blueprint.route("/generate", methods=["POST"])
async def generate_lessons():
    return await handle_generate_request(request, LessonRequest)


@lessons_blueprint.websocket("/stream")
async def stream_lessons():
    while True:
        await handle_stream_request(websocket, LessonRequest)
