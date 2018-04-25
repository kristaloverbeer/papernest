from flask import Blueprint
from flask_cors import CORS

ping_blueprint = Blueprint('ping_blueprint', __name__)
CORS(ping_blueprint)


@ping_blueprint.route('/ping', methods=['GET'])
def ping():
    return 'pong', 200
