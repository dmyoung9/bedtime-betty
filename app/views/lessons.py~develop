from quart import Blueprint

from app.views.views import GenerateItemsView, StreamItemsView

from ..models.validation.requests import LessonRequestModel

lessons_blueprint = Blueprint("lessons", __name__)

lessons_blueprint.add_url_rule(
    "/generate",
    view_func=GenerateItemsView.as_view("generate_lessons", LessonRequestModel),
)
lessons_blueprint.add_url_rule(
    "/stream",
    view_func=StreamItemsView.as_view("stream_lessons", LessonRequestModel),
    is_websocket=True,
)
