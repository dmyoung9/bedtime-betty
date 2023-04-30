from quart import Blueprint, request, jsonify

from beddybai.generation.generator import StoryGenerator

from ..database import db
from ..database.models import Artist, Author, Story, Theme, Title, Lesson

stories_blueprint = Blueprint("stories", __name__)


@stories_blueprint.route("/start", methods=["POST"])
async def start_new_story():
    data = await request.get_json()

    if not all(((age_min := data.get("age_min")), (age_max := data.get("age_max")))):
        return (
            {
                "error": "Missing required parameter(s)",
                "required_parameters": ["age_min", "age_max"],
            },
            400,
        )

    story = Story(age_min=age_min, age_max=age_max)

    db.session.add(story)
    db.session.commit()

    return jsonify({"message": "Story started", "story": story.id}), 201


@stories_blueprint.route("/themes", methods=["POST"])
async def generate_theme_suggestions():
    openai_api_key = request.headers.get("OPENAI_API_KEY")
    story_generator = StoryGenerator(openai_api_key)

    data = await request.get_json()

    return await story_generator.generate_story_themes(**data)


@stories_blueprint.route("/lessons", methods=["POST"])
async def generate_lesson_suggestions():
    openai_api_key = request.headers.get("OPENAI_API_KEY")
    story_generator = StoryGenerator(openai_api_key)

    data = await request.get_json()

    return await story_generator.generate_story_lessons(**(data or {}))


@stories_blueprint.route("/titles", methods=["POST"])
async def generate_title_suggestions():
    openai_api_key = request.headers.get("OPENAI_API_KEY")
    story_generator = StoryGenerator(openai_api_key)

    data = await request.get_json()

    return await story_generator.generate_story_titles(**(data or {}))


@stories_blueprint.route("/authors", methods=["POST"])
async def generate_author_suggestions():
    openai_api_key = request.headers.get("OPENAI_API_KEY")
    story_generator = StoryGenerator(openai_api_key)

    data = await request.get_json()

    return await story_generator.generate_author_styles(**(data or {}))


@stories_blueprint.route("/artists", methods=["POST"])
async def generate_artist_suggestions():
    openai_api_key = request.headers.get("OPENAI_API_KEY")
    story_generator = StoryGenerator(openai_api_key)

    data = await request.get_json()

    return await story_generator.generate_artist_styles(**(data or {}))


@stories_blueprint.route("/<int:story_id>/theme", methods=["PATCH"])
async def update_story_theme(story_id: int):
    data = (await request.get_json()) or {}

    if not all(
        ((emoji := data.get("emoji")), (story_theme := data.get("story_theme")))
    ):
        return (
            {
                "error": "Missing required parameter(s)",
                "required_parameters": ["emoji", "story_theme"],
            },
            400,
        )

    theme = Theme.query.filter_by(emoji=emoji, story_theme=story_theme).first()

    if not theme:
        theme = Theme(**data)

        db.session.add(theme)
        db.session.commit()

    story = Story.query.get_or_404(story_id)
    story.theme_id = theme.id

    db.session.commit()
    return story.to_json()


@stories_blueprint.route("/<int:story_id>/title", methods=["PATCH"])
async def update_story_title(story_id: int):
    data = (await request.get_json()) or {}

    if not (story_title := data.get("story_title")):
        return (
            {
                "error": "Missing required parameter(s)",
                "required_parameters": ["story_title"],
            },
            400,
        )

    title = Title.query.filter_by(story_title=story_title).first()

    if not title:
        title = Title(**data)

        db.session.add(title)
        db.session.commit()

    story = Story.query.get_or_404(story_id)
    story.title_id = title.id

    db.session.commit()
    return story.to_json()


@stories_blueprint.route("/<int:story_id>/lesson", methods=["PATCH"])
async def update_story_lesson(story_id: int):
    data = (await request.get_json()) or {}

    if not (story_lesson := data.get("story_lesson")):
        return (
            {
                "error": "Missing required parameter(s)",
                "required_parameters": ["story_lesson"],
            },
            400,
        )

    lesson = Lesson.query.filter_by(story_lesson=story_lesson).first()

    if not lesson:
        lesson = Lesson(**data)

        db.session.add(lesson)
        db.session.commit()

    story = Story.query.get_or_404(story_id)
    story.lesson_id = lesson.id

    db.session.commit()
    return story.to_json()


@stories_blueprint.route("/<int:story_id>/author", methods=["PATCH"])
async def update_story_author(story_id: int):
    data = (await request.get_json()) or {}

    if not all(
        (
            (author_name := data.get("author_name")),
            (author_style := data.get("author_style")),
        )
    ):
        return (
            {
                "error": "Missing required parameter(s)",
                "required_parameters": ["author_name", "author_style"],
            },
            400,
        )

    author = Author.query.filter_by(
        author_name=author_name, author_style=author_style
    ).first()

    if not author:
        author = Author(**data)

        db.session.add(author)
        db.session.commit()

    story = Story.query.get_or_404(story_id)
    story.author_id = author.id

    db.session.commit()
    return story.to_json()


@stories_blueprint.route("/<int:story_id>/artist", methods=["PATCH"])
async def update_story_artist(story_id: int):
    data = (await request.get_json()) or {}

    if not all(
        (
            (artist_name := data.get("artist_name")),
            (artist_style := data.get("artist_style")),
        )
    ):
        return (
            {
                "error": "Missing required parameter(s)",
                "required_parameters": ["artist_name", "artist_style"],
            },
            400,
        )

    artist = Artist.query.filter_by(
        artist_name=artist_name, artist_style=artist_style
    ).first()

    if not artist:
        artist = Artist(**data)

        db.session.add(artist)
        db.session.commit()

    story = Story.query.get_or_404(story_id)
    story.artist_id = artist.id

    db.session.commit()
    return story.to_json()
