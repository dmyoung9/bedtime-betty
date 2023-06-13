from quart import Blueprint

from betty.types.stories import StoryModel

from .views import CreateItemsView

stories_blueprint = Blueprint("stories", __name__)

stories_blueprint.add_url_rule(
    "/", view_func=CreateItemsView.as_view("create_stories", StoryModel)
)
# stories_blueprint.add_url_rule(
#     "/stream",
#     view_func=StreamItemsView.as_view("stream_stories", Section),
#     is_websocket=True,
# )
