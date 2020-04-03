import datetime
import hashlib

from app.extensions import db


class TokenOperate(object):

    @classmethod
    def gen_token(cls, u_id, u_name):
        # 获取当前时间和设置过期时间
        now_datetime = datetime.datetime.now().replace(microsecond=0)
        expire_time = datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(seconds=3600)
        now_datetime_str = str(now_datetime)

        # 获取数据库中该id对应的token
        sql = '''
        select a_expire_time, a_token from app.auth where a_u_id = :a_u_id
        '''
        rs = db.session.execute(sql, {'a_u_id': u_id}).fetchall()
        # 若数据库存在此用户id的token，更新并返回新token
        if len(rs) == 1:
            # 生成token
            sha256 = hashlib.sha256()
            sha256.update((str(u_id) + u_name + now_datetime_str).encode('utf-8'))
            token_str = sha256.hexdigest()
            sql = '''
            update app.auth set a_token = :new_token, a_expire_time = :new_expire_time where a_u_id = :a_u_id
            '''
            db.session.execute(sql, {'new_token': token_str, 'new_expire_time': expire_time, 'a_u_id': u_id})
            return token_str
        else:
            # 生成token
            sha256 = hashlib.sha256()
            sha256.update((str(u_id) + u_name + now_datetime_str).encode('utf-8'))
            token_str = sha256.hexdigest()
            sql = '''
            insert into app.auth (a_u_id, a_token, a_expire_time) values (:a_u_id, :a_token, :a_expire_time)
            '''
            db.session.execute(sql, {'a_u_id': u_id, 'a_token': token_str, 'a_expire_time': expire_time})
            return token_str

    @classmethod
    def check_token(cls, token, u_id):
        # 获取传入的token和当前时间
        in_token = token
        now_datetime = datetime.datetime.now().replace(microsecond=0)
        # 获取该用户id对应的token及expire_time
        sql = '''
        select a_token, a_expire_time from app.auth where a_u_id = :a_u_id
        '''
        rs = db.session.execute(sql, {'a_u_id': u_id}).fetchall()
        # 若不存在token则返回False
        if len(rs) != 1:
            return False
        # 数据库中的token和expire_time
        db_token = rs[0][0]
        db_expire_time = rs[0][1]
        # 判断token是否相同
        if db_token != in_token:
            return False
        # 若相同判断是否过期
        elif now_datetime > db_expire_time:
            return False
        else:
            return True
