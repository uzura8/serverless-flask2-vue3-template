import traceback
from flask import Blueprint, jsonify, request
from app.routes import check_user_token, check_firebase_auth_or_pgit_client_ip
from app.models.dynamodb import Repository, Job, ModelInvalidParamsException, ModelConditionalCheckFailedException
from app.utils.error import InvalidUsage
from app.utils.request import validate_params
from app.utils.date import utc_iso
from app.utils.string import sanitize_domain_str
from app.utils.service import generate_repo_id
from app.validators import NormalizerUtils
from app.validators.schemas.common import get_list_schema

bp = Blueprint('repository', __name__, url_prefix='/repositories')


@bp.get('/')
@check_firebase_auth_or_pgit_client_ip
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


@bp.post('/')
@check_user_token
def create_repo():
    vals = validate_params(schema_create(), request.json)

    repo_code = generate_repo_id(
        vals['serviceDomain'], vals['serviceSegment'], vals['repoName'])
    if not repo_code:
        raise InvalidUsage('Invalid service domain', 400)

    keys = {'serverDomain': vals['serverDomain'], 'repoCode': repo_code}
    exists = Repository.get_one(keys, 'server_repoCode_idx')
    if exists:
        raise InvalidUsage('Already exists', 409)

    vals['repoCode'] = repo_code

    status = 'pending'
    vals['deployStatus'] = status
    # vals['createdBy'] = request.user.get('user_id', '')

    add_datetime = utc_iso()
    vals['updatedAt'] = add_datetime
    vals['deployStatusUpdatedAt'] = '#'.join([status, add_datetime])

    try:
        repo = Repository.create(vals, 'repoId', True)

    except ModelInvalidParamsException as e:
        raise InvalidUsage(e.message, 400)

    except Exception as e:
        print(traceback.format_exc())
        raise InvalidUsage('Server Error', 500)

    return jsonify(repo), 201


@bp.get('/<string:repo_id>')
@check_user_token
def get_repo(repo_id):
    repo = get_repo_by_repo_id(repo_id)
    return jsonify(repo), 200


@bp.put('/<string:repo_id>')
@check_user_token
def update_repo(repo_id):
    repo = get_repo_by_repo_id(repo_id)
    vals = validate_params(schema_update(), request.json)
    # vals['updatedBy'] = request.user.get('user_id', '')
    try:
        repo = Repository.update({'repoId': repo_id}, vals)

    except ModelInvalidParamsException as e:
        raise InvalidUsage(e.message, 400)

    except Exception as e:
        print(traceback.format_exc())
        raise InvalidUsage('Server Error', 500)

    return jsonify(repo), 200


@bp.put('/<string:repo_id>/deploy/<string:deploy_status>')
@check_firebase_auth_or_pgit_client_ip
def check_and_update_repo_status(repo_id, deploy_status):
    if deploy_status not in ['start', 'completed', 'failed']:
        raise InvalidUsage('Invalid status', 400)

    saved = get_repo_by_repo_id(repo_id)
    cond_vals = None
    if deploy_status == 'start':
        if saved.get('deployStatus') == 'inProgress':
            raise InvalidUsage('Locked', 423)
        upd_status = 'inProgress'
        cond_vals = {'deployStatus': 'pending'}

    elif deploy_status == 'completed':
        if saved.get('deployStatus') != 'inProgress':
            raise InvalidUsage(f'Status is invalid', 400)
        upd_status = 'completed'
        cond_vals = {'deployStatus': 'inProgress'}

    elif deploy_status == 'failed':
        if saved.get('deployStatus') != 'inProgress':
            raise InvalidUsage(f'Status is invalid', 400)
        upd_status = 'failed'
        cond_vals = {'deployStatus': 'inProgress'}

    upd_datetime = utc_iso()
    vals = {
        'updatedAt': upd_datetime,
        'deployStatus': upd_status,
        'deployStatusUpdatedAt': '#'.join([upd_status, upd_datetime]),
    }

    # updated_by = request.user.get('user_id', '')
    # if updated_by:
    #     vals['updatedBy'] = updated_by

    try:
        repo = Repository.update_by_conds({'repoId': repo_id}, vals, cond_vals)

    except ModelInvalidParamsException as e:
        raise InvalidUsage(e.message, 400)

    except ModelConditionalCheckFailedException as e:
        raise InvalidUsage(e.message, 400)

    except Exception as e:
        print(traceback.format_exc())
        raise InvalidUsage('Server Error', 500)

    return jsonify(repo), 200


@bp.delete('/<string:repo_id>')
@check_user_token
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


@bp.post('/<string:repo_id>/jobs')
@check_firebase_auth_or_pgit_client_ip
def create_repo_job(repo_id):
    repo = get_repo_by_repo_id(repo_id)
    vals = validate_params(schema_post_job(), request.json)
    vals['repoId'] = repo['repoId']
    vals['repoCode'] = repo['repoCode']
    vals['repoName'] = repo['repoName']
    vals['serverDomain'] = repo['serverDomain']
    vals['serviceDomain'] = repo['serviceDomain']
    vals['serviceSegment'] = repo['serviceSegment']
    vals['isBuildRequired'] = repo['isBuildRequired']
    vals['buildType'] = repo.get('buildType', '')
    vals['buildTargetDirPath'] = repo.get('buildTargetDirPath', '')
    vals['nodeJSVersion'] = repo.get('nodeJSVersion', '')

    status = 'pending'
    vals['deployStatus'] = status
    vals['deployType'] = 'add'

    add_datetime = utc_iso()
    vals['updatedAt'] = add_datetime
    vals['deployStatusCreatedAt'] = '#'.join([status, add_datetime])

    try:
        job = Job.create(vals, 'jobId', True)

    except ModelInvalidParamsException as e:
        raise InvalidUsage(e.message, 400)

    except Exception as e:
        print(traceback.format_exc())
        raise InvalidUsage('Server Error', 500)

    return jsonify(job), 200


def get_repo_by_repo_id(repo_id):
    repo = Repository.get_one({'repoId': repo_id})
    if not repo:
        raise InvalidUsage('Not Found', 404)

    return repo


allowed_schema_on_update = {
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
    'buildTargetDirPath': {
        'type': 'string',
        'coerce': (NormalizerUtils.trim),
        'required': False,
        'empty': True,
        'nullable': True,
        'default': 'src',
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


def schema_update():
    return allowed_schema_on_update


def schema_create():
    additional_schema = {
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
    }
    return allowed_schema_on_update | additional_schema


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


def schema_post_job():
    return {
        'branchName': {
            'type': 'string',
            'coerce': (NormalizerUtils.trim),
            'required': True,
            'empty': False,
            'regex': r'^[0-9a-zA-Z\-_\./]+$',
        },
    }
    # return allowed_schema_on_update | additional_schema
