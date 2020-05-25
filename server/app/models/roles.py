from app.extensions import db


class Roles(db.Model):
    __tablename__ = 'roles'
    __table_args__ = {'schema': 'app'}

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    name = db.Column(db.String(255))
