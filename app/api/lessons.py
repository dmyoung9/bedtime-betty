from quart import Blueprint

from app.api.views import GenerateItemsView, StreamItemsView

from ..validation import LessonRequest

lessons_blueprint = Blueprint("lessons", __name__)

lessons_blueprint.add_url_rule(
    "/generate", view_func=GenerateItemsView.as_view("generate_lessons", LessonRequest)
)
lessons_blueprint.add_url_rule(
    "/stream",
    view_func=StreamItemsView.as_view("stream_lessons", LessonRequest),
    is_websocket=True,
)
