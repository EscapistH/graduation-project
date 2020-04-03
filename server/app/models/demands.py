from app.extensions import db


class Demands(db.Model):
    __tablename__ = 'demands'
    __table_args__ = {'schema': 'app'}

    d_id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    d_title = db.Column(db.String(32))
    d_content = db.Column(db.Text)
    d_publisher = db.Column(db.String(255))
    d_pub_time = db.Column(db.DateTime)
    d_is_review = db.Column(db.Boolean, default=False)
    d_reviewer = db.Column(db.Integer)
    d_review_time = db.Column(db.DateTime)
    d_is_cancel = db.Column(db.Boolean, default=False)
