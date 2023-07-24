import traceback
from flask import Blueprint, jsonify, request
from app.models.dynamodb import Category
from app.utils.error import InvalidUsage
from app.utils.request import validate_params
from app.validators import NormalizerUtils

bp = Blueprint('category', __name__, url_prefix='/categories')


@bp.get('/<string:cont_div>/<string:slug>')
def get_category_detail(cont_div, slug):
    vals = validate_params(schema_get_detail(), request.args, {
                           'contentDiv': cont_div, 'slug': slug})
    cate = Category.get_one_by_slug(
        vals['contentDiv'], vals['slug'], vals['withChildren'], True)
    if not cate:
        raise InvalidUsage('Not Found', 404)
    return jsonify(cate), 200


def schema_get_detail():
    return {
        'contentDiv': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': True,
            'empty': False,
            'allowed': Category.CONTENT_DIVS,
        },
        'slug': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': True,
            'empty': False,
            'maxlength': 128,
            'regex': r'^[0-9a-z\-]+$',
        },
        'withChildren': {
            'type': 'boolean',
            'coerce': (str, NormalizerUtils.to_bool),
            'required': False,
            'empty': True,
            'default': False,
        },
        # 'withParents': {
        #     'type': 'boolean',
        #     'coerce': (str, NormalizerUtils.to_bool),
        #     'required': False,
        #     'empty': True,
        #     'default': False,
        # },
    }
