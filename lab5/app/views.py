from flask import Flask, flash, render_template, request, redirect, url_for, json, make_response, session
from datetime import datetime
from app import app
from app.forms import LoginForm
import os
import random

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
    user_os, user_agent, current_time = get_user_info()
    return render_template('cv.html', user_os=user_os, user_agent=user_agent, current_time=current_time)

@app.route('/edu')
def edu():
    user_os, user_agent, current_time = get_user_info()
    return render_template('edu.html', user_os=user_os, user_agent=user_agent, current_time=current_time)

@app.route('/hobbies')
def hobbies():
    user_os, user_agent, current_time = get_user_info()
    return render_template('hobbies.html', user_os=user_os, user_agent=user_agent, current_time=current_time)

@app.route('/login', methods=['GET', 'POST'])
def login():
    user_os, user_agent, current_time = get_user_info()
    form = LoginForm()

    filename = os.path.join(app.static_folder, 'data', 'auth.json')
    with open(filename) as test_file:
        data = json.load(test_file)

    json_name = data['name']
    json_password = data['password']

    if form.validate_on_submit():
        form_name = form.username.data
        form_password = form.password.data
        form_remember = form.remember.data

        if json_name == form_name and json_password == form_password:
            user_id = random.randint(1, 10000)
            session['userId'] = user_id
            flash("Вхід виконано", category=("success"))
            if form_remember:
                session['name'] = form_name
                session['password'] = form_password
                return redirect(url_for('info', user=session['name']))
            else:
                return redirect(url_for('home'))
        else:
            flash("Вхід не виконано", category=("warning"))
            return render_template('login.html', form=form, user_os=user_os, user_agent=user_agent, current_time=current_time)
    
    return render_template('login.html', form=form, user_os=user_os, user_agent=user_agent, current_time=current_time)

@app.route('/info', methods=['GET'])
def info():
    cookies = request.cookies
    user_os, user_agent, current_time = get_user_info()
    return render_template('info.html', user_os=user_os, user_agent=user_agent, current_time=current_time, cookies=cookies)

@app.route('/logout')
def logout():
    session.pop('userId')
    session.pop('name')
    session.pop('password')    
    return redirect(url_for("login"))

@app.route('/skills/')
@app.route('/skills/<int:id>')
def skills(id=None):
    user_os, user_agent, current_time = get_user_info()
    if id is not None:
        if 0 <= id < len(my_skills):
            skill = my_skills[id]
            return render_template('skills.html', skill=skill, user_os=user_os, user_agent=user_agent, current_time=current_time)
        else:
            return render_template('skills.html', user_os=user_os, user_agent=user_agent, current_time=current_time)
    else:
        return render_template('skills.html', skills=my_skills, total_skills=len(my_skills), user_os=user_os, user_agent=user_agent, current_time=current_time)

def set_cookie(key, value, max_age):
    user_os, user_agent, current_time = get_user_info()
    flash("Кукі додано", category=("success"))
    response = make_response(render_template('home.html', user_os=user_os, user_agent=user_agent, current_time=current_time))
    response.set_cookie(key, value, max_age=max_age)
    return response

def delete_cookie(key):
    user_os, user_agent, current_time = get_user_info()
    flash("Кукі видалено", category=("danger"))
    response = make_response(render_template('home.html', user_os=user_os, user_agent=user_agent, current_time=current_time))
    response.delete_cookie(key)
    return response

@app.route('/add_cookie', methods=['POST'])
def add_cookie():
    key = request.form.get('key')
    value = request.form.get('value')
    max_age = int(request.form.get('max_age'))

    return set_cookie(key, value, max_age)

@app.route('/remove_cookie/', methods=['GET'])
@app.route('/remove_cookie/<key>', methods=['GET'])
def remove_cookie():

    key = request.args.get('key')

    if key:
        user_os, user_agent, current_time = get_user_info()
        flash("Кукі видалено", category=("dark"))
        response = make_response(render_template('home.html', user_os=user_os, user_agent=user_agent, current_time=current_time))
        response.delete_cookie(key)
        return response
    else:
        flash("Виникла помилка. Повідомте про ключ нам", category=("info"))
        user_os, user_agent, current_time = get_user_info()
        response = make_response(render_template('home.html', user_os=user_os, user_agent=user_agent, current_time=current_time))
        return response

@app.route('/remove_all_cookies', methods=['GET'])
def remove_all_cookies():
    user_os, user_agent, current_time = get_user_info()
    flash("Усі кукі видалено", category=("danger"))
    response = make_response(render_template('home.html', user_os=user_os, user_agent=user_agent, current_time=current_time))
    cookies = request.cookies

    for key in cookies.keys():
        if key != 'session':
            response.delete_cookie(key)

    return response

@app.route('/change_password', methods=['POST'])
def change_password():
    new_password = request.form.get('new_password')
    session['password'] = new_password
    user_os, user_agent, current_time = get_user_info()
    return render_template('password_changed.html', user_os=user_os, user_agent=user_agent, current_time=current_time)

@app.route("/main")
def main():
    return redirect(url_for("home"))