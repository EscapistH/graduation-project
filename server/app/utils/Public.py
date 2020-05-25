from flask import request

from app.utils.TokenOperate import TokenOperate


def get_token_and_id():
    return request.headers.get('token'), request.headers.get('uid')


def is_login():
    token, uid = get_token_and_id()[0], get_token_and_id()[1]
    return TokenOperate.check_token(token, uid)
