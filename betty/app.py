import asyncio
from typing import Union

from quart import Quart

from .views import api_blueprint

from .database import db
from .config import Config


async def create_app(config_name: Union[object, str]) -> Quart:
    app = Quart(__name__)
    app.config.from_object(config_name)

    db.init_app(app)
    async with app.app_context():
        db.create_all()

    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app


quart_app = asyncio.run(create_app(Config))
