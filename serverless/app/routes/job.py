import traceback
from flask import Blueprint, jsonify, request
from app.routes import check_user_token, check_firebase_auth_or_pgit_client_ip
from app.models.dynamodb import Job, Repository, Branch, ModelInvalidParamsException, ModelConditionalCheckFailedException
from app.utils.error import InvalidUsage
from app.utils.request import validate_params
from app.utils.date import utc_iso
from app.utils.string import sanitize_domain_str
from app.utils.service import generate_repo_id
from app.validators import NormalizerUtils

bp = Blueprint('job', __name__, url_prefix='/jobs')


@bp.get('/')
@check_firebase_auth_or_pgit_client_ip
def get_job_list():
    items = Job.scan()
    res = {}
    res['items'] = sorted(
        items, key=lambda x: x['createdAt'], reverse=True)
    return jsonify(res), 200


@bp.post('/')
@check_user_token
def create_job():
    vals = validate_params(schema_create(), request.json)

    repo_code = generate_repo_id(
        vals['serviceDomain'], vals['serviceSegment'], vals['repoName'])
    if not repo_code:
        raise InvalidUsage('Invalid service domain', 400)

    keys = {'serverDomain': vals['serverDomain'], 'repoCode': repo_code}
    repo = Repository.get_one(keys, 'server_repoCode_idx')
    if not repo:
        raise InvalidUsage('Repository not exists', 400)

    vals['repoCode'] = repo_code
    vals['repoId'] = repo['repoId']
    vals['isBuildRequired'] = repo['isBuildRequired']
    vals['buildType'] = repo['buildType']
    vals['nodeJSVersion'] = repo['nodeJSVersion']

    status = 'pending'
    vals['deployStatus'] = status
    # vals['createdBy'] = request.user.get('user_id', '')

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

    return jsonify(job), 201


@bp.get('/<string:job_id>')
@check_user_token
def get_job(job_id):
    job = get_job_by_job_id(job_id)
    return jsonify(job), 200


@bp.put('/<string:job_id>/deploy/<string:deploy_status>')
@check_firebase_auth_or_pgit_client_ip
def check_and_update_job_status(job_id, deploy_status):
    if deploy_status not in ['start', 'completed', 'failed']:
        raise InvalidUsage('Invalid status', 400)

    vals = validate_params(schema_update(), request.json)
    saved = get_job_by_job_id(job_id)
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

    created_at = saved['createdAt']
    vals['deployStatus'] = upd_status
    vals['deployStatusCreatedAt'] = '#'.join([upd_status, created_at])

    # updated_by = request.user.get('user_id', '')
    # if updated_by:
    #     vals['updatedBy'] = updated_by

    try:
        job = Job.update_by_conds({'jobId': job_id}, vals, cond_vals, True)

    except ModelInvalidParamsException as e:
        raise InvalidUsage(e.message, 400)

    except ModelConditionalCheckFailedException as e:
        raise InvalidUsage(e.message, 400)

    except Exception as e:
        print(traceback.format_exc())
        raise InvalidUsage('Server Error', 500)

    if deploy_status == 'completed':
        if job['deployType'] == 'add':
            branchVals = {
                'repoId': job['repoId'],
                'branchName': job['branchName'],
                'repoCode': job['repoCode'],
                'serverDomain': job['serverDomain'],
                'serviceDomain': job['serviceDomain'],
                'serviceSegment': job['serviceSegment'],
                'repoName': job['repoName'],
                'lastCommitInfo': job.get('lastCommitInfo'),
                'updatedAt': utc_iso(),
            }
            try:
                Branch.create(branchVals, 'branchId', True)
            except ModelInvalidParamsException as e:
                raise InvalidUsage(e.message, 400)

            except Exception as e:
                print(traceback.format_exc())
                raise InvalidUsage('Server Error', 500)

        elif job['deployType'] == 'delete':
            br_keys = {'repoId': job['repoId'],
                       'branchName': job['branchName']}
            branch = Branch.get_one(br_keys, 'repo_branch_idx')
            if branch:
                try:
                    Branch.delete({'branchId': branch['branchId']})
                except ModelInvalidParamsException as e:
                    raise InvalidUsage(e.message, 400)

                except Exception as e:
                    print(traceback.format_exc())
                    raise InvalidUsage('Server Error', 500)

    return jsonify(job), 200


@bp.delete('/<string:job_id>')
@check_user_token
def delete_job(job_id):
    get_job_by_job_id(job_id)
    try:
        Repository.delete({'jobId': job_id})

    except ModelInvalidParamsException as e:
        raise InvalidUsage(e.message, 400)

    except Exception as e:
        print(traceback.format_exc())
        raise InvalidUsage('Server Error', 500)

    return jsonify(), 204


def get_job_by_job_id(job_id):
    job = Job.get_one({'jobId': job_id})
    if not job:
        raise InvalidUsage('Not Found', 404)
    return job


def schema_create():
    return {
        'serverDomain': {
            'type': 'string',
            'coerce': (NormalizerUtils.trim),
            'required': True,
            'empty': False,
            'allowed': Job.allowed_vals['serverDomain'],
        },
        'serviceDomain': {
            'type': 'string',
            'coerce': (NormalizerUtils.trim),
            'required': True,
            'empty': False,
            'allowed': Job.allowed_vals['serviceDomain'],
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
        'branchName': {
            'type': 'string',
            'coerce': (NormalizerUtils.trim),
            'required': True,
            'empty': False,
            'regex': r'^[0-9a-zA-Z\-_\./]+$',
        },
    }
    # return allowed_schema_on_update | additional_schema


def schema_update():
    return {
        'lastCommitInfo': {
            'type': 'dict',
            # 'coerce': (NormalizerUtils.json2dict),
            'required': False,
            'empty': True,
            'nullable': True,
            'schema': {
                'hash': {
                    'type': 'string',
                    'required': True,
                    'empty': False,
                },
                'authorName': {
                    'type': 'string',
                    'required': False,
                    'empty': True,
                    'nullable': True,
                },
                'message': {
                    'type': 'string',
                    'required': False,
                    'empty': True,
                    'nullable': True,
                },
                'date': {
                    'type': 'string',
                    'required': False,
                    'empty': True,
                    # 'regex': r'\d{4}\-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}([\+\-]\d{2}:\d{2}|Z)$',
                },
            }
        },
        'resultLog': {
            'type': 'string',
            'coerce': (NormalizerUtils.trim),
            'required': False,
            'empty': True,
            'nullable': True,
        },
    }
