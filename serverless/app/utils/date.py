import re
from datetime import datetime, timezone


def utc_iso(dt=None, use_zulu_format=True, scale='millisec'):
    if not dt:
        dt = datetime.utcnow()

    if scale == 'millisec':
        dt = dt.replace(tzinfo=timezone.utc)
        res = dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + '+00:00'

    elif scale == 'sec':
        res = dt.replace(tzinfo=timezone.utc, microsecond=0).isoformat()

    else:
        res = dt.replace(tzinfo=timezone.utc).isoformat()

    if use_zulu_format:
        res = res.replace('+00:00', 'Z')

    return res
