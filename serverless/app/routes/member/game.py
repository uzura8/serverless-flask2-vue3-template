import traceback
from flask import Blueprint, jsonify, request
from app.firebase import check_user_token
from app.models.dynamodb import Game, Game, UserGame, ModelInvalidParamsException
from app.utils.error import InvalidUsage
from app.utils.request import validate_req_params
from app.validators import NormalizerUtils
from app.validators.schemas import ulid_schema
from app.routes.member import bp


def get_game(game_id):
    params = {'gameId': game_id}
    vals = validate_req_params(validation_schema_get_game_detail(), params)
    item = Game.get_one({'p': {'key': 'gameId', 'val': game_id}})
    if not item:
        raise InvalidUsage('Not Found', 404)

    return item


@bp.get('/games/')
@check_user_token
def get_member_games():
    # game = get_game(game_id)
    user_id = request.user.get('user_id')
    pkeys = {'key': 'userId', 'val': user_id}
    games = Game.get_all_by_pkey(pkeys, None, 'userIdIndex')
    return jsonify({'items': games}), 200


@bp.get('/games/<string:game_id>')
@check_user_token
def get_member_game(game_id):
    game = get_game(game_id)
    user_id = request.user.get('user_id')
    user_id_game_id = f'{user_id}#{game_id}'
    res = UserGame.get_one(
        {'p': {'key': 'userIdGameId', 'val': user_id_game_id}})
    if not res:
        raise InvalidUsage('Not Found', 404)

    return jsonify(UserGame.to_response(res)), 200


@bp.put('/games/<string:game_id>')
@check_user_token
def put_member_game(game_id):
    game = get_game(game_id)
    user_id = request.user.get('user_id')
    user_id_game_id = f'{user_id}#{game_id}'

    schema = validation_schema_put_game()
    vals = validate_req_params(schema, request.json)
    vals['gameId'] = game_id
    user_id = request.user.get('user_id')
    vals['userId'] = user_id
    # vals['userIdGameId'] = user_id_game_id

    res = UserGame.get_one(
        {'p': {'key': 'userIdGameId', 'val': user_id_game_id}})
    # if res:
    #    raise InvalidUsage('Already exists', 400)
    is_edit = bool(res)

    try:
        if is_edit:
            query_keys = {'p': {'key': 'userIdGameId', 'val': user_id_game_id}}
            res = UserGame.update(query_keys, vals, True)
        else:
            vals['userIdGameId'] = user_id_game_id
            res = UserGame.create(vals)

    except ModelInvalidParamsException as e:
        raise InvalidUsage(e.message, 400)

    except Exception as e:
        print(traceback.format_exc())
        raise InvalidUsage('Server Error', 500)

    return jsonify(UserGame.to_response(res)), 201


def validation_schema_get_game_detail():
    return {
        'gameId': ulid_schema,
    }


def validation_schema_put_game():
    return {
        'gameId': ulid_schema,
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
