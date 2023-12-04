from app import db

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    description = db.Column(db.String(300))
    rate = db.Column(db.Integer)
    useful = db.Column(db.Boolean)