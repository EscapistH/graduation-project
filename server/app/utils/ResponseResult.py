from flask import jsonify
from app.utils.StatusCode import StatusCode


class ResponseResult(object):
    result = {
        'data': [],
        'msg': '',
        'code': 0
    }

    @classmethod
    def get_result(cls, status, data=None):
        if data is None:
            data = []
        if status == 'Success':
            cls.result['data'] = data
            cls.result['msg'] = '请求成功'
            cls.result['code'] = StatusCode.Success
        elif status == 'Declined':
            cls.result['data'] = data
            cls.result['msg'] = '拒绝访问'
            cls.result['code'] = StatusCode.Declined
        elif status == 'Error':
            cls.result['data'] = data
            cls.result['msg'] = '请求失败'
            cls.result['code'] = StatusCode.Error
        return jsonify(cls.result)
