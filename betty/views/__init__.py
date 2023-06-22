from quart import Blueprint

from .covers import covers_blueprint
from .sections import sections_blueprint
from .stories import stories_blueprint


api_blueprint = Blueprint("api", __name__)

api_blueprint.register_blueprint(covers_blueprint, url_prefix="/covers")
api_blueprint.register_blueprint(sections_blueprint, url_prefix="/sections")
api_blueprint.register_blueprint(stories_blueprint, url_prefix="/stories")
