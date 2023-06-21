from quart import Blueprint

from betty.types.sections import Section

from .views import GenerateItemsView

sections_blueprint = Blueprint("sections", __name__)


# class StreamSectionsView(StreamItemsView):
#     async def handle_existing_item(self, item: SectionDatabaseModel, **kwargs):
#         section_item = Section(**item.to_dict())
#         await super().handle_streamed_item(section_item, **kwargs)

#     async def handle_streamed_item(self, item: Item, **kwargs):
#         story_item = kwargs.pop("story_item")
#         section_item = Section.get_database_model()(**asdict(item))
#         section_item.story_id = story_item.id

#         db.session.add(section_item)
#         story_item.sections.append(section_item)

#         db.session.commit()

#         await super().handle_streamed_item(item, **kwargs)

#     async def handle_stream_request(self, data, **kwargs):
#         story_item = StoryDatabaseModel.query.get_or_404(kwargs.get("id"))

#         if story_item.sections:
#             for section in story_item.sections:
#                 await self.handle_existing_item(
#                     section,
#                     **kwargs,
#                 )
#         else:
#             await super().handle_stream_request(
#                 story_item.to_dict(), **{"story_item": story_item, **kwargs}
#             )


sections_blueprint.add_url_rule(
    "/generate", view_func=GenerateItemsView.as_view("generate_sections", Section)
)
# sections_blueprint.add_url_rule(
#     "/stream",
#     view_func=StreamItemsView.as_view("stream_sections", Section),
# )
# sections_blueprint.add_url_rule(
#     "/stream/<int:id>",
#     view_func=StreamSectionsView.as_view("stream_sections_for_story", Section),
# )
