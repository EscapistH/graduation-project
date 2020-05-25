from app.extensions import db


class Demands(db.Model):
    __tablename__ = 'demands'
    __table_args__ = {'schema': 'app'}

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    type = db.Column(db.String(2))

    publisher = db.Column(db.Integer)

    donate_for = db.Column(db.Integer)
    express_code = db.Column(db.String(255))
