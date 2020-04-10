import datetime
import hashlib
import json

from flask import Blueprint, request

from app.utils.TokenOperate import TokenOperate
from app.utils.ResponseResult import ResponseResult

from app.extensions import db

public = Blueprint('login', __name__)


def get_token_and_id():
    return request.headers.get('token'), request.headers.get('uid')


@public.route('/login', methods=['POST'])
def do_login():
    # 初始化sql结果集
    sql_res = None
    if request.method == 'POST':
        # 获取页面传来的登录信息json
        in_json = json.loads(request.data)
        # 当前时间
        login_time = datetime.datetime.now().replace(microsecond=0)
        # 用户名登录
        if in_json['logby'] == 'username':
            # 获取页面传来的数据
            username, password = in_json['username'], in_json['password']
            # 获取该用户的手机号
            rs = db.session.execute('select u_phone from app.users where u_nick = :username', {'username': username}).fetchall()
            if len(rs) == 0:
                return ResponseResult.get_result('Error', [{'msg': '用户名或密码错误'}])
            phone = rs[0][0]
            # 创建sha256对象对传入的密码进行加密
            sha256 = hashlib.sha256()
            sha256.update((username + password + phone + '5A!t').encode('utf-8'))
            password_hash = sha256.hexdigest()
            # 登录验证
            sql = '''
                select
                u_id,
                u_nick,
                u_name,
                u_gender,
                u_phone,
                u_email,
                u_role,
                u_last_login_time
                from app.users
                where u_nick = :username and u_pwd = :pwd
            '''
            sql_res = db.session.execute(sql, {'username': username, 'pwd': password_hash}).fetchall()
            db.session.execute(
                'update app.users set u_last_login_time = :login_time where u_nick = :username',
                {'login_time': login_time, 'username': username}
            )
        # 手机号登录
        elif in_json['logby'] == 'phone':
            phone, password = in_json['username'], in_json['password']
            # 获取该用户的用户名
            rs = db.session.execute('select u_nick from app.users where u_phone = :phone', {'phone': phone}).fetchall()
            if len(rs) == 0:
                return ResponseResult.get_result('Error', [{'msg': '手机号或密码错误'}])
            username = rs[0][0]
            # 创建sha256对象对传入的密码进行加密
            sha256 = hashlib.sha256()
            sha256.update((username + password + phone + '5A!t').encode('utf-8'))
            password_hash = sha256.hexdigest()
            sql = '''
                select
                u_id,
                u_nick,
                u_name,
                u_gender,
                u_phone,
                u_email,
                u_role,
                u_last_login_time
                from app.users
                where u_phone = :phone and u_pwd = :pwd
            '''
            sql_res = db.session.execute(sql, {'phone': phone, 'pwd': password_hash}).fetchall()
            db.session.execute(
                'update app.users set u_last_login_time = :login_time where u_phone = :phone',
                {'login_time': login_time, 'phone': phone}
            )

        # 结果集不为空,即账号密码正确
        if len(sql_res):
            data = [
                {
                    'id': i[0],
                    'nick': i[1],
                    'name': i[2],
                    'gender': i[3],
                    'phone': i[4],
                    'email': i[5],
                    'role': i[6],
                    'last_login_time': str(i[7]),
                    'token': TokenOperate.gen_token(i[0], i[1])
                } for i in sql_res
            ]
            # print(data)
            return ResponseResult.get_result('Success', data)
        else:
            return ResponseResult.get_result('Error')


@public.route('/register', methods=['POST'])
def do_register():
    if request.method == 'POST':
        # 页面传来的数据
        in_json = json.loads(request.data)
        username = in_json['username']
        password = in_json['password']
        phone = in_json['phone']
        # 验证用户名是否注册
        sql = '''
        select * from app.users where u_nick = :username
        '''
        rs = db.session.execute(sql, {'username': username}).fetchall()
        if len(rs) == 1:
            return ResponseResult.get_result('Error', [{'msg': '注册失败，该用户名已存在'}])
        # 验证手机号是否注册
        sql = '''
        select * from app.users where u_phone = :phone
        '''
        rs = db.session.execute(sql, {'phone': phone}).fetchall()
        if len(rs) == 1:
            return ResponseResult.get_result('Error', [{'msg': '注册失败，该手机号已注册'}])
        # 注册
        if len(rs) == 0:
            # 当前时间，即用户注册时间
            create_time = datetime.datetime.now().replace(microsecond=0)
            # 创建hash对象，对密码进行加密后存储
            sha256 = hashlib.sha256()
            sha256.update((username + password + phone + '5A!t').encode('utf-8'))
            password_hash = sha256.hexdigest()
            sql = '''
            insert into app.users(u_nick,u_pwd,u_phone,u_create_time) values(:username,:password,:phone,:create_time)
            '''
            db.session.execute(
                sql, {
                    'username': username,
                    'password': password_hash,
                    'phone': phone,
                    'create_time': create_time
                }
            )
            return ResponseResult.get_result('Success', [{'msg': '注册成功'}])
