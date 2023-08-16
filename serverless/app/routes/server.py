import traceback
from flask import Blueprint, jsonify, request
from app.routes import check_firebase_auth_or_pgit_client_ip
from app.models.dynamodb import Server, Repository, ModelInvalidParamsException, ModelConditionalCheckFailedException
from app.utils.error import InvalidUsage
from app.utils.request import validate_params
from app.utils.date import utc_iso
from app.utils.string import sanitize_domain_str
from app.validators import NormalizerUtils
from app.validators.schemas.common import get_list_schema

bp = Blueprint('server', __name__, url_prefix='/servers')


# @bp.before_request
# @site_before_request
# def before_request():
#     pass


@bp.get('/')
@check_firebase_auth_or_pgit_client_ip
def get_server_list():
    vals = validate_params(get_list_schema, request.args.to_dict())
    res = {}
    items = Server.scan()
    res['items'] = sorted(items, key=lambda x: x['createdAt'], reverse=True)
    return jsonify(res), 200


@bp.get('/<string:domain>')
@check_firebase_auth_or_pgit_client_ip
def get_server(domain):
    server = get_server_by_domain(domain)
    return jsonify(server), 200


@bp.put('/<string:domain>/deploy/<string:status>')
@check_firebase_auth_or_pgit_client_ip
def check_and_update_server_status(domain, status):
    if status not in ['start', 'finish']:
        raise InvalidUsage('Invalid status', 400)

    server = get_server_by_domain(domain)
    if status == 'start':
        if server['isExecuting'] == '1':
            raise InvalidUsage('Locked', 423)
        upd_vals = {'isExecuting': '1'}
        cond_vals = {'isExecuting': '0'}

    elif status == 'finish':
        if server['isExecuting'] == '0':
            raise InvalidUsage('Not Locked', 400)
        upd_vals = {'isExecuting': '0'}
        cond_vals = {'isExecuting': '1'}

    keys = {'domain': domain}
    try:
        server = Server.update_by_conds(keys, upd_vals, cond_vals, True)

    except ModelInvalidParamsException as e:
        raise InvalidUsage(e.message, 400)

    except ModelConditionalCheckFailedException as e:
        raise InvalidUsage(e.message, 400)

    except Exception as e:
        print(traceback.format_exc())
        raise InvalidUsage('Server Error', 500)

    return jsonify(server), 200


@bp.delete('/<string:domain>')
@check_firebase_auth_or_pgit_client_ip
def delete_server(domain):
    pass


@bp.get('/<string:domain>/repositories')
@check_firebase_auth_or_pgit_client_ip
def get_repo_list(domain):
    server = get_server_by_domain(domain)
    vals = validate_params(schema_get_reps(), request.args.to_dict())

    keys = {'serverDomain': domain}
    skey_cond_type = 'eq'
    if vals.get('status'):
        keys['deployStatusUpdatedAt'] = vals['status']
        skey_cond_type = 'begins_with'
    res = Repository.get_all_pager(
        keys, vals, 'serverDomain_idx', False, skey_cond_type)
    return jsonify(res), 200


def get_server_by_domain(domain):
    server = Server.get_one({'domain': domain})
    if not server:
        raise InvalidUsage('Not Found', 404)
    return server


def schema_get_reps():
    base = get_list_schema
    schema = {
        'status': {
            'type': 'string',
            'coerce': (NormalizerUtils.trim),
            'required': False,
            'empty': True,
            'nullable': True,
            'allowed': Repository.allowed_vals['deployStatus'],
        },
    }
    return base | schema
