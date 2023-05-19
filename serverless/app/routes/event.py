import traceback
from flask import Blueprint, jsonify, request
from app.models.dynamodb import Event, Game, ModelInvalidParamsException
from app.utils.error import InvalidUsage
from app.utils.request import validate_req_params
from app.validators import NormalizerUtils

bp = Blueprint('event', __name__, url_prefix='/events')


def get_event(event_id):
    params = {'eventId': event_id}
    vals = validate_req_params(validation_schema_get_event_detail(), params)
    item = Event.get_one({'p': {'key': 'eventId', 'val': event_id}})
    if not item:
        raise InvalidUsage('Not Found', 404)

    return item


@bp.get('/')
def get_event_list():
    items = Event.scan()
    return jsonify({'items': items}), 200


@bp.get('/<string:event_id>')
def get_event_detail(event_id):
    item = get_event(event_id)
    params = {'eventId': event_id}
    vals = validate_req_params(validation_schema_get_event_detail(), params)
    item = Event.get_one({'p': {'key': 'eventId', 'val': event_id}})
    if not item:
        raise InvalidUsage('Not Found', 404)

    return jsonify(Event.to_response(item)), 200


@bp.route('/<string:event_id>', methods=['HEAD'])
def head_event_detail(event_id):
    get_event(event_id)
    return jsonify(), 200


@bp.post('/<string:event_id>/games')
def post_event_game(event_id):
    field = get_event(event_id)
    schema = validation_schema_post_game()
    vals = validate_req_params(schema, request.json)
    vals['eventId'] = event_id
    # created_by = current_cognito_jwt.get('cognito:username', '')
    # if created_by:
    #    vals['createdBy'] = created_by

    try:
        event = Game.create(vals, 'gameId')

    except ModelInvalidParamsException as e:
        raise InvalidUsage(e.message, 400)

    except Exception as e:
        print(traceback.format_exc())
        raise InvalidUsage('Server Error', 500)

    event_response = Event.to_response(event)
    return jsonify(event_response), 201


@bp.get('/<string:event_id>/games')
def get_event_game_list(event_id):
    field = get_event(event_id)
    pkeys = {'key': 'eventId', 'val': event_id}
    games = Game.get_all_by_pkey(pkeys, None, 'eventIdIndex')
    response = [Game.to_response(game) for game in games]
    return jsonify(response), 200


ulid_schema = {
    'type': 'string',
    'coerce': (str, NormalizerUtils.trim),
    'required': True,
    'empty': False,
    'valid_ulid': True,
}


def validation_schema_get_event_detail():
    return {
        'eventId': ulid_schema,
    }


def validation_schema_post_game():
    return {
        'eventId': ulid_schema,
        'name': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': False,
            'empty': True,
            'nullable': True,
        },
        'body': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': False,
            'empty': False,
            'nullable': True,
        },
        'gameType': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': True,
            'empty': False,
        },
        'gameTypeText': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': False,
            'empty': True,
            'nullable': True,
        },
        'joinedCount': {
            'type': 'integer',
            'coerce': int,
            'required': False,
            'empty': True,
            'nullable': True,
        },
        'duration': {
            'type': 'integer',
            'coerce': int,
            'required': False,
            'empty': True,
            'nullable': True,
        },
        'durationText': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': False,
            'allowed': ['min', 'hour', 'day'],
        },
        # 'createdBy': {
        #    'type': 'string',
        #    'coerce': (str, NormalizerUtils.trim),
        #    'required': True,
        #    'empty': False,
        # },
    }