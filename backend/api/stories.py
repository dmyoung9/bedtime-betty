from quart import Blueprint, request, jsonify

from pydantic import ValidationError

from ..validation import ItemIdRequest, StoryCreateRequest
from ..database import db
from ..database.models import Artist, Author, Serializer, Story, Idea, Title, Lesson, Page, to_dict

stories_blueprint = Blueprint("stories", __name__)
themes = []


@stories_blueprint.route("/", methods=["POST"])
async def create_story():
    data = await request.get_json()

    # try:
    story_request = StoryCreateRequest.parse_obj(data)
    # except ValidationError as ve:
    #     return {"error": str(ve)}, 400

    if not (
        artist := Artist.query.filter_by(
            artist_name=story_request.story_artist.artist_name,
            artist_style=story_request.story_artist.artist_style,
        ).first()
    ):
        artist = Artist(
            artist_name=story_request.story_artist.artist_name,
            artist_style=story_request.story_artist.artist_style,
        )
        db.session.add(artist)

    if not (
        author := Author.query.filter_by(
            author_name=story_request.story_author.author_name,
            author_style=story_request.story_author.author_style,
        ).first()
    ):
        author = Author(
            author_name=story_request.story_author.author_name,
            author_style=story_request.story_author.author_style,
        )
        db.session.add(author)

    if not (
        idea := Idea.query.filter_by(
            idea=story_request.story_idea.idea,
            emoji=story_request.story_idea.emoji,
        ).first()
    ):
        idea = Idea(
            idea=story_request.story_idea.idea,
            emoji=story_request.story_idea.emoji,
        )
        db.session.add(idea)

    if not (
        title := Title.query.filter_by(
            title=story_request.story_title.title,
        ).first()
    ):
        title = Title(
            title=story_request.story_title.title,
        )
        db.session.add(title)

    if not (
        lesson := Lesson.query.filter_by(
            lesson=story_request.story_lesson.lesson,
        ).first()
    ):
        lesson = Lesson(
            lesson=story_request.story_lesson.lesson,
        )
        db.session.add(lesson)

    db.session.commit()

    story = Story(
        pages=[Page(number=page.number, total=page.total, content=page.content, image=page.image) for page in story_request.story_pages],
        age=story_request.age,
        idea_id=idea.id,
        title_id=title.id,
        author_id=author.id,
        artist_id=artist.id,
        lesson_id=lesson.id,
    )
    db.session.add(story)
    db.session.commit()

    return jsonify({"message": "Story created", "story": story.id}), 201


@stories_blueprint.route("/<int:story_id>")
async def get_story(story_id: int):
    return jsonify(to_dict(Story.query.get_or_404(story_id)))
