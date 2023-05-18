from quart import Blueprint

from .ideas import ideas_blueprint
from .lessons import lessons_blueprint

api_blueprint = Blueprint("api", __name__)

api_blueprint.register_blueprint(ideas_blueprint, url_prefix="/ideas")
api_blueprint.register_blueprint(lessons_blueprint, url_prefix="/lessons")
