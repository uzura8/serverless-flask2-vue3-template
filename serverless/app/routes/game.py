import traceback
from flask import Blueprint, jsonify, request
from app.firebase import check_user_token
from app.models.dynamodb import Game, UserGame, ModelInvalidParamsException
from app.utils.error import InvalidUsage
from app.utils.request import validate_req_params
from app.validators import NormalizerUtils
from app.validators.schemas.common import ulid_schema
from app.validators.schemas.survalog import game_schema

bp = Blueprint('game', __name__, url_prefix='/games')


def get_game(game_id):
    params = {'gameId': game_id}
    vals = validate_req_params(validation_schema_get_game_detail(), params)
    item = Game.get_one({'p': {'key': 'gameId', 'val': game_id}})
    if not item:
        raise InvalidUsage('Not Found', 404)

    return item


@bp.get('/')
def get_game_list():
    items = Game.scan()
    return jsonify({'items': items}), 200


@bp.get('/<string:game_id>')
def get_game_detail(game_id):
    item = get_game(game_id)
    return jsonify(Game.to_response(item)), 200


@bp.route('/<string:game_id>', methods=['HEAD'])
def head_game_detail(game_id):
    get_game(game_id)
    return jsonify(), 200


@bp.put('/<string:game_id>')
@check_user_token
def put_game(game_id):
    get_game(game_id)
    vals = validate_req_params(game_schema, request.json)
    user_id = request.user.get('user_id')
    if user_id:
        vals['createdBy'] = user_id
        vals['createdUserType'] = 'user'

    try:
        keys = {'p': {'key': 'gameId', 'val': game_id}}
        updated = Game.update(keys, vals, True)

    except ModelInvalidParamsException as e:
        raise InvalidUsage(e.message, 400)

    except Exception as e:
        print(traceback.format_exc())
        raise InvalidUsage('Server Error', 500)

    response = Game.to_response(updated)
    return jsonify(response), 201


@bp.get('/<string:game_id>/users')
def get_game_user_list(game_id):
    get_game(game_id)
    pkeys = {'key': 'gameId', 'val': game_id}
    items = UserGame.get_all_by_pkey(pkeys, None, 'gameIdIndex')
    return jsonify({'items': items}), 200


@bp.post('/<string:game_id>/users')
@check_user_token
def post_game_user(game_id):
    get_game(game_id)
    schema = validation_schema_post_game_user()
    vals = validate_req_params(schema, request.json)
    vals['gameId'] = game_id

    user_id = request.user.get('user_id')
    if user_id:
        vals['userId'] = user_id

    try:
        game_user = UserGame.create(vals, 'gameUserId')

    except ModelInvalidParamsException as e:
        raise InvalidUsage(e.message, 400)

    except Exception as e:
        print(traceback.format_exc())
        raise InvalidUsage('Server Error', 500)

    response = UserGame.to_response(game_user)
    return jsonify(response), 201


def validation_schema_get_game_detail():
    return {
        'gameId': ulid_schema,
    }


def validation_schema_post_game_user():
    return {
        'gameUserId': ulid_schema,
        'gameId': ulid_schema,
        'userId': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': True,
            'empty': False,
            'regex': r'^[a-zA-Z0-9]{28,32}$',
        },
        'killCount': {
            'type': 'integer',
            'coerce': int,
            'required': False,
            'empty': True,
            'nullable': True,
        },
        'deathCount': {
            'type': 'integer',
            'coerce': int,
            'required': False,
            'empty': True,
            'nullable': True,
        },
        'isFlugGet': {
            'type': 'boolean',
            'coerce': bool,
            'required': False,
            'empty': True,
            'nullable': True,
            'default': False,
        },
        'gameMemo': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': False,
            'empty': True,
            'nullable': True,
        },
    }
