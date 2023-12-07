from flask import url_for
import pytest
from app import create_app, db
from app.auth.models import User

@pytest.fixture(scope='module')
def client():
    app = create_app('test')
    app.config['SERVER_NAME'] = '127.0.0.1:5000'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture()
def user_test():
    user = User(username='brand_new', email='brand_new@example.com', password='password')
    return user

@pytest.fixture(scope='module')
def init_database(client):
    # Insert user data
    default_user = User(username='patkennedy', email='patkennedy24@gmail.com', password='FlaskIsAwesome')
    db.session.add(default_user)

    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

@pytest.fixture(scope='function')
def log_in_default_user(client):
    client.post(url_for('auth_bp.login'),
                     data={'email': 'patkennedy24@gmail.com', 'password': 'FlaskIsAwesome'},
                     follow_redirects=True
                     )

    yield  # this is where the testing happens!

    client.get(url_for('auth_bp.logout'))