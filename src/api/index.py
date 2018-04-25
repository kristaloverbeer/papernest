from flask import Blueprint
from flask_cors import CORS

index_blueprint = Blueprint('index_blueprint', __name__)
CORS(index_blueprint)


@index_blueprint.route('/', methods=['GET'])
@index_blueprint.route('/hello', methods=['GET'])
def hello():
    return 'It works!', 200
