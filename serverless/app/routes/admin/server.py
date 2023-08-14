import traceback
from flask import jsonify, request
from flask_cognito import cognito_auth_required, current_cognito_jwt
from app.models.dynamodb import Server, ModelInvalidParamsException, ModelConditionalCheckFailedException
from app.utils.error import InvalidUsage
from app.utils.request import validate_params
from app.utils.date import utc_iso
from app.utils.string import sanitize_domain_str
from app.validators import NormalizerUtils
from app.validators.schemas.common import get_list_schema
from app.routes.admin import bp, site_before_request, admin_role_editor_required


@bp.before_request
@site_before_request
def before_request():
    pass


@bp.get('/servers')
@cognito_auth_required
@admin_role_editor_required
def get_server_list():
    vals = validate_params(get_list_schema, request.args.to_dict())
    res = {}
    items = Server.scan()
    res['items'] = sorted(items, key=lambda x: x['createdAt'], reverse=True)
    return jsonify(res), 200


@bp.get('/servers/<string:domain>')
@cognito_auth_required
@admin_role_editor_required
def get_server(domain):
    server = get_server_by_domain(domain)
    return jsonify(server), 200


@bp.put('/servers/<string:domain>/deploy/<string:status>')
@cognito_auth_required
@admin_role_editor_required
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


@bp.delete('/servers/<string:domain>')
@cognito_auth_required
@admin_role_editor_required
def delete_server(domain):
    pass


def get_server_by_domain(domain):
    server = Server.get_one({'domain': domain})
    if not server:
        raise InvalidUsage('Not Found', 404)
    return server
