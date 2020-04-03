import datetime

from flask import Blueprint, request

from app.extensions import db
from app.utils.ResponseResult import ResponseResult
from app.utils.TokenOperate import TokenOperate
from app.views.public import get_token_and_id

users = Blueprint('users', __name__)


@users.route('/users', methods=['GET'])
def get_users():
    pass


@users.route('/users', methods=['POST'])
def add_user():
    pass


@users.route('/users/<int:uid>', methods=['GET'])
def get_user_by_id(uid):
    if request.method == 'GET':
        u_id = int(uid)
        sql = 'select u_nick, u_name, u_gender, u_phone, u_email from app.users where u_id = :u_id'
        rs = db.session.execute(sql, {'u_id': u_id}).fetchall()
        data = [
            {
                'nick': r[0],
                'name': r[1],
                'gender': r[2],
                'phone': r[3],
                'email': r[4],
            } for r in rs
        ]
        # print(rs)
        return ResponseResult.get_result('Success', data)


@users.route('/users/<int:uid>', methods=['PUT'])
def update_user_by_id(uid):
    in_json = request.json
    name = in_json['name']
    gender = in_json['gender']
    phone = in_json['phone']
    email = in_json['email']
    modify_time = datetime.datetime.now().replace(microsecond=0)
    if request.method == 'PUT':
        token, u_id = get_token_and_id()
        if TokenOperate.check_token(token, u_id):
            return ResponseResult.get_result('Declined')
        sql = '''update app.users
        set u_name = :u_name, u_gender = :u_gender, u_phone = :u_phone, u_email = :u_email, u_modify_time = :u_modify_time
        where u_id = :u_id
        '''
        db.session.execute(sql, {'u_name': name, 'u_gender': gender, 'u_phone': phone, 'u_email': email, 'u_id': uid,
                                 'u_modify_time': modify_time})
        return ResponseResult.get_result('Success')
