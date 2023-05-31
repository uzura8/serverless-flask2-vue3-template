import traceback
from flask import Blueprint, jsonify, request
from app.firebase import check_user_token
from app.models.dynamodb import Event, Game, UserEvent, ModelInvalidParamsException
from app.utils.error import InvalidUsage
from app.utils.request import validate_req_params
from app.validators import NormalizerUtils
from app.validators.schemas.common import ulid_schema, get_list_schema
from app.validators.schemas.survalog import event_schema, game_schema

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
    return jsonify(Event.to_response(item)), 200


@bp.route('/<string:event_id>', methods=['HEAD'])
def head_event_detail(event_id):
    get_event(event_id)
    return jsonify(), 200


@bp.put('/<string:event_id>')
@check_user_token
def put_event(event_id):
    get_event(event_id)
    vals = validate_req_params(event_schema, request.json)
    user_id = request.user.get('user_id')
    if user_id:
        vals['createdBy'] = user_id
        vals['createdUserType'] = 'user'

    try:
        keys = {'p': {'key': 'eventId', 'val': event_id}}
        updated = Event.update(keys, vals, True)

    except ModelInvalidParamsException as e:
        raise InvalidUsage(e.message, 400)

    except Exception as e:
        print(traceback.format_exc())
        raise InvalidUsage('Server Error', 500)

    response = Event.to_response(updated)
    return jsonify(response), 201


@bp.post('/<string:event_id>/games')
@check_user_token
def post_event_game(event_id):
    get_event(event_id)
    schema = validation_schema_post_game()
    vals = validate_req_params(schema, request.json)
    vals['eventId'] = event_id

    user_id = request.user.get('user_id')
    if user_id:
        vals['createdBy'] = user_id
        vals['createdUserType'] = 'user'

    try:
        game = Game.create(vals, 'gameId')

    except ModelInvalidParamsException as e:
        raise InvalidUsage(e.message, 400)

    except Exception as e:
        print(traceback.format_exc())
        raise InvalidUsage('Server Error', 500)

    response = Game.to_response(game)
    return jsonify(response), 201


@bp.get('/<string:event_id>/games')
def get_event_game_list(event_id):
    get_event(event_id)
    params = validate_req_params(get_list_schema, request.args)
    pkeys = {'key': 'eventId', 'val': event_id}
    games = Game.get_all_by_pkey(pkeys, params, 'eventIdIndex')
    response = [Game.to_response(game) for game in games]
    return jsonify(response), 200


@bp.get('/<string:event_id>/users')
def get_event_member_list(event_id):
    get_event(event_id)
    pkeys = {'key': 'eventId', 'val': event_id}
    users = UserEvent.get_all_by_pkey(pkeys, None, 'eventIdIndex')
    res_items = [UserEvent.to_response(user) for user in users]
    return jsonify({'items': res_items}), 200


def validation_schema_get_event_detail():
    return {
        'eventId': ulid_schema,
    }


def validation_schema_post_game():
    schema = game_schema
    schema['eventId'] = ulid_schema
    return schema
