from quart import Blueprint

from .views import CreateItemsView, ListItemsView, RetrieveItemsView

from ..types.stories import Story


stories_blueprint = Blueprint("stories", __name__)

stories_blueprint.add_url_rule(
    "/", view_func=CreateItemsView.as_view("create_stories", Story)
)
stories_blueprint.add_url_rule(
    "/", view_func=ListItemsView.as_view("list_stories", Story)
)
stories_blueprint.add_url_rule(
    "/<int:id>", view_func=RetrieveItemsView.as_view("get_stories", Story)
)