from flask import Blueprint, jsonify, request
from app.models.dynamodb import Field, Event
from app.utils.error import InvalidUsage
from app.utils.request import validate_req_params
from app.validators import NormalizerUtils

bp = Blueprint('field', __name__, url_prefix='/fields')


def get_field(field_id):
    params = {'fieldId':field_id}
    vals = validate_req_params(validation_schema_get_field_detail(), params)
    item = Field.get_one({'p': {'key':'fieldId', 'val':field_id}})
    if not item:
        raise InvalidUsage('Not Found', 404)

    return item


@bp.get('/')
def get_field_list():
    items = Field.scan()
    return jsonify({'items':items}), 200


@bp.get('/<string:field_id>')
def get_field_detail(field_id):
    item = get_field(field_id)
    return jsonify(Field.to_response(item)), 200


@bp.get('/<string:field_id>/events/<string:date>')
def get_field_detail_event_list(field_id, date):
    field = get_field(field_id)
    pkeys = {'key':'fieldIdDate', 'val':f'{field_id}#{date}'}
    events = Event.get_all_by_pkey(pkeys, None, 'FieldIdDateIndex')
    events_response = [Event.to_response(event) for event in events]
    return jsonify(Field.to_response(events_response)), 200


@bp.route('/<string:field_id>', methods=['HEAD'])
def head_field_detail(field_id):
    get_field(field_id)
    return jsonify(), 200


def validation_schema_get_field_detail():
    return {
        'fieldId': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': True,
            'empty': False,
            'valid_ulid': True,
        }
    }
