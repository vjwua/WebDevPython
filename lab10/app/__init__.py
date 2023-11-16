from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)
app.secret_key = b"277764450344399279392461713642952840400"
#using secrets.SystemRandom().getrandbits(128)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///flaskdb.db")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'

from app import views
from app import database

from .home import home_blueprint
app.register_blueprint(home_blueprint, url_prefix='/home')

from .todo import todo_blueprint
app.register_blueprint(todo_blueprint, url_prefix='/todo')

from .cookies import cookies_blueprint
app.register_blueprint(cookies_blueprint, url_prefix='/cookies')