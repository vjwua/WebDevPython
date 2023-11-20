import enum

from app import db
from datetime import datetime
from sqlalchemy.types import Enum

class PostType(enum.Enum):
    News = 'News'
    Publication = 'Publication'
    Other = 'Other'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=True)
    image_file = db.Column(db.String(64), nullable=False, server_default='default.jpg')
    created = db.Column(db.DateTime, default=datetime.now())
    type = db.Column(db.Enum(PostType))   
    enabled = db.Column(db.Boolean, default=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.created}', '{self.type}', '{self.user_id})"