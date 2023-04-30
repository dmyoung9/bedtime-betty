import asyncio

from quart import Quart, render_template
from quart_cors import cors

from .api import api_blueprint
from .database import db
from .config import Config


CORS_CONFIG = {
    "allow_origin": "*",
    "allow_headers": "*",
    "allow_methods": "*",
    "allow_credentials": False,
}


async def create_app(config_name):
    app = Quart(__name__)
    app.config.from_object(config_name)

    app = cors(app, **CORS_CONFIG)

    db.init_app(app)
    async with app.app_context():
        db.create_all()

    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app


quart_app = asyncio.run(create_app(Config))


@quart_app.route("/", methods=["GET"])
async def index():
    return await render_template("/index.html")


@quart_app.route("/preferences", methods=["GET"])
async def preferences():
    return await render_template("/preferences.html")
