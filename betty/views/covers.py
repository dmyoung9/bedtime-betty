from quart import Blueprint

from .views import GenerateItemsView, get_auth_and_data, stream_response

from ..chat.api import ChatAPI
from ..types.covers import Cover


covers_blueprint = Blueprint("covers", __name__)

covers_blueprint.add_url_rule(
    "/generate", view_func=GenerateItemsView.as_view("generate_covers", Cover)
)


@covers_blueprint.route("/stream", methods=["POST"])
async def stream_covers():
    api_key, data = await get_auth_and_data()
    chat_api = ChatAPI(ai_prefix="Betty", openai_api_key=api_key)

    item_request = Cover.get_completion_request_model().parse_obj(data).dict()

    return stream_response(chat_api, Cover, **item_request)
