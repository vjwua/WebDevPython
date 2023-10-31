from app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Todo(db.Model):
    id = db.column(db.Integer, primary_key = True)
    title = db.column(db.String(100))
    complete = db.column(db.Boolean)