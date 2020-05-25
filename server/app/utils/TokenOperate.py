import datetime
import hashlib

from app.extensions import db


class TokenOperate(object):

    @staticmethod
    def gen_token(user: int):
        # 获取当前时间和设置过期时间
        now_datetime = datetime.datetime.now().replace(microsecond=0)
        expire_time = now_datetime + datetime.timedelta(seconds=3600)
        now_datetime_str = str(now_datetime)

        # 生成token
        sha256 = hashlib.sha256()
        sha256.update((str(user) + now_datetime_str).encode('utf-8'))
        token_str = sha256.hexdigest()

        # 获取数据库中该id对应的token
        sql = 'select token, expire_time from app.tokens where "user" = :user'
        rs = db.session.execute(sql, {'user': int(user)}).fetchall()
        # 若数据库存在此用户id的token，更新并返回新token
        if len(rs) == 1:
            sql = 'update app.tokens set token = :new_token, expire_time = :new_expire_time where "user" = :user'
            db.session.execute(sql, {'new_token': token_str, 'new_expire_time': expire_time, 'user': int(user)})
            return token_str
        else:
            sql = 'insert into app.tokens ("user", token, expire_time) values (:user, :token, :expire_time)'
            db.session.execute(sql, {'user': int(user), 'token': token_str, 'expire_time': expire_time})
            return token_str

    @staticmethod
    def check_token(token: str, user: int):
        # 获取传入的token和当前时间
        in_token = token
        now_datetime = datetime.datetime.now().replace(microsecond=0)
        # 获取该用户id对应的token及expire_time
        sql = '''
        select token, expire_time from app.tokens where "user" = :user
        '''
        rs = db.session.execute(sql, {'user': int(user)}).fetchall()
        # 若不存在token则返回False
        if len(rs) != 1:
            return False
        # 数据库中的token和expire_time
        db_token, db_expire_time = rs[0][0], rs[0][1]
        # 判断token是否相同
        if db_token != in_token:
            return False
        # 若相同判断是否过期
        elif now_datetime > db_expire_time:
            return False
        else:
            return True
