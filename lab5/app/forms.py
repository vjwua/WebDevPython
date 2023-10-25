from flask_wtf import flaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(flaskForm):
    username = StringField("Username", validators=[DataRequired("Це поле обовʼязкове")])
    password = PasswordField("Password", validators=[
                            DataRequired("Це поле обовʼязкове"),
                            Length(min=4, max=10)
                        ])
    remember = BooleanField("Remember")
    submit = SubmitField("Sign in")