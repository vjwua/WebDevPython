from app import db

class Enterprise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    activity_type = db.Column(db.String(100))
    number_of_workers = db.Column(db.Integer)
    revenue = db.Column(db.Double)