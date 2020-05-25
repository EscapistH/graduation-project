import datetime

from app.extensions import db


class Users(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'app'}

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    address = db.Column(db.String(255))

    role = db.Column(db.SmallInteger)

    last_login_time = db.Column(db.DateTime)
    modify_time = db.Column(db.DateTime)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now().replace(microsecond=0))

    is_review = db.Column(db.Boolean)
    reviewer = db.Column(db.Integer)
    review_time = db.Column(db.DateTime)
