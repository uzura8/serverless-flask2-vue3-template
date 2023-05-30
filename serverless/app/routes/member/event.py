import traceback
from flask import Blueprint, jsonify, request
from app.firebase import check_user_token
from app.models.dynamodb import Event, UserGame, UserEvent, ModelInvalidParamsException
from app.utils.error import InvalidUsage
from app.utils.request import validate_req_params
from app.validators import NormalizerUtils
from app.validators.schemas.common import ulid_schema
from app.routes.member import bp


def get_event(event_id):
    params = {'eventId': event_id}
    vals = validate_req_params(validation_schema_get_event_detail(), params)
    item = Event.get_one({'p': {'key': 'eventId', 'val': event_id}})
    if not item:
        raise InvalidUsage('Not Found', 404)

    return item


@bp.get('/events/')
@check_user_token
def get_member_events():
    # event = get_event(event_id)
    user_id = request.user.get('user_id')
    pkeys = {'key': 'userId', 'val': user_id}
    events = Event.get_all_by_pkey(pkeys, None, 'userIdIndex')
    return jsonify({'items': events}), 200


@bp.get('/events/<string:event_id>')
@check_user_token
def get_member_event(event_id):
    event = get_event(event_id)
    user_id = request.user.get('user_id')
    user_id_event_id = f'{user_id}#{event_id}'
    res = UserEvent.get_one(
        {'p': {'key': 'userIdEventId', 'val': user_id_event_id}})
    if not res:
        raise InvalidUsage('Not Found', 404)

    return jsonify(UserEvent.to_response(res)), 200


@bp.put('/events/<string:event_id>')
@check_user_token
def put_member_event(event_id):
    event = get_event(event_id)
    user_id = request.user.get('user_id')
    user_id_event_id = f'{user_id}#{event_id}'

    res = UserEvent.get_one(
        {'p': {'key': 'userIdEventId', 'val': user_id_event_id}})
    if res:
        raise InvalidUsage('Already exists', 400)

    vals = {'userId': user_id, 'eventId': event_id,
            'userIdEventId': user_id_event_id}
    try:
        res = UserEvent.create(vals)

    except ModelInvalidParamsException as e:
        raise InvalidUsage(e.message, 400)

    except Exception as e:
        print(traceback.format_exc())
        raise InvalidUsage('Server Error', 500)

    return jsonify(UserEvent.to_response(res)), 201


@bp.get('/events/<string:event_id>/games')
@check_user_token
def get_member_event_games(event_id):
    get_event(event_id)
    user_id = request.user.get('user_id')
    user_id_event_id = f'{user_id}#{event_id}'

    pkeys = {'key': 'userIdEventId', 'val': user_id_event_id}
    games = UserGame.get_all_by_pkey(pkeys, None, 'userIdEventIdIndex')
    res = [UserGame.to_response(g) for g in games]
    return jsonify(res), 200


def validation_schema_get_event_detail():
    return {
        'eventId': ulid_schema,
    }
