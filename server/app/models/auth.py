from app.extensions import db


class Auth(db.Model):
    __tablename__ = 'auth'
    __table_args__ = {'schema': 'app'}

    a_id = db.Column(db.Integer, primary_key=True)
    a_u_id = db.Column(db.Integer)
    a_token = db.Column(db.String(255))
    a_expire_time = db.Column(db.DateTime)
