from flask import url_for
from flask_login import current_user
from app.auth.models import User
from app import db

#HomePageTestCase
def test_main_page_view(client):
    response = client.get(url_for('home_bp.home'))
    assert response.status_code == 200
    assert b'Modal' in response.data

def test_cv_view(client):
    response = client.get(url_for('home_bp.cv'))
    assert response.status_code == 200
    assert b'Java' in response.data

def test_edu_view(client):
    response = client.get(url_for('home_bp.edu'))
    assert response.status_code == 200
    assert b'QT' in response.data

def test_hobbies_view(client):
    response = client.get(url_for('home_bp.hobbies'))
    assert response.status_code == 200
    assert b'Dendy' in response.data

def test_skills_view(client):
    response = client.get(url_for('home_bp.skills'))
    assert response.status_code == 200
    assert b'C++' in response.data

#UserTestCase
def test_add_user(client):
    """Ensure a new user can be added to the database."""
    response = client.post(
        url_for('auth_bp.register'),
        data=dict(
            username='michael',
            email='michael@realpython.com',
            password='123456',
            confirm_password='123456'
        ),
        follow_redirects=True
    )
    user = User.query.filter_by(email="michael@realpython.com").first()
    assert response.status_code == 200
    assert u'Аккаунт зареєстровано' in response.data.decode('utf8')
    assert user is not None

def test_register_page(client):
    response = client.get(url_for('auth_bp.register'))
    assert response.status_code == 200

def test_login_page(client):
    response = client.get(url_for('auth_bp.login'))
    assert response.status_code == 200

def test_get_account_page(user_test):
    db.session.add(user_test)
    db.session.commit()
    user = User.query.filter_by(email='brand_new@example.com').first()
    assert user.username == 'brand_new'

def test_get_account_page(init_database):
    user_new = User.query.filter_by(email='patkennedy24@gmail.com').first()
    assert user_new.username == 'patkennedy'

def test_home_page_post_with_fixture(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is posted to (POST)
    THEN check that a '405' (Method Not Allowed) status code is returned
    """
    response = client.post('/')
    assert response.status_code == 405
    assert b"Flask User Management Example!" not in response.data

def test_login_user(client):
    response = client.post(
        url_for('auth_bp.login', external=True),
        data=dict(
            email='michael@realpython.com',
            password='123456',
            remember = True
        ),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert current_user.is_authenticated == True
    assert u"Вхід виконано" in response.data.decode('utf8')

def test_login_user_with_fixture(log_in_default_user):
    assert current_user.is_authenticated == True
    #assert u"Вхід виконано" in response.data.decode('utf8')