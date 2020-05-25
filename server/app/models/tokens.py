from app.extensions import db


class Tokens(db.Model):
    __tablename__ = 'tokens'
    __table_args__ = {'schema': 'app'}

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer)
    token = db.Column(db.String(255))
    expire_time = db.Column(db.DateTime)
