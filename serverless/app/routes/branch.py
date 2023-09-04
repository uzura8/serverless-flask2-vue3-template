from flask import Blueprint, jsonify, request
from app.routes import check_user_token
from app.models.dynamodb import Branch
from app.utils.error import InvalidUsage
from app.utils.request import validate_params
from app.validators import NormalizerUtils
from app.validators.schemas.common import get_list_schema

bp = Blueprint('branch', __name__, url_prefix='/branches')


@bp.get('/')
@check_user_token
def get_repo_list():
    vals = validate_params(get_list_schema, request.args.to_dict())
    items = Branch.scan()
    items = sorted(items, key=lambda x: x['createdAt'], reverse=True)
    return jsonify({'items': items}), 200


@bp.get('/<string:branch_id>')
@check_user_token
def get_branch(branch_id):
    item = get_branch_by_branch_id(branch_id)
    return jsonify(item), 200


def get_branch_by_branch_id(branch_id):
    branch = Branch.get_one({'branchId': branch_id})
    if not branch:
        raise InvalidUsage('Not Found', 404)
    return branch


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


def schema_get_jobs():
    base = get_list_schema
    schema = {
        'status': {
            'type': 'string',
            'coerce': (NormalizerUtils.trim),
            'required': False,
            'empty': True,
            'nullable': True,
            'allowed': Job.allowed_vals['deployStatus'],
        },
    }
    return base | schema
