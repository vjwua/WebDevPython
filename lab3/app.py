from flask import Flask, render_template, redirect, url_for
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('base.html')

@app.route('/cv')
def cv():
    return render_template('cv.html')

@app.route('/edu')
def edu():
    return render_template('edu.html')

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route("/main")
def main():
    return redirect(url_for("base"))