from quart import Blueprint

from betty.chat.api import ChatAPI
from betty.types.sections import Section

from .views import GenerateItemsView, get_auth_and_data, stream_response


sections_blueprint = Blueprint("sections", __name__)

sections_blueprint.add_url_rule(
    "/generate", view_func=GenerateItemsView.as_view("generate_sections", Section)
)

# sections_blueprint.add_url_rule(
#     "/stream/<int:id>",
#     view_func=StreamSectionsView.as_view("stream_sections_for_story", Section),
# )


@sections_blueprint.route("/stream", methods=["POST"])
async def stream_sections():
    api_key, data = await get_auth_and_data()
    chat_api = ChatAPI(ai_prefix="Betty", openai_api_key=api_key)

    item_request = Section.get_completion_request_model().parse_obj(data).dict()

    return stream_response(chat_api, Section, **item_request)
