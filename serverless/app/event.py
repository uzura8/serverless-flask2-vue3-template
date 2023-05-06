from flask import Blueprint, jsonify, request
from app.models.dynamodb import Event, Field
from app.utils.error import InvalidUsage
from app.utils.request import validate_req_params
from app.validators import NormalizerUtils

bp = Blueprint('event', __name__, url_prefix='/events')


def get_event(event_id):
    params = {'eventId':event_id}
    vals = validate_req_params(validation_schema_get_event_detail(), params)
    item = Event.get_one({'p': {'key':'eventId', 'val':event_id}})
    if not item:
        raise InvalidUsage('Not Found', 404)

    return item


@bp.get('/')
def get_event_list():
    items = Event.scan()
    return jsonify({'items':items}), 200


@bp.get('/<string:event_id>')
def get_event_detail(event_id):
    item = get_event(event_id)
    params = {'eventId':event_id}
    vals = validate_req_params(validation_schema_get_event_detail(), params)
    item = Event.get_one({'p': {'key':'eventId', 'val':event_id}})
    if not item:
        raise InvalidUsage('Not Found', 404)

    return jsonify(Event.to_response(item)), 200


@bp.route('/<string:event_id>', methods=['HEAD'])
def head_event_detail(event_id):
    get_event(event_id)
    return jsonify(), 200


def validation_schema_get_event_detail():
    return {
        'eventId': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': True,
            'empty': False,
            'length': 26,
            'valid_ulid': True,
        }
    }
