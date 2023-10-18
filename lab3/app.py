from flask import Flask, render_template, request, redirect, url_for
import os
from _datetime import datetime

app = Flask(__name__)

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

@app.route("/main")
def main():
    return redirect(url_for("base"))

if __name__ == '__main__':
    app.run(debug=True)