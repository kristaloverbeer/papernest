from flask import request, make_response, jsonify, Blueprint
from flask_cors import CORS

from src.database.schema.mobile_sites_schema import MobileSitesSchema
from src.logging.mixin import LoggingMixin
from src.repository.coverage_repository import CoverageRepository
from src.services.data_gouv_service import DataGouvService

logger = LoggingMixin().logger

coverage_blueprint = Blueprint('coverage_blueprint', __name__, url_prefix='/v1')
CORS(coverage_blueprint)


@coverage_blueprint.route('/coverage', methods=['GET'])
def coverage():
    given_address = request.args.get('q', type=str)

    geolocalisation_service = DataGouvService()
    mobile_sites_schema = MobileSitesSchema()
    coverage_repository = CoverageRepository(geolocalisation_service, mobile_sites_schema)

    providers_coverage_or_error_message, status_code = coverage_repository.get_coverage_information(given_address)

    return make_response(jsonify(providers_coverage_or_error_message), status_code)
