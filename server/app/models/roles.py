from app.extensions import db


class Roles(db.Model):
    __tablename__ = 'roles'
    __table_args__ = {'schema': 'app'}

    r_id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    r_name = db.Column(db.String(255))
