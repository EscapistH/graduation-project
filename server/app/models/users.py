import datetime

from app.extensions import db


class Users(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'app'}

    u_id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    u_nick = db.Column(db.String(255))
    u_pwd = db.Column(db.String(255))
    u_name = db.Column(db.String(255))
    u_gender = db.Column(db.String(2))
    u_phone = db.Column(db.String(255))
    u_email = db.Column(db.String(255))
    u_last_login_time = db.Column(db.DateTime)
    u_modify_time = db.Column(db.DateTime)
    u_create_time = db.Column(db.DateTime, default=datetime.datetime.now().replace(microsecond=0))
    u_role = db.Column(db.SmallInteger, nullable=False, default=2)
