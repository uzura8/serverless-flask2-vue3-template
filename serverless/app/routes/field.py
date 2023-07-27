import traceback
from flask import Blueprint, jsonify, request
from app.firebase import check_user_token
from app.models.dynamodb import Field, Event, Category, ModelInvalidParamsException
from app.utils.error import InvalidUsage
from app.utils.request import validate_req_params
from app.utils.string import validate_uuid, validate_slug
from app.validators import NormalizerUtils

bp = Blueprint('field', __name__, url_prefix='/fields')


def get_field(identifier):
    if validate_uuid(identifier):
        keys = {'fieldId': identifier}
        index = None
    elif validate_slug(identifier):
        keys = {'slug': identifier}
        index = 'slug_idx'
    else:
        raise InvalidUsage('Invalid Identifier', 400)

    item = Field.get_one(keys, index)
    if not item:
        raise InvalidUsage('Not Found', 404)

    return item


@bp.get('/')
def get_field_list():
    items = Field.scan()
    return jsonify({'items': items}), 200


@bp.get('/categories/<string:cate_slug>')
def get_fields_by_cate_slug(cate_slug):
    cont_div_slug = '#'.join(['region', cate_slug])
    cate = Category.get_one(
        {'contentDivSlug': cont_div_slug}, 'ContentDivSlug_idx')
    if not cate:
        raise InvalidUsage('Not Found', 404)

    skey_val = '/'.join([cate.get('parentPath'), str(cate.get('cateId'))])
    keys = {
        'categoryContentDiv': cate.get('contentDiv'),
        'categoryRegionPathSlug': skey_val,
    }
    res = Field.get_all_pager(
        keys, None, 'categoryRegionParentPath_idx', False, 'begins_with')
    res['meta'] = {'category': cate}
    return jsonify(res), 200


@bp.get('/<string:field_id>')
def get_field_detail(field_id):
    item = get_field(field_id)
    return jsonify(Field.to_response(item)), 200


@bp.post('/<string:field_id>/events')
@check_user_token
def post_field_event(field_id):
    field = get_field(field_id)
    schema = validation_schema_post_event()
    vals = validate_req_params(schema, request.json)
    vals['fieldId'] = field_id
    vals['fieldIdDate'] = f'{field_id}#{vals["date"]}'
    # vals['fieldName'] = field.get('name')

    user_id = request.user.get('user_id')
    if user_id:
        vals['createdBy'] = user_id
        vals['createdUserType'] = 'user'

    try:
        event = Event.create(vals, 'eventId')

    except ModelInvalidParamsException as e:
        raise InvalidUsage(e.message, 400)

    except Exception as e:
        print(traceback.format_exc())
        raise InvalidUsage('Server Error', 500)

    event_response = Event.to_response(event)
    return jsonify(event_response), 201


@bp.get('/<string:identifier>/events/<string:date>')
def get_field_detail_event_list(identifier, date):
    field = get_field(identifier)
    field_id = field.get('fieldId')
    pkeys = {'fieldIdDate': f'{field_id}#{date}'}
    res = Event.get_all_pager(pkeys, None, 'fieldIdDateIndex')
    res['meta'] = {'field': field}
    return jsonify(res), 200


@bp.route('/<string:field_id>', methods=['HEAD'])
def head_field_detail(field_id):
    get_field(field_id)
    return jsonify(), 200


def validation_schema_get_field_detail():
    return {
        'fieldId': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': True,
            'empty': False,
            'valid_ulid': True,
        }
    }


def validation_schema_post_event():
    return {
        'fieldId': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': True,
            'empty': False,
            'valid_ulid': True,
        },
        'date': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': True,
            'empty': False,
            'regex': r'^\d{4}\d{2}\d{2}$'
        },
        'name': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': True,
            'empty': False,
        },
        'body': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': False,
            'empty': True,
        },
        'eventType': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': True,
            'allowed': ['regular', 'exclusive', 'others'],
        },
        'joinedCount': {
            'type': 'integer',
            'coerce': int,
            'required': False,
            'empty': True,
            'nullable': True,
        },
        'weatherType': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': False,
            'empty': True,
            'nullable': True,
            'allowed': [
                'clear',
                'cloudy',
                'cloudyOccasionallyClear',
                'rain',
                'heavyRain',
                'cloudyOccasionallyRain',
                'snow',
                'sleet'
            ],
        },
        'weatherText': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': False,
            'empty': True,
            'nullable': True,
        },
        'windType': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': False,
            'empty': True,
            'nullable': True,
            'allowed': ['calm', 'light', 'moderate', 'strong', 'gale'],
        },
        'temperature': {
            'type': 'integer',
            'coerce': int,
            'required': False,
            'empty': True,
            'nullable': True,
        },
        # 'temperatureUnit': {
        #    'type': 'string',
        #    'coerce': (str, NormalizerUtils.trim),
        #    'required': False,
        #    'allowed': ['celsius', 'fahrenheit'],
        # },
    }
