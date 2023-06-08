from quart import Blueprint

from betty.types.data import Lesson

from .views import GenerateItemsView, StreamItemsView


lessons_blueprint = Blueprint("lessons", __name__)

lessons_blueprint.add_url_rule(
    "/generate",
    view_func=GenerateItemsView.as_view("generate_lessons", Lesson),
)
lessons_blueprint.add_url_rule(
    "/stream",
    view_func=StreamItemsView.as_view("stream_lessons", Lesson),
    is_websocket=True,
)
