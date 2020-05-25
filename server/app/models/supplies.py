from app.extensions import db


class Supplies(db.Model):
    __tablename__ = 'supplies'
    __table_args__ = {'schema': 'app'}

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    name = db.Column(db.String(32))
    specification = db.Column(db.String(255))
    number = db.Column(db.Integer)

    demand = db.Column(db.Integer)
