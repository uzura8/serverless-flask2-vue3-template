import traceback
from flask import Blueprint, jsonify, request
from app.firebase import check_user_token
from app.models.dynamodb import Field, Event, ModelInvalidParamsException
from app.utils.error import InvalidUsage
from app.utils.request import validate_req_params
from app.validators import NormalizerUtils

bp = Blueprint('field', __name__, url_prefix='/fields')


def get_field(field_id):
    params = {'fieldId': field_id}
    vals = validate_req_params(validation_schema_get_field_detail(), params)
    item = Field.get_one({'p': {'key': 'fieldId', 'val': field_id}})
    if not item:
        raise InvalidUsage('Not Found', 404)

    return item


@bp.get('/')
def get_field_list():
    items = Field.scan()
    return jsonify({'items': items}), 200


@bp.get('/<string:field_id>')
def get_field_detail(field_id):
    item = get_field(field_id)
    return jsonify(Field.to_response(item)), 200


@bp.post('/<string:field_id>/events')
@check_user_token
def post_field_event(field_id):
    field = get_field(field_id)
    schema = validation_schema_post_event()
    vals = validate_req_params(schema, request.json)
    vals['fieldId'] = field_id
    vals['fieldIdDate'] = f'{field_id}#{vals["date"]}'
    vals['fieldName'] = field.get('name')

    user_id = request.user.get('user_id')
    if user_id:
        vals['createdBy'] = user_id
        vals['createdUserType'] = 'user'

    try:
        event = Event.create(vals, 'eventId')

    except ModelInvalidParamsException as e:
        raise InvalidUsage(e.message, 400)

    except Exception as e:
        print(traceback.format_exc())
        raise InvalidUsage('Server Error', 500)

    event_response = Event.to_response(event)
    return jsonify(event_response), 201


@bp.get('/<string:field_id>/events/<string:date>')
def get_field_detail_event_list(field_id, date):
    field = get_field(field_id)
    pkeys = {'key': 'fieldIdDate', 'val': f'{field_id}#{date}'}
    events = Event.get_all_by_pkey(pkeys, None, 'fieldIdDateIndex')
    events_response = [Event.to_response(event) for event in events]
    return jsonify(events_response), 200


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


def validation_schema_post_event():
    return {
        'fieldId': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': True,
            'empty': False,
            'valid_ulid': True,
        },
        'date': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': True,
            'empty': False,
            'regex': r'^\d{4}\d{2}\d{2}$'
        },
        'name': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': True,
            'empty': False,
        },
        'body': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': False,
            'empty': True,
        },
        'eventType': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': True,
            'allowed': ['regular', 'exclusive', 'others'],
        },
        'joinedCount': {
            'type': 'integer',
            'coerce': int,
            'required': False,
            'empty': True,
            'nullable': True,
        },
        'weatherType': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': False,
            'empty': True,
            'nullable': True,
            'allowed': [
                'clear',
                'cloudy',
                'cloudyOccasionallyClear',
                'rain',
                'heavyRain',
                'cloudyOccasionallyRain',
                'snow',
                'sleet'
            ],
        },
        'weatherText': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': False,
            'empty': True,
            'nullable': True,
        },
        'windType': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': False,
            'empty': True,
            'nullable': True,
            'allowed': ['calm', 'light', 'moderate', 'strong', 'gale'],
        },
        'temperature': {
            'type': 'integer',
            'coerce': int,
            'required': False,
            'empty': True,
            'nullable': True,
        },
        # 'temperatureUnit': {
        #    'type': 'string',
        #    'coerce': (str, NormalizerUtils.trim),
        #    'required': False,
        #    'allowed': ['celsius', 'fahrenheit'],
        # },
    }
