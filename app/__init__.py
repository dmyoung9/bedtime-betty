from typing import Union
from quart import Quart

# from quart_cors import cors

from .api import api_blueprint

# from .database import db
from .config import Config


CORS_CONFIG = {
    "allow_origin": [
        "http://bedtime-betty.com",
        "http://www.bedtime-betty.com",
        "127.0.0.1",
    ],
    "allow_headers": ["Content-Type", "Authorization"],
}


def create_app(config_name: Union[object, str]) -> Quart:
    app = Quart(__name__)
    app.config.from_object(config_name)

    # app = cors(app, **CORS_CONFIG)

    # db.init_app(app)
    # async with app.app_context():
    #     db.create_all()

    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app


quart_app = create_app(Config)


# @quart_app.route("/", methods=["GET"])
# async def index():
#     return await render_template("/base.html")


# @quart_app.route("/stories", methods=["GET"])
# async def stories():
#     return await render_template(
#         "/stories.html",
#         base_api_url=Config.BASE_API_URL,
#         ssl_enabled=Config.SSL_ENABLED,
#     )


# @quart_app.route("/settings", methods=["GET"])
# async def settings():
#     return await render_template("/settings.html")
