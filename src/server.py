from flask import Flask

from src.api.index import index_blueprint
from src.api.ping import ping_blueprint
from src.api.v1.coverage import coverage_blueprint
from src.logging.mixin import LoggingMixin

logger = LoggingMixin().logger


def create_api():
    logger.info('[SETUP] API Application')

    api = Flask(__name__)

    api.url_map.strict_slashes = False

    _register_blueprints(api)

    logger.info('[DONE] API Application')
    return api


def _register_blueprints(api_application: Flask) -> None:
    api_application.register_blueprint(ping_blueprint)
    api_application.register_blueprint(index_blueprint)
    api_application.register_blueprint(coverage_blueprint)


api = create_api()
