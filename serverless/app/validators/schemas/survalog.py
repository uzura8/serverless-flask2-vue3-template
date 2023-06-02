from app.validators import NormalizerUtils


event_schema = {
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


game_schema = {
    'name': {
        'type': 'string',
        'coerce': (str, NormalizerUtils.trim),
        'required': False,
        'empty': True,
        'nullable': True,
    },
    'body': {
        'type': 'string',
        'coerce': (str, NormalizerUtils.trim),
        'required': False,
        'empty': True,
        'nullable': True,
    },
    'gameType': {
        'type': 'string',
        'coerce': (str, NormalizerUtils.trim),
        'required': True,
        'empty': False,
    },
    'gameTypeNote': {
        'type': 'string',
        'coerce': (str, NormalizerUtils.trim),
        'required': False,
        'empty': True,
        'nullable': True,
    },
    'duration': {
        'type': 'integer',
        'coerce': int,
        'required': False,
        'empty': True,
        'nullable': True,
    },
    'durationUnit': {
        'type': 'string',
        'coerce': (str, NormalizerUtils.trim),
        'required': False,
        'allowed': ['min', 'hour', 'day'],
    },
    'isUnlimitedRespawn': {
        'type': 'boolean',
        'coerce': bool,
        'required': False,
        'empty': True,
        'nullable': True,
        'default': False,
    },
    'respawnCount': {
        'type': 'integer',
        'coerce': int,
        'required': False,
        'empty': True,
        'nullable': True,
    },
    'firepowerLimitType': {
        'type': 'string',
        'coerce': (str, NormalizerUtils.trim),
        'required': False,
        'empty': True,
        'nullable': True,
        'allowed': ['none', 'semiAuto', 'realCount', 'countLimit', 'others'],
    },
    'firepowerLimitNote': {
        'type': 'string',
        'coerce': (str, NormalizerUtils.trim),
        'required': False,
        'empty': True,
        'nullable': True,
    },
    'joinedCount': {
        'type': 'integer',
        'coerce': int,
        'required': False,
        'empty': True,
        'nullable': True,
    },
    'matchResultType': {
        'type': 'string',
        'coerce': (str, NormalizerUtils.trim),
        'required': False,
        'empty': True,
        'nullable': True,
        'allowed': ['draw', 'redWin', 'yellowWin', 'others'],
    },
    'matchResultNote': {
        'type': 'string',
        'coerce': (str, NormalizerUtils.trim),
        'required': False,
        'empty': True,
        'nullable': True,
    },
    # 'createdBy': {
    #    'type': 'string',
    #    'coerce': (str, NormalizerUtils.trim),
    #    'required': True,
    #    'empty': False,
    # },
}
