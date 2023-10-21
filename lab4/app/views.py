from flask import Flask, render_template, request, redirect, url_for, json, session
import os
from datetime import datetime
from app import app

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
    if request.method == "POST":
        filename = os.path.join(app.static_folder, 'data', 'auth.json')
        with open(filename) as test_file:
            data = json.load(test_file)

        json_name = data['name']
        json_password = data['password']

        form_name = request.form.get("name")
        form_password = request.form.get("password")

        if json_name == form_name and json_password == form_password:
            session['name'] = form_name
            session['password'] = form_password
            return redirect(url_for('info', user=session['name']))
    
    return render_template('login.html', user_os=user_os, user_agent=user_agent, current_time=current_time)

@app.route('/info')
def info():
    user_os, user_agent, current_time = get_user_info()
    return render_template('info.html', user_os=user_os, user_agent=user_agent, current_time=current_time)

@app.route('/logout')
def logout():
    user_os, user_agent, current_time = get_user_info()
    session.pop('name', default=None)
    session.pop('password', default=None)    
    return redirect(url_for("home"))

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
    
@app.route("/main")
def main():
    return redirect(url_for("home"))