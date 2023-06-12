from quart import Blueprint

# from .artists import artists_blueprint
# from .authors import authors_blueprint
from .ideas import ideas_blueprint

# from .lessons import lessons_blueprint
# from .covers import covers_blueprint
# from .sections import sections_blueprint
# from .stories import stories_blueprint

# from .titles import titles_blueprint
# from .pages import pages_blueprint
# from .images import images_blueprint
# from .descriptions import descriptions_blueprint

api_blueprint = Blueprint("api", __name__)

api_blueprint.register_blueprint(ideas_blueprint, url_prefix="/ideas")
# api_blueprint.register_blueprint(lessons_blueprint, url_prefix="/lessons")
# api_blueprint.register_blueprint(authors_blueprint, url_prefix="/authors")
# api_blueprint.register_blueprint(artists_blueprint, url_prefix="/artists")
# api_blueprint.register_blueprint(covers_blueprint, url_prefix="/covers")
# api_blueprint.register_blueprint(sections_blueprint, url_prefix="/sections")
# api_blueprint.register_blueprint(stories_blueprint, url_prefix="/stories")
# api_blueprint.register_blueprint(titles_blueprint, url_prefix="/titles")
# api_blueprint.register_blueprint(pages_blueprint, url_prefix="/pages")
# api_blueprint.register_blueprint(images_blueprint, url_prefix="/images")
# api_blueprint.register_blueprint(descriptions_blueprint, url_prefix="/descriptions")
