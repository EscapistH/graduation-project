import datetime
import hashlib
import json

from flask import Blueprint, request

from app.extensions import db
from app.utils.ResponseResult import ResponseResult
from app.utils.TokenOperate import TokenOperate
from app.utils.Public import get_token_and_id, is_login

users = Blueprint('users', __name__)


# 获取全部用户信息
@users.route('/users', methods=['GET'])
def get_users():
    if request.method == 'GET':
        sql = 'select id, name, phone, address, role, last_login_time, create_time from app.users where role != 3'
        rs = db.session.execute(sql).fetchall()
        data = []
        for r in rs:
            data.append(
                {
                    'id': r[0],
                    'name': r[1],
                    'phone': r[2],
                    'address': r[3],
                    'role': r[4],
                    'last_login_time': str(r[5]),
                    'create_time': str(r[6])
                }
            )
        return ResponseResult.get_result('Success', data)


# 获取单个用户信息
@users.route('/users/<int:uid>', methods=['GET'])
def get_user_by_id(uid):
    if request.method == 'GET':
        u_id = int(uid)
        sql = 'select id, name, phone, address, role, last_login_time, create_time from app.users where user = :user'
        rs = db.session.execute(sql, {'user': u_id}).fetchall()
        data = [
            {
                'id': r[0],
                'name': r[1],
                'phone': r[2],
                'address': r[3],
                'role': r[4],
                'last_login_time': str(r[5]),
                'create_time': str(r[6])
            } for r in rs
        ]
        # print(rs)
        return ResponseResult.get_result('Success', data)


"""
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
        if not TokenOperate.check_token(token, u_id):
            return ResponseResult.get_result('Declined')
        rs = db.session.execute('select u_phone from app.users where u_phone = :phone and u_id != :u_id',
                                {'phone': phone, 'u_id': u_id}).fetchall()
        if len(rs) >= 1:
            return ResponseResult.get_result('Error', [{'msg': '手机号已存在'}])
        sql = '''update app.users
        set u_name = :u_name, u_gender = :u_gender, u_phone = :u_phone, u_email = :u_email, u_modify_time = :u_modify_time
        where u_id = :u_id
        '''
        db.session.execute(sql, {'u_name': name, 'u_gender': gender, 'u_phone': phone, 'u_email': email, 'u_id': uid,
                                 'u_modify_time': modify_time})
        return ResponseResult.get_result('Success')



@users.route('/reset_pwd', methods=['PUT'])
def reset_user_password():
    if request.method == 'PUT':
        token, u_id = get_token_and_id()
        if not TokenOperate.check_token(token, u_id):
            return ResponseResult.get_result('Declined')
        reset_u_id = request.json['u_id']
        rs = db.session.execute('select u_nick, u_phone from app.users where u_id = :u_id',
                                {'u_id': reset_u_id}).fetchall()
        u_nick, u_phone = rs[0][0], rs[0][1]
        sha256 = hashlib.sha256()
        sha256.update((u_nick + '12345678' + u_phone + '5A!t').encode('utf-8'))
        password_hash = sha256.hexdigest()
        sql = 'update app.users set u_pwd = :pwd where u_id = :u_id'
        db.session.execute(sql, {'pwd': password_hash, 'u_id': reset_u_id})
        return ResponseResult.get_result('Success')
"""


# 登录函数
@users.route('/users/login', methods=['POST'])
def do_login():
    if request.method == 'POST':
        # 获取页面传来的登录信息json
        in_json = json.loads(request.data)
        # 登录时间
        login_time = datetime.datetime.now().replace(microsecond=0)
        # 获取页面传来的数据
        username, password = in_json['username'], in_json['password']
        # 创建sha256对象对传入的密码进行加密
        sha256 = hashlib.sha256()
        sha256.update((password + '5A!t').encode('utf-8'))
        password_hash = sha256.hexdigest()
        # 医院登录
        if in_json['log_as'] == 'hospital':
            # 登录验证
            sql = 'select * from app.users where "name" = :username and password = :password'
            rs = db.session.execute(sql, {'username': username, 'password': password_hash}).fetchall()
            if len(rs) == 0:
                return ResponseResult.get_result('Error', [{'msg': '医院名或密码错误'}])
            sql = 'update app.users set last_login_time = :login_time where "name" = :username'
            db.session.execute(sql, {'login_time': login_time, 'username': username})
            data = [
                {
                    'id': i[0],
                    'name': i[1],
                    'phone': i[3],
                    'address': i[4],
                    'role': i[5],
                    'is_review': i[9],
                    'reviewer': i[10],
                    'review_time': i[11],
                    'token': TokenOperate.gen_token(i[0])
                } for i in rs
            ]
            return ResponseResult.get_result('Success', data)

        # 手机号登录
        if in_json['log_as'] == 'user':
            # 登录验证
            sql = 'select * from app.users where phone = :phone and password = :password'
            rs = db.session.execute(sql, {'phone': username, 'password': password_hash}).fetchall()
            if len(rs) == 0:
                return ResponseResult.get_result('Error', [{'msg': '手机号或密码错误'}])
            sql = 'update app.users set last_login_time = :login_time where phone = :phone'
            db.session.execute(sql, {'login_time': login_time, 'phone': username})
            data = [
                {
                    'id': i[0],
                    'name': i[1],
                    'phone': i[3],
                    'role': i[5],
                    'token': TokenOperate.gen_token(i[0])
                } for i in rs
            ]
            return ResponseResult.get_result('Success', data)


# 注册函数
@users.route('/users', methods=['POST'])
def do_register():
    if request.method == 'POST':
        # 页面传来的数据
        in_json = json.loads(request.data)
        username = in_json['username']
        password = in_json['password']
        phone = in_json['phone']
        address = in_json['address']
        role = 3 if in_json['reg_as'] == 'hospital' else 4
        is_review = False if in_json['reg_as'] == 'hospital' else None
        # 当前时间，即用户注册时间
        create_time = datetime.datetime.now().replace(microsecond=0)
        if in_json['reg_as'] == 'hospital':
            # 验证用户名是否注册
            sql = 'select * from app.users where name = :username'
            rs = db.session.execute(sql, {'username': username}).fetchall()
            if len(rs) == 1:
                return ResponseResult.get_result('Error', [{'msg': '注册失败，该医院已存在'}])
        if in_json['reg_as'] == 'user':
            # 验证手机号是否注册
            sql = 'select * from app.users where phone = :phone'
            rs = db.session.execute(sql, {'phone': phone}).fetchall()
            if len(rs) == 1:
                return ResponseResult.get_result('Error', [{'msg': '注册失败，该手机号已注册'}])
        # 注册
        # 创建hash对象，对密码进行加密后存储
        sha256 = hashlib.sha256()
        sha256.update((password + '5A!t').encode('utf-8'))
        password_hash = sha256.hexdigest()
        if in_json['reg_as'] == 'hospital':
            sql = '''
            insert into
            app.users(name, password, address, role, create_time, is_review)
            values(:username,:password,:address,:role,:create_time,:is_review)
            '''
            db.session.execute(
                sql, {
                    'username': username,
                    'password': password_hash,
                    'address': address,
                    'role': role,
                    'create_time': create_time,
                    'is_review': is_review
                }
            )
        else:
            sql = '''
            insert into
            app.users(name, password, phone, role, create_time, is_review)
            values(:username,:password,:phone,:role,:create_time,:is_review)
            '''
            db.session.execute(
                sql, {
                    'username': username,
                    'password': password_hash,
                    'phone': phone,
                    'role': role,
                    'create_time': create_time,
                    'is_review': is_review
                }
            )
        return ResponseResult.get_result('Success', [{'msg': '注册成功'}])


@users.route('/set_reviewer', methods=['PUT'])
def set_reviewer():
    if request.method == 'PUT':
        token, u_id = get_token_and_id()
        if not TokenOperate.check_token(token, u_id):
            return ResponseResult.get_result('Declined')
        tgt_uid = request.json['new_reviewer']
        db.session.execute('update app.users set u_role = 2 where u_id = :tgt_uid', {'tgt_uid': tgt_uid})
        return ResponseResult.get_result('Success')
