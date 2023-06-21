import asyncio
from dataclasses import asdict
import json
from queue import Empty, Queue
from threading import Thread

from quart import Blueprint

from betty.chat.api import ChatAPI
from betty.types.covers import Cover

from .views import GenerateItemsView, get_auth_and_data

covers_blueprint = Blueprint("covers", __name__)

covers_blueprint.add_url_rule(
    "/generate", view_func=GenerateItemsView.as_view("generate_covers", Cover)
)
# covers_blueprint.add_url_rule(
#     "/stream",
#     view_func=StreamItemsView.as_view("stream_covers", Cover),
# )


@covers_blueprint.route("/stream", methods=["POST"])
async def stream_covers():
    api_key, data = await get_auth_and_data()
    chat_api = ChatAPI(ai_prefix="Betty", openai_api_key=api_key)

    def stream(*args, **kwargs):
        queue = Queue()
        job_done = object()
        queue.put(job_done)

        chat_thread = Thread(
            target=asyncio.run,
            args=(chat_api.stream(*args, queue=queue, **kwargs),),
        )
        chat_thread.start()

        while True:
            try:
                next_obj = queue.get(True, timeout=1)
                if next_obj is job_done:
                    if not chat_thread.is_alive():
                        break
                    continue

                json_obj = json.dumps(asdict(next_obj))
                yield f"{json_obj}\n"
            except Empty:
                if not chat_thread.is_alive():
                    break
                continue

    item_request = Cover.get_completion_request_model().parse_obj(data).dict()

    return stream(Cover, **item_request)
