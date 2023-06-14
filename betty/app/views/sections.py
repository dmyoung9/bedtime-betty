from dataclasses import asdict
import json

from quart import Blueprint, websocket

from betty.chat.api import ChatAPI
from betty.database import db
from betty.types import Item
from betty.types.sections import Section, SectionDatabaseModel
from betty.types.stories import StoryDatabaseModel

from .views import GenerateItemsView, StreamItemsView

sections_blueprint = Blueprint("sections", __name__)


class StreamSectionsView(StreamItemsView):
    async def handle_existing_item(self, item: SectionDatabaseModel, **kwargs):
        section_item = Section(**item.to_dict())
        await super().handle_streamed_item(section_item, **kwargs)

    async def handle_streamed_item(self, item: Item, **kwargs):
        story_item = kwargs.pop("story_item")
        section_item = Section.get_database_model()(**asdict(item))
        section_item.story_id = story_item.id

        db.session.add(section_item)
        story_item.sections.append(section_item)

        db.session.commit()

        await super().handle_streamed_item(item, **kwargs)

    async def handle_stream_request(self, **kwargs):
        message = await websocket.receive()
        data = json.loads(message)

        if data.get("type") == "request":
            story_item = StoryDatabaseModel.query.get_or_404(kwargs.get("id"))
            start = json.dumps({"type": "start"})
            await websocket.send(start)
            print(start)

            if story_item.sections:
                for section in story_item.sections:
                    await self.handle_existing_item(
                        section,
                        **kwargs,
                    )
            else:
                item_request = story_item.to_dict()

                story_generator = ChatAPI(
                    ai_prefix="Betty", openai_api_key=data.pop("api_key", "")
                )

                await story_generator.stream(
                    self.item_type,
                    **item_request,
                    callback_func=self.handle_streamed_item,
                    callback_kwargs={"story_item": story_item, **kwargs},
                )

            end = json.dumps({"type": "end"})
            await websocket.send(end)
            print(end)


sections_blueprint.add_url_rule(
    "/generate", view_func=GenerateItemsView.as_view("generate_sections", Section)
)
sections_blueprint.add_url_rule(
    "/stream",
    view_func=StreamItemsView.as_view("stream_sections", Section),
    is_websocket=True,
)
sections_blueprint.add_url_rule(
    "/stream/<int:id>",
    view_func=StreamSectionsView.as_view("stream_sections_for_story", Section),
    is_websocket=True,
)
