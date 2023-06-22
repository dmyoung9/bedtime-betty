from quart import Blueprint, jsonify

from .views import GenerateItemsView, get_auth_and_data, stream_response

from ..chat.api import ChatAPI
from ..types.sections import Section
from ..types.stories import Story


sections_blueprint = Blueprint("sections", __name__)

sections_blueprint.add_url_rule(
    "/generate", view_func=GenerateItemsView.as_view("generate_sections", Section)
)


@sections_blueprint.route("/stream", methods=["POST"])
async def stream_sections():
    api_key, data = await get_auth_and_data()
    chat_api = ChatAPI(ai_prefix="Betty", openai_api_key=api_key)

    item_request = Section.get_completion_request_model().parse_obj(data).dict()

    return stream_response(chat_api, Section, **item_request)


@sections_blueprint.route("/for_story/<int:id>", methods=["GET"])
async def section_for_story(id: int):
    story_item = Story.get_database_model().query.get_or_404(id)

    return jsonify([section.to_dict() for section in story_item.sections])
