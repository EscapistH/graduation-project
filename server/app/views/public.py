from flask import request


def get_token_and_id():
    return request.headers.get('token'), request.headers.get('uid')
