from app.validators import NormalizerUtils

ulid_schema = {
    'type': 'string',
    'coerce': (str, NormalizerUtils.trim),
    'required': True,
    'empty': False,
    'valid_ulid': True,
}

user_id_schema = {
    'type': 'string',
    'coerce': (str, NormalizerUtils.trim),
    'required': True,
    'empty': False,
    'regex': r'^[a-zA-Z0-9]{28,32}$',
}

get_list_schema = {
    'count': {
        'type': 'integer',
        'coerce': int,
        'required': False,
        'min': 1,
        'max': 50,
        'default': 10,
    },
    'order': {
        'type': 'string',
        'required': False,
        'allowed': ['asc', 'desc'],
        'default': 'asc',
    },
}
