"""
全局定义Api响应状态码，
暂时只定义
20x:
    200: 请求成功
40x:
    401: 请求错误:未授权(请求无Token)
50x:
    500: 服务器错误
后期可以根据业务需求添加修改
"""


class StatusCode(object):
    Success = 200
    Declined = 401
    Error = 500
