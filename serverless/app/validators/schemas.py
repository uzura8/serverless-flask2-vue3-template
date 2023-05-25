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
