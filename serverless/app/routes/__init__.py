import os
from functools import wraps
from flask import request
from firebase_admin import auth
from utils.request import is_valid_ip
from routes.allowed_ips import ALLOWED_IPS


def check_user_token(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not request.headers.get('authorization'):
            return {'message': 'No token provided'}, 400
        try:
            user = auth.verify_id_token(request.headers['authorization'])
            request.user = user
        except Exception as e:
            return {'message': 'Invalid token provided.'}, 400
        return f(*args, **kwargs)
    return wrap


def check_firebase_auth_or_pgit_client_ip(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if request.headers.get('authorization'):
            try:
                user = auth.verify_id_token(request.headers['authorization'])
                request.authType = 'firebase'
                request.user = user
            except Exception as e:
                return {'message': 'Invalid token provided.'}, 400
        else:
            client_ip = request.remote_addr  # Get ip address of client
            allowed_ips = ALLOWED_IPS['pgitClient']
            if client_ip not in allowed_ips:
                return {'message': 'Requested IP is invalid'}, 400
            request.authType = 'ip-address'
        return f(*args, **kwargs)
    return wrap


def check_webhook_client_ip(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        client_ip = request.remote_addr  # Get ip address of client

        is_allowed = False
        if client_ip in ALLOWED_IPS['backlog']:
            is_allowed = True
        elif is_valid_ip(client_ip, ALLOWED_IPS['github']):
            is_allowed = True

        if not is_allowed:
            return {'message': 'Requested IP is invalid'}, 400

        request.authType = 'ip-address'
        return f(*args, **kwargs)
    return wrap
