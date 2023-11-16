from flask import Flask, flash, render_template, request, redirect, url_for, send_file, make_response, session
from flask_login import login_user, current_user, logout_user, login_required

from app import app, bcrypt
from app.forms import LoginForm, ChangePasswordForm, RegisterForm, UpdateAccountForm
from app.database import db, User

from datetime import datetime
import os
import random
import email_validator
import secrets
from PIL import Image

my_skills = ["C++", "HTML & CSS", "MySQL", "JavaScript", "Java", "Python", "OpenGL", "Paint.net"]

def get_user_info():
    user_os = os.name
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return user_os, user_agent, current_time

@app.route('/base')
def index():
    user_os, user_agent, current_time = get_user_info()
    return render_template('base.html', user_os=user_os, user_agent=user_agent, current_time=current_time)

@app.route('/home')
@app.route('/')
def home():
    user_os, user_agent, current_time = get_user_info()
    return render_template('home.html', user_os=user_os, user_agent=user_agent, current_time=current_time)

@app.route('/cv')
def cv():
    return render_template('cv.html')

@app.route('/edu')
def edu():
    return render_template('edu.html')

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        image_file = form.image_file.data

        if password == confirm_password:
            new_user = User(username=username, email=email, password=password, image_file=image_file)
            db.session.add(new_user)
            db.session.commit()
        flash("Аккаунт зареєстровано", category=("success"))
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.validate_password(form.password.data):
            if form.remember.data:
                login_user(user, remember=form.remember.data)
                flash("Вхід виконано", category=("success"))
                return redirect(url_for('account'))
            else:
                flash("Ви не запамʼятали себе, введіть дані ще раз", category=("warning"))
                return redirect(url_for('home'))
        else:
            flash("Вхід не виконано", category=("warning"))
            return redirect(url_for('login'))
    
    return render_template('login.html', form=form)

@app.route('/users')
@login_required
def users():
    all_users = User.query.all()
    return render_template('users.html', all_users=all_users)

@app.route('/info', methods=['GET'])
@login_required
def info():
    cookies = request.cookies

    return render_template('info.html', cookies=cookies)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    cp_form = ChangePasswordForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data

        if form.picture.data:
            current_user.image_file = save_picture(form.picture.data)

        db.session.commit()
        flash("Аккаунт оновлено", category=("success"))
        return redirect(url_for('account'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    return render_template('account.html', form=form, cp_form=cp_form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@app.after_request
def after_request(response):
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        try:
            db.session.commit()
        except:
            flash("Помилка при оновленні last_seen", category=("danger"))
    return response

@app.route('/skills/')
@app.route('/skills/<int:id>')
def skills(id=None):
    if id is not None:
        if 0 <= id < len(my_skills):
            skill = my_skills[id]
            return render_template('skills.html', skill=skill)
        else:
            return render_template('skills.html')
    else:
        return render_template('skills.html', skills=my_skills, total_skills=len(my_skills))

@app.route('/change_password', methods=['POST'])
def change_password():
    cp_form = ChangePasswordForm()

    if cp_form.validate_on_submit():
        user = User.query.filter_by(email=cp_form.email.data).first()

        if user:
            new_password = cp_form.password.data
            confirm_new_password = cp_form.confirm_password.data

            if user:
                if new_password == confirm_new_password:
                    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                    user.password = hashed_password
                    db.session.commit()

                    flash("Пароль успішно змінено", category=("success"))
                    return redirect(url_for('account'))
                else:
                    flash("Паролі не збігаються", category="danger")
        else:
            flash("Користувача з такою поштою не існує", category="danger")

        flash("Ви не змінили пароль", category=("danger"))
        return redirect(url_for('account'))

    flash("Ви не набрали пароль. Спробуйте ще раз", category=("danger"))
    return redirect(url_for('account'))

@app.route("/main")
def main():
    return redirect(url_for("home"))