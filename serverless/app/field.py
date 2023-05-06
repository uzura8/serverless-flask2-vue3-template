from flask import Blueprint, jsonify, request
from app.models.dynamodb import Field
#from app.utils.error import InvalidUsage
#from app.utils.request import validate_req_params
#from app.validators import NormalizerUtils

bp = Blueprint('field', __name__, url_prefix='/fields')


@bp.get('/')
def get_field_list():
    items = Field.scan()
    return jsonify({'items':items}), 200
