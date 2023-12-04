from flask import Flask, url_for
from flask_login import current_user
from flask_testing import TestCase
import unittest

from app import create_app, db, bcrypt
from app.auth.models import User
from app.todo.models import Todo

class BaseTestCase(TestCase):
    def setUp(self):
        self.app = create_app(config_name='test')
        self.appctx = self.app.app_context()
        self.appctx.push()
        db.create_all()
        self.add_user(self)
        self.client = self.app.test_client()

    def add_user(self):
        hashed_password = bcrypt.generate_password_hash("password")
        user = User("test", "test@gmail.com", "password")
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.appctx = None
        self.client = None

    """def test_register_user(self):
        user = User.query.filter_by(username='test').first()
        assert user.username == "test"
        assert user.email == "test@gmail.com"
        assert user.password != "password"

    def test_register_post(self):
        with self.client:
            response = self.client.post(
                url_for('auth_bp.register'),
                data=dict(
                    username="test", 
                    email="test@gmail.com", 
                    password="password"
                    ),
                follow_redirects = True
            )
            self.assertEqual(response.status_code, 200)
            print (response.data)
            print(b'Account created' in response.data)
            #user = User.query.filter_by(username='test').first()
            #assert user.username == "test"
            #assert user.email == "test@gmail.com"
            #assert user.password != "password"

    def test_login_user(self):
        with self.client:
            response = self.client.post(
                url_for('auth_bp.login'),
                data=dict(
                    email = "test@gmail.com",
                    password = "password",
                ),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            print(b'Login Succesful' in response.data)
    
    def test_todo_create(self):
        data = {
            'title': 'Write flask test',
            'description': 'bruh bruh',
            'complete': False,
        }
        with self.client:
            response = self.client.post(
                url_for('todo_bp.create_todo'),
                data = data,
                follow_redirects = True
            )
            self.assertEqual(response.status_code, 200)
            todo = Todo.query.get(1)
            assert todo.title == data['title']

    def test_get_all_todo(self):
        todo_1 = Todo(title="11", description="11", complete=False)
        todo_2 = Todo(title="22", description="22", complete=False)
        db.session.add_all([todo_1, todo_2])
        all_todo = Todo.query.count()
        assert all_todo == 2

    def test_update_todo_complete(self):
        todo_1 = Todo(title="11", description="11", complete=False)
        db.session.add(todo_1)
        with self.client:
            response = self.client.get(
                url_for('todo_bp.update_todo', todo_id = 1),
                follow_redirects = True
            )
            todo = Todo.query.get(1)
            assert todo.complete == True

#class ViewTestCase(BaseTestCase):
    def test_real_server_is_up_and_running(self):
        
        url = 'http://localhost:5000/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertIn(b'Footer', response.data)"""

if __name__ == '__main__':
    unittest.main()