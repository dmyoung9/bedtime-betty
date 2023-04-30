from quart import Blueprint

from .stories import stories_blueprint

api_blueprint = Blueprint("api", __name__)

api_blueprint.register_blueprint(stories_blueprint, url_prefix="/stories")
