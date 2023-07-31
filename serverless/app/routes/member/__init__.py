import os
from flask import Blueprint

bp = Blueprint('member', __name__, url_prefix='/member')


def site_before_request(f):
    def wrapper(*args, **kwargs):
        f(*args, **kwargs)
        # g.locale = str(get_locale())
    return wrapper


# from . import hoge
