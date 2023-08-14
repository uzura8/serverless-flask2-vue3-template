import traceback
from flask import jsonify, request
from flask_cognito import cognito_auth_required, current_cognito_jwt
from app.models.dynamodb import Repository, ModelInvalidParamsException
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


@bp.get('/repositories')
@cognito_auth_required
@admin_role_editor_required
def get_repo_list():
    vals = validate_params(get_list_schema, request.args.to_dict())
    res = {}
    if vals.get('server'):
        keys = {'serverDomain': vals['server']}
        index = 'serverDomain_idx'
        res = Repository.get_all_pager(keys, vals, index)
    else:
        items = Repository.scan()
        res['items'] = sorted(
            items, key=lambda x: x['createdAt'], reverse=True)
    return jsonify(res), 200


@bp.post('/repositories')
@cognito_auth_required
@admin_role_editor_required
def create_repo():
    vals = validate_params(schema_post(), request.json)
    vals['repoId'] = generate_repo_id(
        vals['serviceDomain'], vals['serviceSegment'], vals['repoName'])
    exists = Repository.get_one({'repoId': vals['repoId']})
    if exists:
        raise InvalidUsage('Already exists', 400)

    status = 'pending'
    vals['deployStatus'] = status
    created_by = current_cognito_jwt.get('cognito:username', '')
    if created_by:
        vals['createdBy'] = created_by

    add_datetime = utc_iso()
    vals['updatedAt'] = add_datetime
    vals['deployStatusUpdatedAt'] = '#'.join([status, add_datetime])

    try:
        repo = Repository.create(vals, None, True)

    except ModelInvalidParamsException as e:
        raise InvalidUsage(e.message, 400)

    except Exception as e:
        print(traceback.format_exc())
        raise InvalidUsage('Server Error', 500)

    return jsonify(repo), 201


@bp.get('/repositories/<string:repo_id>')
@cognito_auth_required
@admin_role_editor_required
def get_repo(repo_id):
    repo = get_repo_by_repo_id(repo_id)
    return jsonify(repo), 200


@bp.put('/repositories/<string:repo_id>')
@cognito_auth_required
@admin_role_editor_required
def update_repo(repo_id):
    repo = get_repo_by_repo_id(repo_id)
    vals = validate_params(schema_post(), request.json)
    vals['updatedBy'] = current_cognito_jwt.get('cognito:username', '')
    try:
        repo = Repository.update({'repoId': repo_id}, vals, True)

    except ModelInvalidParamsException as e:
        raise InvalidUsage(e.message, 400)

    except Exception as e:
        print(traceback.format_exc())
        raise InvalidUsage('Server Error', 500)

    return jsonify(repo), 200


@bp.delete('/repositories/<string:repo_id>')
@cognito_auth_required
@admin_role_editor_required
def delete_repo(repo_id):
    get_repo_by_repo_id(repo_id)
    try:
        Repository.delete({'repoId': repo_id})

    except ModelInvalidParamsException as e:
        raise InvalidUsage(e.message, 400)

    except Exception as e:
        print(traceback.format_exc())
        raise InvalidUsage('Server Error', 500)

    return jsonify(), 204


def get_repo_by_repo_id(repo_id):
    repo = Repository.get_one({'repoId': repo_id})
    if not repo:
        raise InvalidUsage('Not Found', 404)

    return repo


def generate_repo_id(service_domain, service_segment, repo_name):
    services = Repository.services
    name = next((service['name']
                for service in services if service['domain'] == service_domain), None)
    if not name:
        raise InvalidUsage('Invalid service domain', 400)
    suffix = '-'.join([sanitize_domain_str(service_segment),
                       sanitize_domain_str(repo_name)])
    return f'{name}.{suffix}'


def schema_post():
    return {
        'serviceDomain': {
            'type': 'string',
            'coerce': (NormalizerUtils.trim),
            'required': True,
            'empty': False,
            'allowed': Repository.allowed_vals['serviceDomain'],
        },
        'serviceSegment': {
            'type': 'string',
            'coerce': (NormalizerUtils.trim),
            'required': True,
            'empty': False,
            'regex': r'^[0-9a-zA-Z\-_]+$',
        },
        'repoName': {
            'type': 'string',
            'coerce': (NormalizerUtils.trim),
            'required': True,
            'empty': False,
            'regex': r'^[0-9a-zA-Z\-_]+$',
        },
        'serverDomain': {
            'type': 'string',
            'coerce': (NormalizerUtils.trim),
            'required': True,
            'empty': False,
            'allowed': Repository.allowed_vals['serverDomain'],
        },
        'isBuildRequired': {
            'type': 'boolean',
            'coerce': (str, NormalizerUtils.to_bool),
            'required': False,
            'empty': False,
            'default': False,
        },
        'buildType': {
            'type': 'string',
            'coerce': (NormalizerUtils.trim),
            'required': False,
            'empty': True,
            'nullable': True,
            'allowed': Repository.allowed_vals['buildType'],
        },
        'nodeJSVersion': {
            'type': 'string',
            'coerce': (NormalizerUtils.trim),
            'required': False,
            'empty': True,
            'nullable': True,
            'allowed': Repository.allowed_vals['nodeJSVersion'],
        },
    }


def schema_get_list():
    base = get_list_schema
    schema = {
        'server': {
            'type': 'string',
            'coerce': (NormalizerUtils.trim),
            'required': False,
            'empty': True,
            'nullable': True,
            'allowed': Repository.allowed_vals['serverDomain'],
        },
    }
    return base | schema
